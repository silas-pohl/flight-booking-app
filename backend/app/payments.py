from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from . import schemas, crud

import os


class PayPalClient:
    def __init__(self):
        self.client_id = os.getenv('PAYPAL_SANDBOX_CLIENT_ID')
        self.client_secret = os.getenv('PAYPAL_SANDBOX_CLIENT_SECRET')

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                self.object_to_json(value) if not self.is_primittive(value) else\
                value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item)
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)


class CreateOrder(PayPalClient):

    # 2. Set up your server to receive a call from the client
    """ This is the sample function to create an order. It uses the
      JSON body returned by buildRequestBody() to create an order."""

    def create_order(self, flight: schemas.Flight, user: schemas.User):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        # 3. Call PayPal to set up a transaction
        request.request_body(self.build_request_body(flight=flight, user=user))
        response = self.client.execute(request)
        return response

    """Setting up the JSON request body for creating the order. Set the intent in the
    request body to "CAPTURE" for capture intent flow."""
    @staticmethod
    def build_request_body(flight: schemas.Flight, user: schemas.User):
        """Method to create body with CAPTURE intent"""

        ticket_price_dollars = flight.ticket_price_dollars
        return \
            {
                "intent": "CAPTURE",
                "application_context": {
                    "brand_name": "Flight Booking App",
                    "landing_page": "LOGIN",
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "PAY_NOW"
                },
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": ticket_price_dollars
                        },
                    }
                ]
            }


class CaptureOrder(PayPalClient):

    # 2. Set up your server to receive a call from the client
    """this sample function performs payment capture on the order.
    Approved order ID should be passed as an argument to this function"""

    def capture_order(self, order_id):
        """Method to capture order using order_id"""
        request = OrdersCaptureRequest(order_id)
        # 3. Call PayPal to capture an order
        response = self.client.execute(request)
        # 4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
        return response


create_order = CreateOrder()
capture_order = CaptureOrder()
