FROM python:3.9-slim

WORKDIR /app

COPY hilos.py ./

RUN pip install pandas

CMD ["python", "hilos.py", "4"]  
