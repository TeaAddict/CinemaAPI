
docker run -dp 5005:5000 -w /app -v ${pwd}:/app cinema-rest-api sh -c "flask run --host 0.0.0.0"

worked without container:
DATABASE_URL="postgresql://postgres:password@localhost:5432/cinema_db"
