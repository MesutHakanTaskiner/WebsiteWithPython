from flask import Flask, redirect, url_for, render_template, Flask, request
import requests
from bs4 import BeautifulSoup
import re
import json
from operator import itemgetter
import operator

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

@app.route("/Indexing", methods=["POST", "GET"])
def view_fourth_page():
    if request.method == "POST":
        url = request.form["url"]

        page = requests.get(url)
        page2 = requests.get('https://en.wikipedia.org/wiki/Mustafa_Kemal_Atat%C3%BCrk')
        page3 = requests.get('https://en.wikipedia.org/wiki/%C4%B0smet_%C4%B0n%C3%B6n%C3%BC')
        page4 = requests.get('https://en.wikipedia.org/wiki/K%C3%A2z%C4%B1m_Karabekir')
        page5 = requests.get('https://en.wikipedia.org/wiki/Mehmed_the_Conqueror')
        
        soup = BeautifulSoup(page.content, 'html.parser')
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        soup3 = BeautifulSoup(page3.content, 'html.parser')
        soup4 = BeautifulSoup(page4.content, 'html.parser')
        soup5 = BeautifulSoup(page5.content, 'html.parser')

        url2 = 'https://en.wikipedia.org/wiki/Mustafa_Kemal_Atat%C3%BCrk'
        url3 = 'https://en.wikipedia.org/wiki/%C4%B0smet_%C4%B0n%C3%B6n%C3%BC'
        url4 = 'https://en.wikipedia.org/wiki/K%C3%A2z%C4%B1m_Karabekir'
        url5 = 'https://en.wikipedia.org/wiki/Mehmed_the_Conqueror'

        text_string = soup.get_text()
        text_string2 = soup2.get_text()
        text_string3 = soup3.get_text()
        text_string4 = soup4.get_text()
        text_string5 = soup5.get_text()

        frequency = {}
        frequency2 = {}
        frequency3 = {}
        frequency4 = {}
        frequency5 = {}

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)
        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        match_pattern3 = re.findall(r'\b[a-z]{3,15}\b', text_string3)
        match_pattern4 = re.findall(r'\b[a-z]{3,15}\b', text_string4)
        match_pattern5 = re.findall(r'\b[a-z]{3,15}\b', text_string5)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1

        for word in match_pattern2:
            count2 = frequency2.get(word,0)
            frequency2[word] = count2 + 1

        for word in match_pattern3:
            count3 = frequency3.get(word,0)
            frequency3[word] = count3 + 1

        for word in match_pattern4:
            count4 = frequency4.get(word,0)
            frequency4[word] = count4 + 1

        for word in match_pattern5:
            count5 = frequency5.get(word,0)
            frequency5[word] = count5 + 1

        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) # KeyWords for first link

        common_keys2 = result.keys() & frequency2.keys() # Finding the keywords in other links
        common_keys3 = result.keys() & frequency3.keys() # Finding the keywords in other links
        common_keys4 = result.keys() & frequency4.keys() # Finding the keywords in other links
        common_keys5 = result.keys() & frequency5.keys() # Finding the keywords in other links

        sum_result2 = 0
        sum_frequency2 = 0

        sum_result3 = 0
        sum_frequency3 = 0

        sum_result4 = 0
        sum_frequency4 = 0

        sum_result5 = 0
        sum_frequency5 = 0

        frequency2_total = {}
        frequency3_total = {}
        frequency4_total = {}
        frequency5_total = {}

        result_values = set(result)
        frequency2_values = set(frequency2)
        frequency3_values = set(frequency3)
        frequency4_values = set(frequency4)
        frequency5_values = set(frequency5)

        for name2 in result_values.intersection(frequency2_values):
            sum_result2 = sum_result2 + result[name2]
            sum_frequency2 = sum_frequency2 + frequency2[name2]
            frequency2_total[name2] = frequency2[name2]

        for name3 in result_values.intersection(frequency3_values):
            sum_result3 = sum_result3 + result[name3]
            sum_frequency3 = sum_frequency3 + frequency3[name3]
            frequency4_total[name3] = frequency3[name3]

        for name4 in result_values.intersection(frequency4_values):
            sum_result4 = sum_result4 + result[name4]
            sum_frequency4 = sum_frequency4 + frequency4[name4]
            frequency4_total[name4] = frequency4[name4]

        for name5 in result_values.intersection(frequency5_values):
            sum_result5 = sum_result5 + result[name5]
            sum_frequency5 = sum_frequency5 + frequency5[name5]
            frequency5_total[name5] = frequency5[name5]

        str_frequency2_total = str(frequency2_total)
        str_frequency3_total = str(frequency3_total)
        str_frequency4_total = str(frequency4_total)
        str_frequency5_total = str(frequency5_total)

        try:
            similarity2 = ((sum_result2/sum_frequency2)*100)
            if(similarity2 > 100):
                similarity2 = ((sum_frequency2/sum_result2)*100)
        except ZeroDivisionError:
            similarity2 = 0

        try:
            similarity3 = ((sum_result3/sum_frequency3)*100)
            if(similarity3 > 100):
                similarity3 = ((sum_frequency3/sum_result3)*100)
        except ZeroDivisionError:
            similarity3 = 0

        try:
            similarity4 = ((sum_result4/sum_frequency4)*100)
            if(similarity4 > 100):
                similarity4 = ((sum_frequency4/sum_result4)*100)
        except ZeroDivisionError:
            similarity4 = 0

        try:
            similarity5 = ((sum_result5/sum_frequency5)*100)
            if(similarity5 > 100):
                similarity5 = ((sum_frequency5/sum_result5)*100)
        except ZeroDivisionError:
            similarity5 = 0

        if(similarity2 == 0):
            str_similarity2 = "0"
        else:
            str_similarity2 = str(similarity2)

        if(similarity3 == 0):
            str_similarity3 = "0"
        else:
            str_similarity3 = str(similarity3)

        if(similarity4 == 0):
            str_similarity4 = "0"
        else:
            str_similarity4 = str(similarity4)

        if(similarity5 == 0):
            str_similarity5 = "0"
        else:
            str_similarity5 = str(similarity5)
        
        similarity_rate_sorting_dict = {}
        
        similarity_rate_sorting_dict[url2] = similarity2
        similarity_rate_sorting_dict[url3] = similarity3
        similarity_rate_sorting_dict[url4] = similarity4
        similarity_rate_sorting_dict[url5] = similarity5

        sorted_dict = sorted(similarity_rate_sorting_dict.items(), key=operator.itemgetter(1), reverse=True)

        total_string = json.dumps(sorted_dict, indent=1)


        return render_template("index4.html", title="Indexing", content = total_string)
    else:
        return render_template("index4.html", title="Indexing")

@app.route("/Semantic", methods=["POST", "GET"])
def view_fifth_page():
    return render_template("index5.html", title="Semantic")

if __name__ == "__main__":
    app.run()