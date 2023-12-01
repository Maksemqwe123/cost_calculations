FROM python:3.9

WORKDIR /code/

COPY requirements.txt /code/

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade pip

CMD ["python", "bot_main.py"]
