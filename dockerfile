FROM python:3.9-slim


WORKDIR /app


COPY . /app


RUN pip install pandas
RUN pip install psutil


ENTRYPOINT ["python", "hilos.py"]
CMD ["4"]  # Default parameter to be used if no other is provided at runtime

