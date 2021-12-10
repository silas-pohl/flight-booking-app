from datetime import datetime
from fastapi.testclient import TestClient
from app import main, schemas, models
from fastapi import HTTPException, status


client = TestClient(main.app)


def get_test_user():
    return schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="0deb3503-8efd-4f47-b842-44975098ff32",
        is_active=True,
        is_admin=False
    )


def get_test_user_with_hashed_password():
    return models.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="0deb3503-8efd-4f47-b842-44975098ff32",
        hashed_password="$2b$12$Y.a0OA0mjcWWlcearsG2COaxG5q9O0Ps/Wrc2nBNSOjJTJ5RA91dK",
        is_active=True,
        is_admin=False
    )


def get_test_user_json():
    return {
        "email": "test@test.test",
        "first_name": "test",
        "last_name": "test",
        "id": "0deb3503-8efd-4f47-b842-44975098ff32",
        "is_active": True,
        "is_admin": False
    }


def get_test_admin_user():
    return schemas.User(
        email="best@best.best",
        first_name="best",
        last_name="best",
        id="0deb3503-8efd-4f47-b842-44975098ff45",
        is_active=True,
        is_admin=True
    )


def get_inactive_test_user():
    return schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="0deb3503-8efd-4f47-b842-44975098ff32",
        is_active=False,
        is_admin=False
    )


def get_test_users():
    user1 = schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="0deb3503-8efd-4f47-b842-44975098ff32",
        is_active=True,
        is_admin=False
    )

    user2 = schemas.User(
        email="best@best.best",
        first_name="best",
        last_name="best",
        id="0deb3503-8efd-4f47-b842-44975098ff45",
        is_active=True,
        is_admin=True
    )

    return [user1, user2]


def get_test_users_json():
    return [{
        "email": "test@test.test",
        "first_name": "test",
        "last_name": "test",
        "id": "0deb3503-8efd-4f47-b842-44975098ff32",
        "is_active": True,
        "is_admin": False
    },
        {
        "email": "best@best.best",
        "first_name": "best",
        "last_name": "best",
        "id": "0deb3503-8efd-4f47-b842-44975098ff45",
        "is_active": True,
        "is_admin": True
    }]


def get_access_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXltZW50cy5mbGlnaHQuYm9va2luZ0BnbWFpbC5jb20iLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTYzODU1MDI4N30.pcjYDatsOw7rtbOl36s0aruAaKwl6dWYPHrxR94iI-A"


def get_refresh_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QudGVzdCJ9.O3JxzSUwBBSS7LOFUWPfJTcBRUSo_F48z_TiNGkFyJw"


def get_test_verification_entry():
    return schemas.EmailVerificationEntry(email="test@test.test",
                                          verification_code=12345678,
                                          created=datetime.now())


def get_valid_test_email():
    return "test@test.test"


def get_invalid_test_email():
    return "testtest.test"


def get_valid_names():
    return {
        "first_name": "Test",
        "last_name": "Test"
    }


def get_invalid_names():
    return {
        "first_name": "T",
        "last_name": "T"
    }


def get_valid_password():
    return "TestT3stT€st"


def get_invalid_password():
    return "TestT3st"


