FROM python:3.11.0-alpine

WORKDIR /backend

COPY requirements.txt ./

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/backend

CMD ["./scripts/start.sh"]