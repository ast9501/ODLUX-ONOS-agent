FROM python:3.8.12-buster

RUN add main.py
RUN add requirements.txt
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000