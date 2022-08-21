FROM ubuntu:18.04

WORKDIR /app
RUN apt-get update -y
RUN apt install python3 -y && apt-get install -y python3-pip
RUN apt-get install vim && apt-get install nano

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
