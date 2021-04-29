FROM python:3.9

RUN apt-get update && \
    apt-get install -y python-opencv && \
    apt-get clean && \
    apt-get -y autoremove && \
    python3 -m pip install --upgrade pip 

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
RUN ./download.sh

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENTRYPOINT [ "python3", "tikfake/bot.py"]