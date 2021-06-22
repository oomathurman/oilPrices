FROM ubuntu:18.04
COPY prices.py /scripts/pricesInitial.py
RUN apt-get update 
RUN apt-get install -y apache2
RUN apt-get install -y cron
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install requests
# RUN apt-get install -y openssh-server
RUN apt-get clean
RUN echo "*/30 * * * * python3 /scripts/prices.py >/dev/null 2>&1" >> /etc/cron.d/prices
RUN echo "# empty line for cron" >> /etc/cron.d/prices
RUN crontab /etc/cron.d/prices
RUN python3 /scripts/pricesInitial.py
ENTRYPOINT apache2ctl start && /etc/init.d/cron start && bash