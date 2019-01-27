FROM python:3.6
RUN apt-get update
RUN apt-get install -y default-jre
ADD ./hanlp_backend /infnlp/hanlp_backend
ADD ./server.py /infnlp/server.py
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /infnlp
CMD python server.py