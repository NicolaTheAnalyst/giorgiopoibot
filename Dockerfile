FROM python:3.11.0
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /code
COPY main.py /code/
COPY Songs.db /code/
CMD ["python3", "main.py"]