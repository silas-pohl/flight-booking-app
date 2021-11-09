### Hey 👋
The **Flight Booking App** is a web application that simulates the process of booking a flight, taking security into account already in the design of the application.

The application uses [Svelte](https://svelte.dev/) in the frontend, [FastAPI](https://fastapi.tiangolo.com/) in the backend and [PostgreSQL](https://www.postgresql.org/) as database. Any changes to the `main` branch are automatically deployed to [Heroku](https://www.heroku.com) via a Github actions workflow, so both backend and frontend are accessible via the following links: 

🔴 https://frontend-flight-booking-app.herokuapp.com/

🔴 https://backend-flight-booking-app.herokuapp.com/

## 🛠️ Development

Clone repository
```
git clone https://github.com/silas-pohl/flight-booking-app.git

cd flight-booking-app
```
Create `/backend/.env` with the following content (`USER`, `PASSWORD` and `DATABASE` can be changed):
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DATABASE=postgres
POSTGRES_HOST=database
POSTGRES_PORT=5432
```
Start frontend, backend and local database via `docker-compose up`
```
docker-compose up
```
Access frontend on http://localhost:5000/ and backend on http://localhost:80/