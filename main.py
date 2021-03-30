from flask import Flask, redirect, url_for, render_template, Flask, request
from bs4 import BeautifulSoup
from operator import itemgetter
from nltk.corpus import wordnet
import requests
import re
import json
import operator
import nltk

app = Flask(__name__)

@app.route("/")
def view_home():
    return render_template("home.html", title="Home page", content="Web Indexing")

@app.route("/Frequency", methods=["POST", "GET"])
def Frequency():
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
        
        total_frequency = ""
        for key, value in sorted(frequency.items(), key=operator.itemgetter(1), reverse=True):
            total_frequency = total_frequency + "   ~{}: {}".format(key, value) + "\n"

        return render_template("index.html", title="Frequency", content = total_frequency)
    else:
        return render_template("index.html", title="Frequency")

@app.route("/KeyWord", methods=["POST", "GET"])
def KeyWord():
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
def Similarity():
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

        frequency2_total = {}

        result_values = set(result)
        frequency2_values = set(frequency2)

        for name in result_values.intersection(frequency2_values):
            sum_result = sum_result + result[name]
            sum_frequency2 = sum_frequency2 + frequency2[name]
            frequency2_total[name] = frequency2[name]

        str_frequency2_total = str(frequency2_total)

        try:
            similarity = ((sum_result/sum_frequency2)*100)
            if(similarity > 100):
                similarity = ((sum_frequency2/sum_result)*100)
        except ZeroDivisionError:
            similarity = 0

        if(similarity == 0):
            str_similarity = "0"
        else:
            str_similarity = str(similarity)

        return render_template("index3.html", title="Similarity", content = json.dumps(frequency2_total, indent = 1) + "\n\n\n              Similarity Rate : " + "%" + str_similarity)
    else:    
        return render_template("index3.html", title="Similarity")

def get_link(url):
    links = []
    
    for link in url.findAll('a', attrs={'href': re.compile("^https://")}):
        links.append(link.get('href'))

    first_url = links[0]
    second_url = links[4]

    return first_url, second_url
        
def finding_frequency(text):
    
    frequency = {}  

    for word in text:
            count = frequency.get(word,0)
            frequency[word] = count + 1

    return frequency

def finding_result_sum(result_values, frequency_values, result, frequency):

    sum_result = 0
    sum_frequency = 0
    frequency_total = {}

    for name2 in result_values.intersection(frequency_values):
        sum_result = sum_result + result[name2]
        sum_frequency = sum_frequency + frequency[name2]
        frequency_total[name2] = frequency[name2]

    similarity = 0

    try:
        similarity = ((sum_result/sum_frequency)*100)
        if(similarity > 100):
            similarity = ((sum_frequency/sum_result)*100)
    except ZeroDivisionError:
        similarity = 0

    return similarity

