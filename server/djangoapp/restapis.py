# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# def get_request(endpoint, **kwargs):
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    # request_url = backend_url + endpoint + "?" + params
    request_url = backend_url.rstrip("/") + "/" + endpoint.lstrip("/") + "?" + params

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except:
        print("Network exception occurred")

# Add code for get requests to back end

# def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    encoded_text = quote(text)
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + encoded_text

    print("GET sentiment from {}".format(request_url))

    try:
        response = requests.get(request_url, timeout=10)
        print("Sentiment status:", response.status_code)
        print("Sentiment response:", response.text[:300])

        if response.status_code == 200:
            return response.json()
        else:
            return {"sentiment": "neutral"}

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"sentiment": "neutral"}
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
# Add code for posting review
def post_review(data_dict):
    request_url = backend_url.rstrip("/") + "/insert_review"
    print("POST to {}".format(request_url))
    print("POST payload:", data_dict)

    try:
        response = requests.post(request_url, json=data_dict)
        print("Backend POST status:", response.status_code)
        print("Backend POST response:", response.text[:500])
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"status": 500, "error": str(e)}