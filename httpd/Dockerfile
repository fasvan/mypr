FROM python:3.7.2

ADD requirements.txt / 
# "cashing"
RUN pip install -r requirements.txt
ADD . /

CMD [ "python", "test_get_homepage.py", "--alluredir=allure-results" ]