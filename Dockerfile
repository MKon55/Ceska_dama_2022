FROM python:3.10
ADD . .
RUN pip install -r requirements.txt

#RUN adduser -u 5678 --disabled-password --gecos
#CMD ["pyhon", "-m", "", "dicover", "-s"]
CMD  python /main.py