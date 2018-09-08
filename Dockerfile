FROM python:3

ENV DNS_REFRESH_TIME_S 5
ENV DNS_FILTER_CONTAINS intranet
ENV HOST_PATH /usr/src/hosts

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
