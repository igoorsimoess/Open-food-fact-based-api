FROM python:3.8.10

ENV DJANGO_SETTINGS_MODULE food_details_api.settings

WORKDIR /food_details_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY db_connection.py .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
