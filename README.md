# Deploying Flight Reservation API

- Prerequisites
1. Install `docker` and `docker-compose`

### Starting PostgreSQL
- `docker-compose -f docker-compose-postgres.yml up -d`

### Required Environment Variables
- **POSTGRES_USER:** Username that API may use to connect to Postgres
- **POSTGRES_DB:** Database that API migrates the changes and serve users
- **POSTGRES_PORT:** Port at which the Postgres is running
- **POSTGRES_PASSWORD:** Password that API may use to connect to Postgres
- **POSTGRES_HOST:** Host (URL) that API may use to connect to Postgres, e.g. 'localhost' or 'db.traveloair.com' or '10.20.0.0'


### Starting API
- Configurable variables should be isolated to .env
- Start with:
`docker build -t traveloair_flight_reservation_api:latest -f Dockerfile .`

`docker-compose -f docker-compose.yml up -d`
- Optional: include `-d` flag at end of docker-compose statement to run in background