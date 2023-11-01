FROM python:3.10

WORKDIR /gpt-tg-bot

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

RUN chmod 755 .

COPY --chmod=777 . .