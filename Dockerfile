FROM python:3.12
RUN apt-get update -y && apt-get install -y build-essential
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]