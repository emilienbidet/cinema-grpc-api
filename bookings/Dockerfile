FROM python:3.6
WORKDIR /bookings/
EXPOSE 5001
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]