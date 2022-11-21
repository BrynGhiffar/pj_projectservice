FROM python:3.10-slim

WORKDIR /pj-projectservice

COPY requirements.txt /pj-projectservice/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pj-projectservice/requirements.txt

COPY . /pj-projectservice/src

WORKDIR /pj-projectservice/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--proxy-headers"]