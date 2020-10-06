 FROM alpine:3.12

 RUN apk update \
    && apk add --no-cache python3-dev \
    && apk add py-pip
 WORKDIR /src

 COPY . /src
 RUN pip3 install -r requirements.txt

 EXPOSE 5000:5000