def get_tickets():
    ticket1 = schemas.Ticket(id="23c557f8-5fb6-4fc0-8cf6-a685d7680112", created=datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=177772), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")

    ticket2 = schemas.Ticket(id="e1d11a21-d346-4480-b4bb-c16da0347c3b", created=datetime(
        year=2021, month=12, day=4, hour=18, minute=14, second=9, microsecond=819645), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")

    return [ticket1, ticket2]


def get_tickets_json():
    return [
        {
            "id": "23c557f8-5fb6-4fc0-8cf6-a685d7680112",
            "created": "2021-12-03T11:23:25.177772",
            "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
            "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
        },
        {
            "id": "e1d11a21-d346-4480-b4bb-c16da0347c3b",
            "created": "2021-12-04T18:14:09.819645",
            "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
            "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
        }
    ]


def get_ticket():
    return schemas.Ticket(id="23c557f8-5fb6-4fc0-8cf6-a685d7680112", created=datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=177772), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")


def get_ticket_json():
    return {
        "id": "23c557f8-5fb6-4fc0-8cf6-a685d7680112",
        "created": "2021-12-03T11:23:25.177772",
        "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
        "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
    }


def get_airports():
    airport1 = schemas.Airport(
        title="JFK New York", id="9407584e-18b4-4023-86b1-884cc21ec647", description=None)
    airport2 = schemas.Airport(
        title="Munich Airport", id="41a7ead7-6dc3-4720-8108-35180659e39e", description=None)

    return [airport1, airport2]


def get_airports_json():
    return [
        {
            "title": "JFK New York",
            "id": "9407584e-18b4-4023-86b1-884cc21ec647",
            "description": None
        },
        {
            "title": "Munich Airport",
            "id": "41a7ead7-6dc3-4720-8108-35180659e39e",
            "description": None
        }
    ]


def get_airport():
    return schemas.Airport(
        title="JFK New York", id="9407584e-18b4-4023-86b1-884cc21ec647", description=None)


def get_airport_json():
    return {
        "title": "JFK New York",
        "id": "9407584e-18b4-4023-86b1-884cc21ec647",
        "description": None
    }


def get_flights():

    arrival_time = datetime(year=2021, month=12, day=3,
                            hour=11, minute=23, second=25, microsecond=151590)
    departure_time = datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=151582)

    return [schemas.Flight(id="20453064-2468-48ef-896f-b4a2513973a3", arrival_time_utc=arrival_time,
                           destination_airport_id="41a7ead7-6dc3-4720-8108-35180659e39e", seats=24, departure_time_utc=departure_time,
                           departure_airport_id="9407584e-18b4-4023-86b1-884cc21ec647", ticket_price_dollars=20.0)]


def get_flights_json():
    return [
        {
            "id": "20453064-2468-48ef-896f-b4a2513973a3",
            "arrival_time_utc": "2021-12-03T11:23:25.151590",
            "destination_airport_id": "41a7ead7-6dc3-4720-8108-35180659e39e",
            "seats": 24,
            "departure_time_utc": "2021-12-03T11:23:25.151582",
            "departure_airport_id": "9407584e-18b4-4023-86b1-884cc21ec647",
            "ticket_price_dollars": 20.0
        }
    ]


def get_flight():
    arrival_time = datetime(year=2021, month=12, day=3,
                            hour=11, minute=23, second=25, microsecond=151590)
    departure_time = datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=151582)

    return schemas.Flight(id="20453064-2468-48ef-896f-b4a2513973a3", arrival_time_utc=arrival_time,
                          destination_airport_id="41a7ead7-6dc3-4720-8108-35180659e39e", seats=24, departure_time_utc=departure_time,
                          departure_airport_id="9407584e-18b4-4023-86b1-884cc21ec647", ticket_price_dollars=20.0)


def get_flight_json():
    return{
        "id": "20453064-2468-48ef-896f-b4a2513973a3",
        "arrival_time_utc": "2021-12-03T11:23:25.151590",
        "destination_airport_id": "41a7ead7-6dc3-4720-8108-35180659e39e",
        "seats": 24,
        "departure_time_utc": "2021-12-03T11:23:25.151582",
        "departure_airport_id": "9407584e-18b4-4023-86b1-884cc21ec647",
        "ticket_price_dollars": 20.0
    }


def raise_http_401_could_not_validate_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_http_401_could_not_validate_credentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_http_400_inactive_user():
    raise HTTPException(status_code=400, detail="Inactive user")


def get_http_400_inactive_user():
    return HTTPException(status_code=400, detail="Inactive user")


def raise_http_401_unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized")


def get_http_401_unauthorized():
    return HTTPException(status_code=401, detail="Unauthorized")


def get_http_404_object_not_found():
    return HTTPException(status_code=404, detail="Object not found")


def get_http_422_invalid_id_format(id_type: str):
    return HTTPException(status_code=422, detail=[
        {
            "loc": [
                "path",
                id_type
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ])
