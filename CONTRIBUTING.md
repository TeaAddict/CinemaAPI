
docker run -dp 5005:5000 -w /app -v ${pwd}:/app cinema-rest-api sh -c "flask run --host 0.0.0.0"

worked without container:
DATABASE_URL="postgresql://postgres:password@localhost:5432/cinema_db"

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run" , "--host", "0.0.0.0"]

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]