FROM httpd:latest

ADD requirements.txt / 
# "cashing"
RUN pip install -r requirements.txt
ADD . /
EXPOSE 8081

CMD [ "python", "test_get_homepage.py" ]