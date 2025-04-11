## Run

docker-compose up --build -d

## Endpoint for events (POST)

http://localhost:8000/api/v1/ddup_service/events

## Tests

docker-compose -f docker-compose.loadtest.yml up -d

## Locust GUI on tests

http://localhost:8089
