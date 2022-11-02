FROM alpine:3.10

RUN apk add --update make cmake gcc g++ gfortran
RUN apk add --no-cache python3-dev\
    && pip3 install --upgrade pip
    
RUN pip3 install cython
RUN pip3 install numpy

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3","src/app.py"]

