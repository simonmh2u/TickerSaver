FROM python:alpine3.16

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=.
COPY . .
RUN mkdir -p /usr/src/app/tmp

CMD [ "python", "./tickersaver/fetcher/kite/ws_tick_fetcher.py", "-c","tmp/tickerconfig.json" ]

#docker build -t tickersaver-alpine .
#docker run -it --rm -v $HOME/livetrade:/usr/src/app/tmp --name tickersaver tickersaver-alpine