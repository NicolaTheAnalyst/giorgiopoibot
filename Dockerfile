FROM python:3.7-alpine
COPY requirements.txt /tmp
RUN apk add --no-cache \
    libressl-dev \
	gcc \
	python3-dev \
	openssl-dev \
    musl-dev \
    libffi-dev && \
    pip install --no-cache-dir cryptography==2.3 && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev
#so yeah, installing cryptography was kinda problematic
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /code
COPY main.py /code/
COPY Songs.db /code/
CMD ["python3", "main.py"]
