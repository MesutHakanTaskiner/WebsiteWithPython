from flask import Flask, redirect, url_for, render_template, Flask, request
import requests
from bs4 import BeautifulSoup
import re
import json
from operator import itemgetter 
import deepdiff

app = Flask(__name__)

@app.route("/")
def view_home():
    return render_template("home.html", title="Home page", content="Web Indexing")

@app.route("/Frequency", methods=["POST", "GET"])
def view_first_page():
    if request.method == "POST":
        url = request.form["url"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        text_string = soup.get_text()

        frequency = {}
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1

        return render_template("index.html", title="Frequency", content = json.dumps(frequency, indent=1))
    else:
        return render_template("index.html", title="Frequency")

@app.route("/KeyWord", methods=["POST", "GET"])
def view_second_page():
    if request.method == "POST":
        url = request.form["url"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        text_string = soup.get_text()

        frequency = {}
        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1
        
        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) 

        return render_template("index2.html", title="KeyWord", content = json.dumps(result, indent=1))
    else:
        return render_template("index2.html", title="KeyWord")

@app.route("/Similarity", methods=["POST", "GET"])
def view_third_page():
    if request.method == "POST":
        url = request.form["url"]
        url2 = request.form["url2"]

        page = requests.get(url)
        page2 = requests.get(url2)

        soup = BeautifulSoup(page.content, 'html.parser')
        soup2 = BeautifulSoup(page2.content, 'html.parser')

        text_string = soup.get_text()
        text_string2 = soup2.get_text()

        frequency = {}
        frequency2 = {}

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)
        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        
        for word in match_pattern:
            count = frequency.get(word, 0)
            frequency[word] = count + 1

        for word in match_pattern2:
            count = frequency2.get(word,0)
            frequency2[word] = count + 1

        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) 

        common_keys = result.keys() & frequency2.keys() # intersection operation on keys

        sum_result = 0
        sum_frequency2 = 0

        result_values = set(result)
        frequency2_values = set(frequency2)

        for name in result_values.intersection(frequency2_values):
            sum_result = sum_result + result[name]
            sum_frequency2 = sum_frequency2 + frequency2[name]

        try:
            similarity = ((sum_frequency2/sum_result)*100)
        except ZeroDivisionError:
            similarity = 0

        if(similarity == 0):
            str_similarity = "0"
        else:
            str_similarity = str(similarity)

        return render_template("index3.html", title="Similarity", content = ("Similarity Rate : " + "%" + str_similarity))
    else:    
        return render_template("index3.html", title="Similarity")

@app.route("/Indexing", methods=["POST", "GET"])
def view_fourth_page():
    return render_template("index4.html", title="Indexing")

@app.route("/Semantic", methods=["POST", "GET"])
def view_fifth_page():
    return render_template("index5.html", title="Semantic")

if __name__ == "__main__":
    app.run()