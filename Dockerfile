FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask boto3
CMD ["python","main.py"]
