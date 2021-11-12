FROM python:3.6
WORKDIR /client/
EXPOSE 5005
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]