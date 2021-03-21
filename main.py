from flask import Flask, redirect, url_for, render_template, Flask, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def view_home():
    return render_template("index.html", title="Home page", content="Web Indexing")

@app.route("/Frequency", methods=["POST", "GET"])
def view_first_page():
    if request.method == "POST":
        url = request.form["url"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        return render_template("index.html", title="Frequency", content = soup.get_text())
    else:
        return render_template("index.html", title="Frequency")

@app.route("/KeyWord")
def view_second_page():
    return render_template("index.html", title="KeyWord")

@app.route("/Similarity")
def view_third_page():
    return render_template("index.html", title="Similarity")

@app.route("/Indexing")
def view_fourth_page():
    return render_template("index.html", title="Indexing")

@app.route("/Semantic")
def view_fifth_page():
    return render_template("index.html", title="Semantic")

if __name__ == "__main__":
    app.run()