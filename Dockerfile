FROM python:3.10.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./app ./

RUN chmod +x ./start.sh
CMD ["/bin/bash", "-c", "./start.sh"]
