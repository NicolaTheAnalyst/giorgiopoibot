FROM python:3.10.0-alpine
COPY requirements.txt /tmp
WORKDIR /code
COPY main.py /code/
COPY Songs.db /code/
RUN pip3 install -r /tmp/requirements.txt
CMD ["python3", "main.py"]
EXPOSE 80/tcp
