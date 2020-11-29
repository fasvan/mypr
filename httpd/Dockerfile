FROM httpd:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3.6

ADD requirements.txt / 
# "cashing"
RUN pip install -r requirements.txt
ADD . /
EXPOSE 8081

CMD [ "python", "test_get_homepage.py", "--alluredir=allure-results" ]