FROM python:3.6
WORKDIR /users/
EXPOSE 5003
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]