FROM python:3.7-alpine

ADD . /usr/local/
ENV PYTHONPATH /usr/local/

RUN pip install --no-cache-dir -r /usr/local/requirements.txt
RUN pytest /usr/local/checkout_challenge/client

CMD python /usr/local/checkout_challenge/__init__.py