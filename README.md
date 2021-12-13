### Hey 👋
The **Flight Booking App** is a web application that simulates the process of booking a flight, taking security into account already in the design of the application.

The application uses [Svelte](https://svelte.dev/) in the frontend, [FastAPI](https://fastapi.tiangolo.com/) in the backend and [PostgreSQL](https://www.postgresql.org/) as database. Any changes to the `main` branch are automatically checked with CodeQL and deployed to [Heroku](https://www.heroku.com) via a Github actions workflows, so both backend and frontend are accessible via the following links: 

🔴 https://frontend-flight-booking-app.herokuapp.com/

🔴 https://backend-flight-booking-app.herokuapp.com/

## 🛠️ Development

1. Clone repository
```
git clone https://github.com/silas-pohl/flight-booking-app.git

cd flight-booking-app
```
2. Create `/backend/.env` with the following content (values in curly brackets must be replaced accordingly):
```
POSTGRES_USER={postgres_user}
POSTGRES_PASSWORD={postgres_password}
POSTGRES_DATABASE={postgres_database}
POSTGRES_HOST=database
POSTGRES_PORT=5432

ACCESS_TOKEN_SECRET={access_token_secret}
REFRESH_TOKEN_SECRET={refresh_token_secret}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=0.25

EMAIL_ADDRESS={gmail_address}
EMAIL_PASSWORD={gmail_address_password}
```

3. Change `API_URL` in `/frontend/src/store.ts` to `'http://localhost:80'`
```
export const API_URL: Readable<string> = readable('http://localhost:80');
```

4. Change **both** Cookie-Domains in `/backend/app/main.py` to `'localhost'`
```
response.set_cookie(key="refresh_token", value=refresh_token, domain="localhost",  httponly=True, samesite="none", secure=True)
```

5. Start frontend, backend and local database via `docker-compose up`
```
docker-compose up
```
6. Access frontend on http://localhost:5000/ and backend on http://localhost:80/
