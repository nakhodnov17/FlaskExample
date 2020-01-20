FROM python:3.8-slim AS builder

COPY FlaskExample/src /root/FlaskExample/src

RUN chown -R root:root /root/FlaskExample

WORKDIR /root/FlaskExample/src
RUN pip3 install --target="/python-packages" -r requirements.txt

RUN chmod +x run.py


FROM python:3.8-alpine

COPY --from=builder /python-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /root/FlaskExample/src /root/FlaskExample/src

WORKDIR /root/FlaskExample/src

ENV SECRET_KEY hello
ENV FLASK_APP run.py

CMD ["python3", "run.py"]
