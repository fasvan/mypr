import os
import pytest
import requests

def test_get_homepage():
    r = requests.get("http://127.0.0.1:8081/")
    assert r.text == "Staging Environment!"