@app.route("/Indexing", methods=["POST", "GET"])
def Indexing():
    if request.method == "POST":
        url = request.form["url"]

        page = requests.get(url)

        page2 = requests.get('https://en.wikipedia.org/wiki/Earth')
        page3 = requests.get('https://en.wikipedia.org/wiki/Venus')
        page4 = requests.get('https://en.wikipedia.org/wiki/Jupiter')
        
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")

        soup2 = BeautifulSoup(page2.content, 'html.parser', from_encoding="iso-8859-1")
        soup3 = BeautifulSoup(page3.content, 'html.parser', from_encoding="iso-8859-1")
        soup4 = BeautifulSoup(page4.content, 'html.parser', from_encoding="iso-8859-1")

        links2_1, links2_2 = get_link(soup2)
        links3_1, links3_2 = get_link(soup3)
        links4_1, links4_2 = get_link(soup4)

        #2 sub-links derived from the 2nd link 
        page2_1 = requests.get(links2_1)
        soup2_1 = BeautifulSoup(page2_1.content, 'html.parser', from_encoding="iso-8859-1")
        page2_2 = requests.get(links2_2)
        soup2_2 = BeautifulSoup(page2_2.content, 'html.parser', from_encoding="iso-8859-1")

        links2_1_1, links2_1_2 = get_link(soup2_1)
        links2_2_1, links2_2_2 = get_link(soup2_2)

        #4 sub-links derived from the 2.1 link
        page2_1_1 = requests.get(links2_1_1)
        soup2_1_1 = BeautifulSoup(page2_1_1.content, 'html.parser', from_encoding="iso-8859-1")
        page2_1_2 = requests.get(links2_1_2)
        soup2_1_2 = BeautifulSoup(page2_1_2.content, 'html.parser', from_encoding="iso-8859-1")

        #4 sub-links derived from the 2.2 link
        page2_2_1 = requests.get(links2_2_1)
        soup2_2_1 = BeautifulSoup(page2_2_1.content, 'html.parser', from_encoding="iso-8859-1")
        page2_2_2 = requests.get(links2_2_2)
        soup2_2_2 = BeautifulSoup(page2_2_2.content, 'html.parser', from_encoding="iso-8859-1")

        #2 sub-links derived from the 3nd link 
        page3_1 = requests.get(links3_1)
        soup3_1 = BeautifulSoup(page3_1.content, 'html.parser', from_encoding="iso-8859-1")
        page3_2 = requests.get(links3_2)
        soup3_2 = BeautifulSoup(page3_2.content, 'html.parser', from_encoding="iso-8859-1")

        links3_1_1, links3_1_2 = get_link(soup3_1)
        links3_2_1, links3_2_2 = get_link(soup3_2)

        #4 sub-links derived from the 3.1 link
        page3_1_1 = requests.get(links3_1_1)
        soup3_1_1 = BeautifulSoup(page3_1_1.content, 'html.parser', from_encoding="iso-8859-1")
        page3_1_2 = requests.get(links3_1_2)
        soup3_1_2 = BeautifulSoup(page3_1_2.content, 'html.parser', from_encoding="iso-8859-1")

        #4 sub-links derived from the 3.2 link
        page3_2_1 = requests.get(links3_2_1)
        soup3_2_1 = BeautifulSoup(page3_2_1.content, 'html.parser', from_encoding="iso-8859-1")
        page3_2_2 = requests.get(links3_2_2)
        soup3_2_2 = BeautifulSoup(page3_2_2.content, 'html.parser', from_encoding="iso-8859-1")
        
        #2 sub-links derived from the 4nd link 
        page4_1 = requests.get(links4_1)
        soup4_1 = BeautifulSoup(page4_1.content, 'html.parser', from_encoding="iso-8859-1")
        page4_2 = requests.get(links4_2)
        soup4_2 = BeautifulSoup(page4_2.content, 'html.parser', from_encoding="iso-8859-1")

        links4_1_1, links4_1_2 = get_link(soup4_1)
        links4_2_1, links4_2_2 = get_link(soup4_2)

        #4 sub-links derived from the 4.1 link
        page4_1_1 = requests.get(links4_1_1)
        soup4_1_1 = BeautifulSoup(page4_1_1.content, 'html.parser', from_encoding="iso-8859-1")
        page4_1_2 = requests.get(links4_1_2)
        soup4_1_2 = BeautifulSoup(page4_1_2.content, 'html.parser', from_encoding="iso-8859-1")

        #4 sub-links derived from the 4.2 link
        page4_2_1 = requests.get(links4_2_1)
        soup4_2_1 = BeautifulSoup(page4_2_1.content, 'html.parser', from_encoding="iso-8859-1")
        page4_2_2 = requests.get(links4_2_2)
        soup4_2_2 = BeautifulSoup(page4_2_2.content, 'html.parser', from_encoding="iso-8859-1")

        url2 = 'https://en.wikipedia.org/wiki/Earth'
        url3 = 'https://en.wikipedia.org/wiki/Venus'
        url4 = 'https://en.wikipedia.org/wiki/Jupiter'

        text_string = soup.get_text()
        
        #link set getting text
        text_string2 = soup2.get_text()
        text_string3 = soup3.get_text()
        text_string4 = soup4.get_text() 
        #link set getting text

        #sub-link set getting text
        text_string2_1 = soup2_1.get_text()
        text_string2_2 = soup2_2.get_text()
        text_string3_1 = soup3_1.get_text()
        text_string3_2 = soup3_2.get_text()
        text_string4_1 = soup4_1.get_text()
        text_string4_2 = soup4_2.get_text()
        #sub-link set getting text

        #sub-link set getting text
        text_string2_1_1 = soup2_1_1.get_text()
        text_string2_1_2 = soup2_1_2.get_text()
        text_string2_2_1 = soup2_2_1.get_text()
        text_string2_2_2 = soup2_2_2.get_text()

        text_string3_1_1 = soup3_1_1.get_text()
        text_string3_1_2 = soup3_1_2.get_text()
        text_string3_2_1 = soup3_2_1.get_text()
        text_string3_2_2 = soup3_2_2.get_text()
        
        text_string4_1_1 = soup4_1_1.get_text()
        text_string4_1_2 = soup4_1_2.get_text()
        text_string4_2_1 = soup4_2_1.get_text()
        text_string4_2_2 = soup4_2_2.get_text()
        #sub-link set getting text

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)

        #3-15 letter limitation 
        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        match_pattern2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1)
        match_pattern2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2)

        match_pattern3 = re.findall(r'\b[a-z]{3,15}\b', text_string3)
        match_pattern3_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1)
        match_pattern3_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2)

        match_pattern4 = re.findall(r'\b[a-z]{3,15}\b', text_string4)
        match_pattern4_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1)
        match_pattern4_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2)

        match_pattern2_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1_1)
        match_pattern2_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1_2)
        match_pattern2_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2_1)
        match_pattern2_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2_2)

        match_pattern3_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1_1)
        match_pattern3_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1_2)
        match_pattern3_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2_1)
        match_pattern3_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2_2)

        match_pattern4_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1_1)
        match_pattern4_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1_2)
        match_pattern4_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2_1)
        match_pattern4_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2_2)
        #3-15 letter limitation 

        frequency = {}

        frequency2 = {} 
        frequency3 = {}
        frequency4 = {}
        
        frequency2_1 = {}
        frequency2_2 = {}
        frequency3_1 = {}
        frequency3_2 = {}
        frequency4_1 = {}
        frequency4_2 = {}

        frequency2_1_1 = {}
        frequency2_1_2 = {}
        frequency2_2_1 = {}
        frequency2_2_2 = {}

        frequency3_1_1 = {}
        frequency3_1_2 = {}
        frequency3_2_1 = {}
        frequency3_2_2 = {}

        frequency4_1_1 = {}
        frequency4_1_2 = {}
        frequency4_2_1 = {}
        frequency4_2_2 = {}


        #Finding frequencies in their texts
        frequency = finding_frequency(match_pattern)

        frequency2 = finding_frequency(match_pattern2)
        frequency2_1 = finding_frequency(match_pattern2_1)
        frequency2_2 = finding_frequency(match_pattern2_2)

        frequency3 = finding_frequency(match_pattern3)
        frequency3_1 = finding_frequency(match_pattern3_1)
        frequency3_2 = finding_frequency(match_pattern3_2)

        frequency4 = finding_frequency(match_pattern4)
        frequency4_1 = finding_frequency(match_pattern4_1)
        frequency4_2 = finding_frequency(match_pattern4_2)

        frequency2_1_1 = finding_frequency(match_pattern2_1_1)
        frequency2_1_2 = finding_frequency(match_pattern2_1_2)
        frequency2_2_1 = finding_frequency(match_pattern2_2_1)
        frequency2_2_2 = finding_frequency(match_pattern2_2_2)

        frequency3_1_1 = finding_frequency(match_pattern3_1_1)
        frequency3_1_2 = finding_frequency(match_pattern3_1_2)
        frequency3_2_1 = finding_frequency(match_pattern3_2_1)
        frequency3_2_2 = finding_frequency(match_pattern3_2_2)

        frequency4_1_1 = finding_frequency(match_pattern4_1_1)
        frequency4_1_2 = finding_frequency(match_pattern4_1_2)
        frequency4_2_1 = finding_frequency(match_pattern4_2_1)
        frequency4_2_2 = finding_frequency(match_pattern4_2_2)
        #Finding frequencies in their texts

        # KeyWords for first link
        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) 

        # Finding the keywords in other links
        common_keys2 = result.keys() & frequency2.keys()

        result_values = set(result)

        frequency2_values = set(frequency2)
        frequency2_1_values = set(frequency2_1)
        frequency2_2_values = set(frequency2_2)

        frequency3_values = set(frequency3)
        frequency3_1_values = set(frequency3_1)
        frequency3_2_values = set(frequency3_2)

        frequency4_values = set(frequency4)
        frequency4_1_values = set(frequency4_1)
        frequency4_2_values = set(frequency4_2)

        frequency2_1_1_values = set(frequency2_1_1)
        frequency2_1_2_values = set(frequency2_1_2)
        frequency2_2_1_values = set(frequency2_2_1)
        frequency2_2_2_values = set(frequency2_2_2)

        frequency3_1_1_values = set(frequency3_1_1)
        frequency3_1_2_values = set(frequency3_1_2)
        frequency3_2_1_values = set(frequency3_2_1)
        frequency3_2_2_values = set(frequency3_2_2)

        frequency4_1_1_values = set(frequency4_1_1)
        frequency4_1_2_values = set(frequency4_1_2)
        frequency4_2_1_values = set(frequency4_2_1)
        frequency4_2_2_values = set(frequency4_2_2)

        #Finding Similarity rates
        similarity_rate_2 = finding_result_sum(result_values, frequency2_values, result, frequency2)
        similarity_rate_2_1 = finding_result_sum(result_values, frequency2_1_values, result, frequency2_1)
        similarity_rate_2_2 = finding_result_sum(result_values, frequency2_2_values, result, frequency2_2)
     
        similarity_rate_3 = finding_result_sum(result_values, frequency3_values, result, frequency3)
        similarity_rate_3_1 = finding_result_sum(result_values, frequency3_1_values, result, frequency3_1)
        similarity_rate_3_2 = finding_result_sum(result_values, frequency3_2_values, result, frequency3_2)

        similarity_rate_4 = finding_result_sum(result_values, frequency4_values, result, frequency4)
        similarity_rate_4_1 = finding_result_sum(result_values, frequency4_1_values, result, frequency4_1)
        similarity_rate_4_2 = finding_result_sum(result_values, frequency4_2_values, result, frequency4_2)

        similarity_rate_2_1_1 = finding_result_sum(result_values, frequency2_1_1_values, result, frequency2_1_1)
        similarity_rate_2_1_2 = finding_result_sum(result_values, frequency2_1_2_values, result, frequency2_1_2)
        similarity_rate_2_2_1 = finding_result_sum(result_values, frequency2_2_1_values, result, frequency2_2_1)
        similarity_rate_2_2_2 = finding_result_sum(result_values, frequency2_2_2_values, result, frequency2_2_2)

        similarity_rate_3_1_1 = finding_result_sum(result_values, frequency3_1_1_values, result, frequency3_1_1)
        similarity_rate_3_1_2 = finding_result_sum(result_values, frequency3_1_2_values, result, frequency3_1_2)
        similarity_rate_3_2_1 = finding_result_sum(result_values, frequency3_2_1_values, result, frequency3_2_1)
        similarity_rate_3_2_2 = finding_result_sum(result_values, frequency3_2_2_values, result, frequency3_2_2)

        similarity_rate_4_1_1 = finding_result_sum(result_values, frequency4_1_1_values, result, frequency4_1_1)
        similarity_rate_4_1_2 = finding_result_sum(result_values, frequency4_1_2_values, result, frequency4_1_2)
        similarity_rate_4_2_1 = finding_result_sum(result_values, frequency4_2_1_values, result, frequency4_2_1)
        similarity_rate_4_2_2 = finding_result_sum(result_values, frequency4_2_2_values, result, frequency4_2_2)
        #Finding Similarity rates

        similarity_rate_sorting_dict = {}

        similarity_rate_sorting_dict[url2] = similarity_rate_2
        similarity_rate_sorting_dict[links2_1] = similarity_rate_2_1
        similarity_rate_sorting_dict[links2_2] = similarity_rate_2_2

        similarity_rate_sorting_dict[url3] = similarity_rate_3
        similarity_rate_sorting_dict[links3_1] = similarity_rate_3_1
        similarity_rate_sorting_dict[links3_2] = similarity_rate_3_2

        similarity_rate_sorting_dict[url4] = similarity_rate_4
        similarity_rate_sorting_dict[links4_1] = similarity_rate_4_1
        similarity_rate_sorting_dict[links4_2] = similarity_rate_4_2

        similarity_rate_sorting_dict[links2_1_1] = similarity_rate_2_1_1
        similarity_rate_sorting_dict[links2_1_2] = similarity_rate_2_1_2
        similarity_rate_sorting_dict[links2_2_1] = similarity_rate_2_2_1
        similarity_rate_sorting_dict[links2_2_2] = similarity_rate_2_2_2

        similarity_rate_sorting_dict[links3_1_1] = similarity_rate_3_1_1
        similarity_rate_sorting_dict[links3_1_2] = similarity_rate_3_1_2
        similarity_rate_sorting_dict[links3_2_1] = similarity_rate_3_2_1
        similarity_rate_sorting_dict[links3_2_2] = similarity_rate_3_2_2

        similarity_rate_sorting_dict[links4_1_1] = similarity_rate_4_1_1
        similarity_rate_sorting_dict[links4_1_2] = similarity_rate_4_1_2
        similarity_rate_sorting_dict[links4_2_1] = similarity_rate_4_2_1
        similarity_rate_sorting_dict[links4_2_2] = similarity_rate_4_2_2

        similarity_overall_2 = (similarity_rate_2 + similarity_rate_2_1 + similarity_rate_2_2 + similarity_rate_2_1_1 + similarity_rate_2_1_2 + similarity_rate_2_2_1 + similarity_rate_2_2_2)/7
        similarity_overall_3 = (similarity_rate_3 + similarity_rate_3_1 + similarity_rate_3_2 + similarity_rate_3_1_1 + similarity_rate_3_1_2 + similarity_rate_3_2_1 + similarity_rate_3_2_2)/7
        similarity_overall_4 = (similarity_rate_4 + similarity_rate_4_1 + similarity_rate_4_2 + similarity_rate_4_1_1 + similarity_rate_4_1_2 + similarity_rate_4_2_1 + similarity_rate_4_2_2)/7

        similarity_overall = {}

        similarity_overall[url2] = similarity_overall_2
        similarity_overall[url3] = similarity_overall_3
        similarity_overall[url4] = similarity_overall_4

        tree2 = (
        "\n~" + str(url2) + " %" + str(similarity_rate_2) + "\n   ~" + str(links2_1) + " %" + str(similarity_rate_2_1) + "\n   ~" + str(links2_2)
        + " %" + str(similarity_rate_2_2) + "\n      ~"+ str(links2_1_1) + " %" + str(similarity_rate_2_1_1) + "\n      ~" + str(links2_1_2) + " %" + str(similarity_rate_2_1_2)
        + "\n      ~" + str(links2_2_1) + " %" + str(similarity_rate_2_2_1) + "\n      ~"+ str(links2_2_2) + " %" + str(similarity_rate_2_2_2)
        )

        tree3 = (
        "\n~" + str(url3) + " %" + str(similarity_rate_3) + "\n   ~" + str(links3_1) + " %" + str(similarity_rate_3_1) + "\n   ~" + str(links3_2)
        + " %" + str(similarity_rate_3_2) + "\n      ~"+ str(links3_1_1) + " %" + str(similarity_rate_3_1_1) + "\n      ~" + str(links3_1_2) + " %" + str(similarity_rate_3_1_2)
        + "\n      ~" + str(links3_2_1) + " %" + str(similarity_rate_3_2_1) + "\n      ~"+ str(links3_2_2) + " %" + str(similarity_rate_3_2_2)
        )

        tree4 = (
        "\n~" + str(url4) + " %" + str(similarity_rate_4) + "\n   ~" + str(links4_1) + " %" + str(similarity_rate_4_1) + "\n   ~" + str(links4_2)
        + " %" + str(similarity_rate_4_2) + "\n      ~"+ str(links4_1_1) + " %" + str(similarity_rate_4_1_1) + "\n      ~" + str(links4_1_2) + " %" + str(similarity_rate_4_1_2)
        + "\n      ~" + str(links4_2_1) + " %" + str(similarity_rate_4_2_1) + "\n      ~"+ str(links4_2_2) + " %" + str(similarity_rate_4_2_2)
        )

        if(similarity_rate_2 > similarity_rate_3 > similarity_rate_4):
            main_tree = "\n\n\n" + tree2 + "\n\n\n" + tree3 + "\n\n\n" + tree4
        elif(similarity_rate_2 > similarity_rate_4 > similarity_rate_3):
            main_tree = "\n\n\n" + tree2 + "\n\n\n" + tree4 + "\n\n\n" + tree3
        elif(similarity_rate_3 > similarity_rate_4 > similarity_rate_2):
            main_tree = "\n\n\n" + tree3 + "\n\n\n" + tree4 + "\n\n\n" + tree2
        elif(similarity_rate_3 > similarity_rate_2 > similarity_rate_4):
            main_tree = "\n\n\n" + tree3 + "\n\n\n" + tree2 + "\n\n\n" + tree4
        elif(similarity_rate_4 > similarity_rate_2 > similarity_rate_3):
            main_tree = "\n\n\n" + tree4 + "\n\n\n" + tree2 + "\n\n\n" + tree3
        elif(similarity_rate_4 > similarity_rate_3 > similarity_rate_2):
            main_tree = "\n\n\n" + tree4 + "\n\n\n" + tree3 + "\n\n\n" + tree2
       
        sorted_overall_dict = sorted(similarity_overall.items(), key=operator.itemgetter(1), reverse=True)

        total_string = ""
        for key, value in sorted(similarity_overall.items(), key=operator.itemgetter(1), reverse=True):
            total_string = total_string + "   ~{}: {}".format(key, value) + "\n"

        total_string2 = "Average Similarities" + "\n" + total_string

        return render_template("index4.html", title="Indexing", content = total_string2 + main_tree)
    else:
        return render_template("index4.html", title="Indexing")

