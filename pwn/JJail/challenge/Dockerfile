FROM julia:latest

RUN apt update -y && apt install socat -yq


COPY jail.jl /jjail/jail.jl

WORKDIR /jjail
COPY flag flag

EXPOSE 1337

ENTRYPOINT [ "socat" ]
CMD ["TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'julia /jjail/jail.jl'"]
