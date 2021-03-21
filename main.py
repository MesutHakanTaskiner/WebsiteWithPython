from flask import Flask, redirect, url_for, render_template, Flask, request
import requests
from bs4 import BeautifulSoup
import re
import json

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
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1

        return render_template("index2.html", title="KeyWord", content = json.dumps(frequency, indent=1))
    else:
        return render_template("index2.html", title="KeyWord")

@app.route("/Similarity")
def view_third_page():
    return render_template("index3.html", title="Similarity")

@app.route("/Indexing")
def view_fourth_page():
    return render_template("index4.html", title="Indexing")

@app.route("/Semantic")
def view_fifth_page():
    return render_template("index5.html", title="Semantic")

if __name__ == "__main__":
    app.run()