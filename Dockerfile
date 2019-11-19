FROM ubuntu

WORKDIR /root

RUN apt update && apt install -y g++ gcc python3 python3-pip git

RUN mkdir ./FlaskExample
COPY FlaskExample/src ./FlaskExample/src

#COPY FlaskExample/ ./FlaskExample
RUN chown -R root:root ./FlaskExample

WORKDIR /root/FlaskExample/src
RUN pip3 install -r requirements.txt

ENV SECRET_KEY hello
ENV FLASK_APP run.py

RUN chmod +x run.py
CMD python3 run.py
