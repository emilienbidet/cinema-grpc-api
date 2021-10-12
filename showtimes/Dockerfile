FROM python:3.6
WORKDIR /showtimes/
EXPOSE 5002
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]