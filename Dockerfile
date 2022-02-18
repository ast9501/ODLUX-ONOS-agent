FROM python:3.8.12-buster

WORKDIR /src
COPY main.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000