FROM python:latest

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT [ "hypercorn" ]

EXPOSE 80

CMD [ "--workers", "3", "--bind", "0.0.0.0:80", "server:app" ]
