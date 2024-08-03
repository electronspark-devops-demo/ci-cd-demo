FROM python:3.9-slim

WORKDIR /root/app
COPY requirements.txt /root/app/requirements.txt
COPY app.py /root/app/app.py
RUN pip install -r requirements.txt

COPY html /root/app/html

EXPOSE 80
CMD ["python", "app.py"]