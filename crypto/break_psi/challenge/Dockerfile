FROM python:3.10-slim

RUN apt update -y && apt install socat -yq

WORKDIR /app

COPY ./ /app

RUN pip install -r requirements.txt

EXPOSE 1337

ENTRYPOINT [ "socat" ]
CMD ["TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'python /app/PSI.py'"]