@app.route("/Semantic", methods=["POST", "GET"])
def Semantic():
    if request.method == "POST":
        url = request.form["url"]

        page = requests.get(url)

        page2 = requests.get('https://en.wikipedia.org/wiki/Earth')
        page3 = requests.get('https://en.wikipedia.org/wiki/Venus')
        page4 = requests.get('https://en.wikipedia.org/wiki/Jupiter')
        
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")

        soup2 = BeautifulSoup(page2.content, 'html.parser',from_encoding="iso-8859-1")
        soup3 = BeautifulSoup(page3.content, 'html.parser',from_encoding="iso-8859-1")
        soup4 = BeautifulSoup(page4.content, 'html.parser',from_encoding="iso-8859-1")

        links2_1, links2_2 = get_link(soup2)
        links3_1, links3_2 = get_link(soup3)
        links4_1, links4_2 = get_link(soup4)

        #2 sub-links derived from the 2nd link 
        page2_1 = requests.get(links2_1)
        soup2_1 = BeautifulSoup(page2_1.content, 'html.parser',from_encoding="iso-8859-1")
        page2_2 = requests.get(links2_2)
        soup2_2 = BeautifulSoup(page2_2.content, 'html.parser',from_encoding="iso-8859-1")

        links2_1_1, links2_1_2 = get_link(soup2_1)
        links2_2_1, links2_2_2 = get_link(soup2_2)

        #4 sub-links derived from the 2.1 link
        page2_1_1 = requests.get(links2_1_1)
        soup2_1_1 = BeautifulSoup(page2_1_1.content, 'html.parser',from_encoding="iso-8859-1")
        page2_1_2 = requests.get(links2_1_2)
        soup2_1_2 = BeautifulSoup(page2_1_2.content, 'html.parser',from_encoding="iso-8859-1")

        #4 sub-links derived from the 2.2 link
        page2_2_1 = requests.get(links2_2_1)
        soup2_2_1 = BeautifulSoup(page2_2_1.content, 'html.parser',from_encoding="iso-8859-1")
        page2_2_2 = requests.get(links2_2_2)
        soup2_2_2 = BeautifulSoup(page2_2_2.content, 'html.parser',from_encoding="iso-8859-1")

        #2 sub-links derived from the 3nd link 
        page3_1 = requests.get(links3_1)
        soup3_1 = BeautifulSoup(page3_1.content, 'html.parser',from_encoding="iso-8859-1")
        page3_2 = requests.get(links3_2)
        soup3_2 = BeautifulSoup(page3_2.content, 'html.parser',from_encoding="iso-8859-1")

        links3_1_1, links3_1_2 = get_link(soup3_1)
        links3_2_1, links3_2_2 = get_link(soup3_2)

        #4 sub-links derived from the 3.1 link
        page3_1_1 = requests.get(links3_1_1)
        soup3_1_1 = BeautifulSoup(page3_1_1.content, 'html.parser',from_encoding="iso-8859-1")
        page3_1_2 = requests.get(links3_1_2)
        soup3_1_2 = BeautifulSoup(page3_1_2.content, 'html.parser',from_encoding="iso-8859-1")

        #4 sub-links derived from the 3.2 link
        page3_2_1 = requests.get(links3_2_1)
        soup3_2_1 = BeautifulSoup(page3_2_1.content, 'html.parser',from_encoding="iso-8859-1")
        page3_2_2 = requests.get(links3_2_2)
        soup3_2_2 = BeautifulSoup(page3_2_2.content, 'html.parser',from_encoding="iso-8859-1")
        
        #2 sub-links derived from the 4nd link 
        page4_1 = requests.get(links4_1)
        soup4_1 = BeautifulSoup(page4_1.content, 'html.parser',from_encoding="iso-8859-1")
        page4_2 = requests.get(links4_2)
        soup4_2 = BeautifulSoup(page4_2.content, 'html.parser',from_encoding="iso-8859-1")

        links4_1_1, links4_1_2 = get_link(soup4_1)
        links4_2_1, links4_2_2 = get_link(soup4_2)

        #4 sub-links derived from the 4.1 link
        page4_1_1 = requests.get(links4_1_1)
        soup4_1_1 = BeautifulSoup(page4_1_1.content, 'html.parser',from_encoding="iso-8859-1")
        page4_1_2 = requests.get(links4_1_2)
        soup4_1_2 = BeautifulSoup(page4_1_2.content, 'html.parser',from_encoding="iso-8859-1")

        #4 sub-links derived from the 4.2 link
        page4_2_1 = requests.get(links4_2_1)
        soup4_2_1 = BeautifulSoup(page4_2_1.content, 'html.parser',from_encoding="iso-8859-1")
        page4_2_2 = requests.get(links4_2_2)
        soup4_2_2 = BeautifulSoup(page4_2_2.content, 'html.parser',from_encoding="iso-8859-1")

        url2 = 'https://en.wikipedia.org/wiki/Earth'
        url3 = 'https://en.wikipedia.org/wiki/Venus'
        url4 = 'https://en.wikipedia.org/wiki/Jupiter'

        text_string = soup.get_text()
        
        #link set getting text
        text_string2 = soup2.get_text()
        text_string3 = soup3.get_text()
        text_string4 = soup4.get_text() 
        #link set getting text

        #sub-link set getting text
        text_string2_1 = soup2_1.get_text()
        text_string2_2 = soup2_2.get_text()
        text_string3_1 = soup3_1.get_text()
        text_string3_2 = soup3_2.get_text()
        text_string4_1 = soup4_1.get_text()
        text_string4_2 = soup4_2.get_text()
        #sub-link set getting text

        #sub-link set getting text
        text_string2_1_1 = soup2_1_1.get_text()
        text_string2_1_2 = soup2_1_2.get_text()
        text_string2_2_1 = soup2_2_1.get_text()
        text_string2_2_2 = soup2_2_2.get_text()

        text_string3_1_1 = soup3_1_1.get_text()
        text_string3_1_2 = soup3_1_2.get_text()
        text_string3_2_1 = soup3_2_1.get_text()
        text_string3_2_2 = soup3_2_2.get_text()
        
        text_string4_1_1 = soup4_1_1.get_text()
        text_string4_1_2 = soup4_1_2.get_text()
        text_string4_2_1 = soup4_2_1.get_text()
        text_string4_2_2 = soup4_2_2.get_text()
        #sub-link set getting text

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)

        #3-15 letter limitation 
        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        match_pattern2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1)
        match_pattern2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2)

        match_pattern3 = re.findall(r'\b[a-z]{3,15}\b', text_string3)
        match_pattern3_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1)
        match_pattern3_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2)

        match_pattern4 = re.findall(r'\b[a-z]{3,15}\b', text_string4)
        match_pattern4_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1)
        match_pattern4_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2)

        match_pattern2_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1_1)
        match_pattern2_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_1_2)
        match_pattern2_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2_1)
        match_pattern2_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2_2)

        match_pattern3_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1_1)
        match_pattern3_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_1_2)
        match_pattern3_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2_1)
        match_pattern3_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2_2)

        match_pattern4_1_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1_1)
        match_pattern4_1_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_1_2)
        match_pattern4_2_1 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2_1)
        match_pattern4_2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2_2)
        #3-15 letter limitation 

        frequency = {}

        frequency2 = {} 
        frequency3 = {}
        frequency4 = {}
        
        frequency2_1 = {}
        frequency2_2 = {}
        frequency3_1 = {}
        frequency3_2 = {}
        frequency4_1 = {}
        frequency4_2 = {}

        frequency2_1_1 = {}
        frequency2_1_2 = {}
        frequency2_2_1 = {}
        frequency2_2_2 = {}

        frequency3_1_1 = {}
        frequency3_1_2 = {}
        frequency3_2_1 = {}
        frequency3_2_2 = {}

        frequency4_1_1 = {}
        frequency4_1_2 = {}
        frequency4_2_1 = {}
        frequency4_2_2 = {}


        #Finding frequencies in their texts
        frequency = finding_frequency(match_pattern)

        frequency2 = finding_frequency(match_pattern2)
        frequency2_1 = finding_frequency(match_pattern2_1)
        frequency2_2 = finding_frequency(match_pattern2_2)

        frequency3 = finding_frequency(match_pattern3)
        frequency3_1 = finding_frequency(match_pattern3_1)
        frequency3_2 = finding_frequency(match_pattern3_2)

        frequency4 = finding_frequency(match_pattern4)
        frequency4_1 = finding_frequency(match_pattern4_1)
        frequency4_2 = finding_frequency(match_pattern4_2)

        frequency2_1_1 = finding_frequency(match_pattern2_1_1)
        frequency2_1_2 = finding_frequency(match_pattern2_1_2)
        frequency2_2_1 = finding_frequency(match_pattern2_2_1)
        frequency2_2_2 = finding_frequency(match_pattern2_2_2)

        frequency3_1_1 = finding_frequency(match_pattern3_1_1)
        frequency3_1_2 = finding_frequency(match_pattern3_1_2)
        frequency3_2_1 = finding_frequency(match_pattern3_2_1)
        frequency3_2_2 = finding_frequency(match_pattern3_2_2)

        frequency4_1_1 = finding_frequency(match_pattern4_1_1)
        frequency4_1_2 = finding_frequency(match_pattern4_1_2)
        frequency4_2_1 = finding_frequency(match_pattern4_2_1)
        frequency4_2_2 = finding_frequency(match_pattern4_2_2)
        #Finding frequencies in their texts

        # KeyWords for first link
        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6])

        keywordlist = []

        for key in result.keys():
            keywordlist.append(key)

        i = 0
        synonmys = []
        synonmys2 = []

        # Finding Synonmys words in result dict
        for i in range(len(result)):
            for syn in wordnet.synsets(keywordlist[i]):
                for lemma in syn.lemmas():
                    synonmys.append(lemma.name())
            if(len(synonmys) > 1):
                synonmys2.append(synonmys[1])
                synonmys.clear()
            elif(len(synonmys) == 1):
                synonmys2.append(synonmys[0])
                synonmys.clear()
            else:
                synonmys.clear()

        # Add synonmys word to result dict
        for i in range(len(synonmys2)):
            result[synonmys2[i]] = text_string.count(synonmys2[i])

        # Finding the keywords in other links
        common_keys2 = result.keys() & frequency2.keys()

        result_values = set(result)

        frequency2_values = set(frequency2)
        frequency2_1_values = set(frequency2_1)
        frequency2_2_values = set(frequency2_2)

        frequency3_values = set(frequency3)
        frequency3_1_values = set(frequency3_1)
        frequency3_2_values = set(frequency3_2)

        frequency4_values = set(frequency4)
        frequency4_1_values = set(frequency4_1)
        frequency4_2_values = set(frequency4_2)

        frequency2_1_1_values = set(frequency2_1_1)
        frequency2_1_2_values = set(frequency2_1_2)
        frequency2_2_1_values = set(frequency2_2_1)
        frequency2_2_2_values = set(frequency2_2_2)

        frequency3_1_1_values = set(frequency3_1_1)
        frequency3_1_2_values = set(frequency3_1_2)
        frequency3_2_1_values = set(frequency3_2_1)
        frequency3_2_2_values = set(frequency3_2_2)

        frequency4_1_1_values = set(frequency4_1_1)
        frequency4_1_2_values = set(frequency4_1_2)
        frequency4_2_1_values = set(frequency4_2_1)
        frequency4_2_2_values = set(frequency4_2_2)

        #Finding Similarity rates
        similarity_rate_2 = finding_result_sum(result_values, frequency2_values, result, frequency2)
        similarity_rate_2_1 = finding_result_sum(result_values, frequency2_1_values, result, frequency2_1)
        similarity_rate_2_2 = finding_result_sum(result_values, frequency2_2_values, result, frequency2_2)
     
        similarity_rate_3 = finding_result_sum(result_values, frequency3_values, result, frequency3)
        similarity_rate_3_1 = finding_result_sum(result_values, frequency3_1_values, result, frequency3_1)
        similarity_rate_3_2 = finding_result_sum(result_values, frequency3_2_values, result, frequency3_2)

        similarity_rate_4 = finding_result_sum(result_values, frequency4_values, result, frequency4)
        similarity_rate_4_1 = finding_result_sum(result_values, frequency4_1_values, result, frequency4_1)
        similarity_rate_4_2 = finding_result_sum(result_values, frequency4_2_values, result, frequency4_2)

        similarity_rate_2_1_1 = finding_result_sum(result_values, frequency2_1_1_values, result, frequency2_1_1)
        similarity_rate_2_1_2 = finding_result_sum(result_values, frequency2_1_2_values, result, frequency2_1_2)
        similarity_rate_2_2_1 = finding_result_sum(result_values, frequency2_2_1_values, result, frequency2_2_1)
        similarity_rate_2_2_2 = finding_result_sum(result_values, frequency2_2_2_values, result, frequency2_2_2)

        similarity_rate_3_1_1 = finding_result_sum(result_values, frequency3_1_1_values, result, frequency3_1_1)
        similarity_rate_3_1_2 = finding_result_sum(result_values, frequency3_1_2_values, result, frequency3_1_2)
        similarity_rate_3_2_1 = finding_result_sum(result_values, frequency3_2_1_values, result, frequency3_2_1)
        similarity_rate_3_2_2 = finding_result_sum(result_values, frequency3_2_2_values, result, frequency3_2_2)

        similarity_rate_4_1_1 = finding_result_sum(result_values, frequency4_1_1_values, result, frequency4_1_1)
        similarity_rate_4_1_2 = finding_result_sum(result_values, frequency4_1_2_values, result, frequency4_1_2)
        similarity_rate_4_2_1 = finding_result_sum(result_values, frequency4_2_1_values, result, frequency4_2_1)
        similarity_rate_4_2_2 = finding_result_sum(result_values, frequency4_2_2_values, result, frequency4_2_2)
        #Finding Similarity rates

        similarity_rate_sorting_dict = {}

        similarity_rate_sorting_dict[url2] = similarity_rate_2
        similarity_rate_sorting_dict[links2_1] = similarity_rate_2_1
        similarity_rate_sorting_dict[links2_2] = similarity_rate_2_2

        similarity_rate_sorting_dict[url3] = similarity_rate_3
        similarity_rate_sorting_dict[links3_1] = similarity_rate_3_1
        similarity_rate_sorting_dict[links3_2] = similarity_rate_3_2

        similarity_rate_sorting_dict[url4] = similarity_rate_4
        similarity_rate_sorting_dict[links4_1] = similarity_rate_4_1
        similarity_rate_sorting_dict[links4_2] = similarity_rate_4_2

        similarity_rate_sorting_dict[links2_1_1] = similarity_rate_2_1_1
        similarity_rate_sorting_dict[links2_1_2] = similarity_rate_2_1_2
        similarity_rate_sorting_dict[links2_2_1] = similarity_rate_2_2_1
        similarity_rate_sorting_dict[links2_2_2] = similarity_rate_2_2_2

        similarity_rate_sorting_dict[links3_1_1] = similarity_rate_3_1_1
        similarity_rate_sorting_dict[links3_1_2] = similarity_rate_3_1_2
        similarity_rate_sorting_dict[links3_2_1] = similarity_rate_3_2_1
        similarity_rate_sorting_dict[links3_2_2] = similarity_rate_3_2_2

        similarity_rate_sorting_dict[links4_1_1] = similarity_rate_4_1_1
        similarity_rate_sorting_dict[links4_1_2] = similarity_rate_4_1_2
        similarity_rate_sorting_dict[links4_2_1] = similarity_rate_4_2_1
        similarity_rate_sorting_dict[links4_2_2] = similarity_rate_4_2_2

        similarity_overall_2 = (similarity_rate_2 + similarity_rate_2_1 + similarity_rate_2_2 + similarity_rate_2_1_1 + similarity_rate_2_1_2 + similarity_rate_2_2_1 + similarity_rate_2_2_2)/7
        similarity_overall_3 = (similarity_rate_3 + similarity_rate_3_1 + similarity_rate_3_2 + similarity_rate_3_1_1 + similarity_rate_3_1_2 + similarity_rate_3_2_1 + similarity_rate_3_2_2)/7
        similarity_overall_4 = (similarity_rate_4 + similarity_rate_4_1 + similarity_rate_4_2 + similarity_rate_4_1_1 + similarity_rate_4_1_2 + similarity_rate_4_2_1 + similarity_rate_4_2_2)/7

        similarity_overall = {}

        similarity_overall[url2] = similarity_overall_2
        similarity_overall[url3] = similarity_overall_3
        similarity_overall[url4] = similarity_overall_4

        tree2 = (
        "\n~" + str(url2) + " %" + str(similarity_rate_2) + "\n   ~" + str(links2_1) + " %" + str(similarity_rate_2_1) + "\n   ~" + str(links2_2)
        + " %" + str(similarity_rate_2_2) + "\n      ~"+ str(links2_1_1) + " %" + str(similarity_rate_2_1_1) + "\n      ~" + str(links2_1_2) + " %" + str(similarity_rate_2_1_2)
        + "\n      ~" + str(links2_2_1) + " %" + str(similarity_rate_2_2_1) + "\n      ~"+ str(links2_2_2) + " %" + str(similarity_rate_2_2_2)
        )

        tree3 = (
        "\n~" + str(url3) + " %" + str(similarity_rate_3) + "\n   ~" + str(links3_1) + " %" + str(similarity_rate_3_1) + "\n   ~" + str(links3_2)
        + " %" + str(similarity_rate_3_2) + "\n      ~"+ str(links3_1_1) + " %" + str(similarity_rate_3_1_1) + "\n      ~" + str(links3_1_2) + " %" + str(similarity_rate_3_1_2)
        + "\n      ~" + str(links3_2_1) + " %" + str(similarity_rate_3_2_1) + "\n      ~"+ str(links3_2_2) + " %" + str(similarity_rate_3_2_2)
        )

        tree4 = (
        "\n~" + str(url4) + " %" + str(similarity_rate_4) + "\n   ~" + str(links4_1) + " %" + str(similarity_rate_4_1) + "\n   ~" + str(links4_2)
        + " %" + str(similarity_rate_4_2) + "\n      ~"+ str(links4_1_1) + " %" + str(similarity_rate_4_1_1) + "\n      ~" + str(links4_1_2) + " %" + str(similarity_rate_4_1_2)
        + "\n      ~" + str(links4_2_1) + " %" + str(similarity_rate_4_2_1) + "\n      ~"+ str(links4_2_2) + " %" + str(similarity_rate_4_2_2)
        )

        if(similarity_rate_2 > similarity_rate_3 > similarity_rate_4):
            main_tree = "\n\n\n" + tree2 + "\n\n\n" + tree3 + "\n\n\n" + tree4
        elif(similarity_rate_2 > similarity_rate_4 > similarity_rate_3):
            main_tree = "\n\n\n" + tree2 + "\n\n\n" + tree4 + "\n\n\n" + tree3
        elif(similarity_rate_3 > similarity_rate_4 > similarity_rate_2):
            main_tree = "\n\n\n" + tree3 + "\n\n\n" + tree4 + "\n\n\n" + tree2
        elif(similarity_rate_3 > similarity_rate_2 > similarity_rate_4):
            main_tree = "\n\n\n" + tree3 + "\n\n\n" + tree2 + "\n\n\n" + tree4
        elif(similarity_rate_4 > similarity_rate_2 > similarity_rate_3):
            main_tree = "\n\n\n" + tree4 + "\n\n\n" + tree2 + "\n\n\n" + tree3
        elif(similarity_rate_4 > similarity_rate_3 > similarity_rate_2):
            main_tree = "\n\n\n" + tree4 + "\n\n\n" + tree3 + "\n\n\n" + tree2
       
        sorted_overall_dict = sorted(similarity_overall.items(), key=operator.itemgetter(1), reverse=True)

        total_string = ""
        for key, value in sorted(similarity_overall.items(), key=operator.itemgetter(1), reverse=True):
            total_string = total_string + "   ~{}: {}".format(key, value) + "\n"

        total_string2 = "Average Similarities" + "\n" + total_string

        return render_template("index5.html", title="Semantic", content = total_string2 + main_tree)
    else:
        return render_template("index5.html", title="Semantic")

if __name__ == "__main__":
    app.run()