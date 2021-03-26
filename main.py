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

        links2_2 = []
        links2_3 = []
        links3_2 = []
        links3_3 = []
        links4_2 = []
        links4_3 = []

        page2 = requests.get('https://en.wikipedia.org/wiki/Turkey')
        page3 = requests.get('https://en.wikipedia.org/wiki/Black_hole')
        page4 = requests.get('https://en.wikipedia.org/wiki/International_Space_Station')
        
        soup = BeautifulSoup(page.content, 'html.parser')

        soup2 = BeautifulSoup(page2.content, 'html.parser')
        soup3 = BeautifulSoup(page3.content, 'html.parser')
        soup4 = BeautifulSoup(page4.content, 'html.parser')

        
        for link in soup2.findAll('a', attrs={'href': re.compile("^https://")}):
            links2_2.append(link.get('href'))

        page2_2 = requests.get(links2_2[3])
        soup2_2 = BeautifulSoup(page2_2.content, 'html.parser')

        for link in soup2_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links2_3.append(link.get('href'))

        page2_3 = requests.get(links2_3[1])
        soup2_3 = BeautifulSoup(page2_3.content, 'html.parser')

        for link in soup3.findAll('a', attrs={'href': re.compile("^https://")}):
            links3_2.append(link.get('href'))

        page3_2 = requests.get(links3_2[3])
        soup3_2 = BeautifulSoup(page3_2.content, 'html.parser')

        for link in soup3_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links3_3.append(link.get('href'))

        page3_3 = requests.get(links3_3[1])
        soup3_3 = BeautifulSoup(page3_3.content, 'html.parser')

        for link in soup4.findAll('a', attrs={'href': re.compile("^https://")}):
            links4_2.append(link.get('href'))

        page4_2 = requests.get(links4_2[3])
        soup4_2 = BeautifulSoup(page4_2.content, 'html.parser')

        for link in soup4_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links4_3.append(link.get('href'))

        page4_3 = requests.get(links4_3[1])
        soup4_3 = BeautifulSoup(page4_3.content, 'html.parser')

        url2 = 'https://en.wikipedia.org/wiki/Turkey'
        url2_2 = links2_2[3]
        url2_3 = links2_3[1]

        url3 = 'https://en.wikipedia.org/wiki/Black_hole'
        url3_2 = links3_2[3]
        url3_3 = links3_3[1]

        url4 = 'https://en.wikipedia.org/wiki/International_Space_Station'
        url4_2 = links4_2[3]
        url4_3 = links4_3[1]

        text_string = soup.get_text()

        text_string2 = soup2.get_text()
        text_string2_2 = soup2_2.get_text()
        text_string2_3 = soup2_3.get_text()

        text_string3 = soup3.get_text()
        text_string3_2 = soup3.get_text()
        text_string3_3 = soup3.get_text()

        text_string4 = soup4.get_text()
        text_string4_2 = soup4_2.get_text()
        text_string4_3 = soup4_3.get_text()

        frequency = {}

        frequency2 = {}
        frequency2_2 = {}
        frequency2_3 = {}

        frequency3 = {}
        frequency3_2 = {}
        frequency3_3 = {}

        frequency4 = {}
        frequency4_2 = {}
        frequency4_3 = {}

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)

        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        match_pattern2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2)
        match_pattern2_3 = re.findall(r'\b[a-z]{3,15}\b', text_string2_3)

        match_pattern3 = re.findall(r'\b[a-z]{3,15}\b', text_string3)
        match_pattern3_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2)
        match_pattern3_3 = re.findall(r'\b[a-z]{3,15}\b', text_string3_3)

        match_pattern4 = re.findall(r'\b[a-z]{3,15}\b', text_string4)
        match_pattern4_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2)
        match_pattern4_3 = re.findall(r'\b[a-z]{3,15}\b', text_string4_3)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1

        for word in match_pattern2:
            count2 = frequency2.get(word,0)
            frequency2[word] = count2 + 1
        
        for word in match_pattern2_2:
            count2_2 = frequency2_2.get(word,0)
            frequency2_2[word] = count2_2 + 1
        
        for word in match_pattern2_3:
            count2_3 = frequency2_3.get(word,0)
            frequency2_3[word] = count2_3 + 1

        for word in match_pattern3:
            count3 = frequency3.get(word,0)
            frequency3[word] = count3 + 1

        for word in match_pattern3_2:
            count3_2 = frequency3_2.get(word,0)
            frequency3_2[word] = count3_2 + 1

        for word in match_pattern3_3:
            count3_3 = frequency3_3.get(word,0)
            frequency3_3[word] = count3_3 + 1

        for word in match_pattern4:
            count4 = frequency4.get(word,0)
            frequency4[word] = count4 + 1

        for word in match_pattern4_2:
            count4_2 = frequency4_2.get(word,0)
            frequency4_2[word] = count4_2 + 1

        for word in match_pattern4_3:
            count4_3 = frequency4_3.get(word,0)
            frequency4_3[word] = count4_3 + 1

        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) # KeyWords for first link

        common_keys2 = result.keys() & frequency2.keys() # Finding the keywords in other links
        common_keys2_2 = result.keys() & frequency2_2.keys() # Finding the keywords in other links
        common_keys2_2 = result.keys() & frequency2_3.keys() # Finding the keywords in other links

        common_keys3 = result.keys() & frequency3.keys() # Finding the keywords in other links
        common_keys3_2 = result.keys() & frequency3_2.keys() # Finding the keywords in other links
        common_keys3_3 = result.keys() & frequency3_3.keys() # Finding the keywords in other links

        common_keys4 = result.keys() & frequency4.keys() # Finding the keywords in other links
        common_keys4_2 = result.keys() & frequency4_2.keys() # Finding the keywords in other links
        common_keys4_3 = result.keys() & frequency4_3.keys() # Finding the keywords in other links

        sum_result2 = 0
        sum_frequency2 = 0
        sum_result2_2 = 0
        sum_frequency2_2 = 0
        sum_result2_3= 0
        sum_frequency2_3 = 0

        sum_result3 = 0
        sum_frequency3 = 0
        sum_result3_2 = 0
        sum_frequency3_2 = 0
        sum_result3_3 = 0
        sum_frequency3_3 = 0

        sum_result4 = 0
        sum_frequency4 = 0
        sum_result4_2 = 0
        sum_frequency4_2 = 0
        sum_result4_3 = 0
        sum_frequency4_3 = 0

        frequency2_total = {}
        frequency2_2_total = {}
        frequency2_3_total = {}

        frequency3_total = {}
        frequency3_2_total = {}
        frequency3_3_total = {}

        frequency4_total = {}
        frequency4_2_total = {}
        frequency4_3_total = {}

        result_values = set(result)

        frequency2_values = set(frequency2)
        frequency2_2_values = set(frequency2_2)
        frequency2_3_values = set(frequency2_3)

        frequency3_values = set(frequency3)
        frequency3_2_values = set(frequency3_2)
        frequency3_3_values = set(frequency3_3)

        frequency4_values = set(frequency4)
        frequency4_2_values = set(frequency4_2)
        frequency4_3_values = set(frequency4_3)

        for name2 in result_values.intersection(frequency2_values):
            sum_result2 = sum_result2 + result[name2]
            sum_frequency2 = sum_frequency2 + frequency2[name2]
            frequency2_total[name2] = frequency2[name2]

        for name2_2 in result_values.intersection(frequency2_2_values):
            sum_result2_2 = sum_result2_2 + result[name2_2]
            sum_frequency2_2 = sum_frequency2_2 + frequency2_2[name2]
            frequency2_2_total[name2_2] = frequency2_2[name2]

        for name2_3 in result_values.intersection(frequency2_3_values):
            sum_result2_3 = sum_result2_3 + result[name2_3]
            sum_frequency2_3 = sum_frequency2_3 + frequency2_3[name2_3]
            frequency2_3_total[name2_3] = frequency2_3[name2_3]

        for name3 in result_values.intersection(frequency3_values):
            sum_result3 = sum_result3 + result[name3]
            sum_frequency3 = sum_frequency3 + frequency3[name3]
            frequency3_total[name3] = frequency3[name3]

        for name3_2 in result_values.intersection(frequency3_2_values):
            sum_result3_2 = sum_result3_2 + result[name3_2]
            sum_frequency3_2 = sum_frequency3_2 + frequency3_2[name3_2]
            frequency3_2_total[name3_2] = frequency3_2[name3_2]

        for name3_3 in result_values.intersection(frequency3_3_values):
            sum_result3_3 = sum_result3_3 + result[name3_3]
            sum_frequency3_3 = sum_frequency3_3 + frequency3[name3_3]
            frequency3_3_total[name3_3] = frequency3_3[name3_3]

        for name4 in result_values.intersection(frequency4_values):
            sum_result4 = sum_result4 + result[name4]
            sum_frequency4 = sum_frequency4 + frequency4[name4]
            frequency4_total[name4] = frequency4[name4]

        for name4_2 in result_values.intersection(frequency4_2_values):
            sum_result4_2 = sum_result4_2 + result[name4_2]
            sum_frequency4_2 = sum_frequency4_2 + frequency4_2[name4_2]
            frequency4_2_total[name4_2] = frequency4_2[name4_2]

        for name4_3 in result_values.intersection(frequency4_3_values):
            sum_result4_3 = sum_result4_3 + result[name4_3]
            sum_frequency4_3 = sum_frequency4_3 + frequency4_3[name4_3]
            frequency4_3_total[name4_3] = frequency4_3[name4_3]

        str_frequency2_total = str(frequency2_total)
        str_frequency2_2_total = str(frequency2_2_total)
        str_frequency2_3_total = str(frequency2_3_total)

        str_frequency3_total = str(frequency3_total)
        str_frequency3_2_total = str(frequency3_2_total)
        str_frequency3_3_total = str(frequency3_3_total)

        str_frequency4_total = str(frequency4_total)
        str_frequency4_2_total = str(frequency4_2_total)
        str_frequency4_3_total = str(frequency4_3_total)

        try:
            similarity2 = ((sum_result2/sum_frequency2)*100)
            if(similarity2 > 100):
                similarity2 = ((sum_frequency2/sum_result2)*100)
        except ZeroDivisionError:
            similarity2 = 0
            
        try:
            similarity2_2 = ((sum_result2_2/sum_frequency2_2)*100)
            if(similarity2_2 > 100):
                similarity2_2 = ((sum_frequency2_2/sum_result2_2)*100)
        except ZeroDivisionError:
            similarity2_2 = 0

        try:
            similarity2_3 = ((sum_result2_3/sum_frequency2_3)*100)
            if(similarity2_3 > 100):
                similarity2_3 = ((sum_frequency2_3/sum_result2_3)*100)
        except ZeroDivisionError:
            similarity2_3 = 0

        try:
            similarity3 = ((sum_result3/sum_frequency3)*100)
            if(similarity3 > 100):
                similarity3 = ((sum_frequency3/sum_result3)*100)
        except ZeroDivisionError:
            similarity3 = 0

        try:
            similarity3_2 = ((sum_result3_2/sum_frequency3_2)*100)
            if(similarity3_2 > 100):
                similarity3_2 = ((sum_frequency3_2/sum_result3_2)*100)
        except ZeroDivisionError:
            similarity3_2 = 0

        try:
            similarity3_3 = ((sum_result3_3/sum_frequency3_3)*100)
            if(similarity3_3 > 100):
                similarity3_3 = ((sum_frequency3_3/sum_result3_3)*100)
        except ZeroDivisionError:
            similarity3_3 = 0

        try:
            similarity4 = ((sum_result4/sum_frequency4)*100)
            if(similarity4 > 100):
                similarity4 = ((sum_frequency4/sum_result4)*100)
        except ZeroDivisionError:
            similarity4 = 0

        try:
            similarity4_2 = ((sum_result4_2/sum_frequency4_2)*100)
            if(similarity4_2 > 100):
                similarity4_2 = ((sum_frequency4_2/sum_result4_2)*100)
        except ZeroDivisionError:
            similarity4_2 = 0

        try:
            similarity4_3 = ((sum_result4_3/sum_frequency4_3)*100)
            if(similarity4_3 > 100):
                similarity4_3 = ((sum_frequency4_3/sum_result4_3)*100)
        except ZeroDivisionError:
            similarity4_3 = 0


        if(similarity2 == 0):
            str_similarity2 = "0"
        else:
            str_similarity2 = str(similarity2)

        if(similarity2_2 == 0):
            str_similarity2_2 = "0"
        else:
            str_similarity2_2 = str(similarity2_2)

        if(similarity2_3 == 0):
            str_similarity2_3 = "0"
        else:
            str_similarity2_3 = str(similarity2_3)

        if(similarity3 == 0):
            str_similarity3 = "0"
        else:
            str_similarity3 = str(similarity3)

        if(similarity3_2 == 0):
            str_similarity3_2 = "0"
        else:
            str_similarity3_2 = str(similarity3_2)

        if(similarity3_3 == 0):
            str_similarity3_3 = "0"
        else:
            str_similarity3_3 = str(similarity3_3)

        if(similarity4 == 0):
            str_similarity4 = "0"
        else:
            str_similarity4 = str(similarity4)

        if(similarity4_2 == 0):
            str_similarity4_2 = "0"
        else:
            str_similarity4_2 = str(similarity4_2)

        if(similarity4_3 == 0):
            str_similarity4_3 = "0"
        else:
            str_similarity4_3 = str(similarity4_3)

        similarity_rate_sorting_dict = {}
        
        similarity_rate_sorting_dict[url2] = similarity2
        similarity_rate_sorting_dict[url2_2] = similarity2_2
        similarity_rate_sorting_dict[url2_3] = similarity2_3

        similarity_rate_sorting_dict[url3] = similarity3
        similarity_rate_sorting_dict[url3_2] = similarity3_2
        similarity_rate_sorting_dict[url3_3] = similarity3_3

        similarity_rate_sorting_dict[url4] = similarity4
        similarity_rate_sorting_dict[url4_2] = similarity4_2
        similarity_rate_sorting_dict[url4_3] = similarity4_3

        sorted_dict = sorted(similarity_rate_sorting_dict.items(), key=operator.itemgetter(1), reverse=True)

        total_string = json.dumps(sorted_dict, indent=9)

        return render_template("index4.html", title="Indexing", content = total_string)
    else:
        return render_template("index4.html", title="Indexing")

@app.route("/Semantic", methods=["POST", "GET"])
def view_fifth_page():
    if request.method == "POST":
        url = request.form["url"]

        page = requests.get(url)

        links2_2 = []
        links2_3 = []
        links3_2 = []
        links3_3 = []
        links4_2 = []
        links4_3 = []

        page2 = requests.get('https://en.wikipedia.org/wiki/Turkey')
        page3 = requests.get('https://en.wikipedia.org/wiki/Black_hole')
        page4 = requests.get('https://en.wikipedia.org/wiki/International_Space_Station')
        
        soup = BeautifulSoup(page.content, 'html.parser')

        soup2 = BeautifulSoup(page2.content, 'html.parser')
        soup3 = BeautifulSoup(page3.content, 'html.parser')
        soup4 = BeautifulSoup(page4.content, 'html.parser')

        
        for link in soup2.findAll('a', attrs={'href': re.compile("^https://")}):
            links2_2.append(link.get('href'))

        page2_2 = requests.get(links2_2[3])
        soup2_2 = BeautifulSoup(page2_2.content, 'html.parser')

        for link in soup2_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links2_3.append(link.get('href'))

        page2_3 = requests.get(links2_3[1])
        soup2_3 = BeautifulSoup(page2_3.content, 'html.parser')

        for link in soup3.findAll('a', attrs={'href': re.compile("^https://")}):
            links3_2.append(link.get('href'))

        page3_2 = requests.get(links3_2[3])
        soup3_2 = BeautifulSoup(page3_2.content, 'html.parser')

        for link in soup3_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links3_3.append(link.get('href'))

        page3_3 = requests.get(links3_3[1])
        soup3_3 = BeautifulSoup(page3_3.content, 'html.parser')

        for link in soup4.findAll('a', attrs={'href': re.compile("^https://")}):
            links4_2.append(link.get('href'))

        page4_2 = requests.get(links4_2[3])
        soup4_2 = BeautifulSoup(page4_2.content, 'html.parser')

        for link in soup4_2.findAll('a', attrs={'href': re.compile("^https://")}):
            links4_3.append(link.get('href'))

        page4_3 = requests.get(links4_3[1])
        soup4_3 = BeautifulSoup(page4_3.content, 'html.parser')

        url2 = 'https://en.wikipedia.org/wiki/Turkey'
        url2_2 = links2_2[3]
        url2_3 = links2_3[1]

        url3 = 'https://en.wikipedia.org/wiki/Black_hole'
        url3_2 = links3_2[3]
        url3_3 = links3_3[1]

        url4 = 'https://en.wikipedia.org/wiki/International_Space_Station'
        url4_2 = links4_2[3]
        url4_3 = links4_3[1]

        text_string = soup.get_text()

        text_string2 = soup2.get_text()
        text_string2_2 = soup2_2.get_text()
        text_string2_3 = soup2_3.get_text()

        text_string3 = soup3.get_text()
        text_string3_2 = soup3.get_text()
        text_string3_3 = soup3.get_text()

        text_string4 = soup4.get_text()
        text_string4_2 = soup4_2.get_text()
        text_string4_3 = soup4_3.get_text()

        frequency = {}

        frequency2 = {}
        frequency2_2 = {}
        frequency2_3 = {}

        frequency3 = {}
        frequency3_2 = {}
        frequency3_3 = {}

        frequency4 = {}
        frequency4_2 = {}
        frequency4_3 = {}

        match_pattern = re.findall(r'\b[a-z]{5,10}\b', text_string)

        match_pattern2 = re.findall(r'\b[a-z]{3,15}\b', text_string2)
        match_pattern2_2 = re.findall(r'\b[a-z]{3,15}\b', text_string2_2)
        match_pattern2_3 = re.findall(r'\b[a-z]{3,15}\b', text_string2_3)

        match_pattern3 = re.findall(r'\b[a-z]{3,15}\b', text_string3)
        match_pattern3_2 = re.findall(r'\b[a-z]{3,15}\b', text_string3_2)
        match_pattern3_3 = re.findall(r'\b[a-z]{3,15}\b', text_string3_3)

        match_pattern4 = re.findall(r'\b[a-z]{3,15}\b', text_string4)
        match_pattern4_2 = re.findall(r'\b[a-z]{3,15}\b', text_string4_2)
        match_pattern4_3 = re.findall(r'\b[a-z]{3,15}\b', text_string4_3)
        
        for word in match_pattern:
            count = frequency.get(word,0)
            frequency[word] = count + 1

        for word in match_pattern2:
            count2 = frequency2.get(word,0)
            frequency2[word] = count2 + 1
        
        for word in match_pattern2_2:
            count2_2 = frequency2_2.get(word,0)
            frequency2_2[word] = count2_2 + 1
        
        for word in match_pattern2_3:
            count2_3 = frequency2_3.get(word,0)
            frequency2_3[word] = count2_3 + 1

        for word in match_pattern3:
            count3 = frequency3.get(word,0)
            frequency3[word] = count3 + 1

        for word in match_pattern3_2:
            count3_2 = frequency3_2.get(word,0)
            frequency3_2[word] = count3_2 + 1

        for word in match_pattern3_3:
            count3_3 = frequency3_3.get(word,0)
            frequency3_3[word] = count3_3 + 1

        for word in match_pattern4:
            count4 = frequency4.get(word,0)
            frequency4[word] = count4 + 1

        for word in match_pattern4_2:
            count4_2 = frequency4_2.get(word,0)
            frequency4_2[word] = count4_2 + 1

        for word in match_pattern4_3:
            count4_3 = frequency4_3.get(word,0)
            frequency4_3[word] = count4_3 + 1

        result = dict(sorted(frequency.items(), key = itemgetter(1), reverse = True)[:6]) # KeyWords for first link

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

        print(result)

        common_keys2 = result.keys() & frequency2.keys() # Finding the keywords in other links
        common_keys2_2 = result.keys() & frequency2_2.keys() # Finding the keywords in other links
        common_keys2_2 = result.keys() & frequency2_3.keys() # Finding the keywords in other links

        common_keys3 = result.keys() & frequency3.keys() # Finding the keywords in other links
        common_keys3_2 = result.keys() & frequency3_2.keys() # Finding the keywords in other links
        common_keys3_3 = result.keys() & frequency3_3.keys() # Finding the keywords in other links

        common_keys4 = result.keys() & frequency4.keys() # Finding the keywords in other links
        common_keys4_2 = result.keys() & frequency4_2.keys() # Finding the keywords in other links
        common_keys4_3 = result.keys() & frequency4_3.keys() # Finding the keywords in other links

        sum_result2 = 0
        sum_frequency2 = 0
        sum_result2_2 = 0
        sum_frequency2_2 = 0
        sum_result2_3= 0
        sum_frequency2_3 = 0

        sum_result3 = 0
        sum_frequency3 = 0
        sum_result3_2 = 0
        sum_frequency3_2 = 0
        sum_result3_3 = 0
        sum_frequency3_3 = 0

        sum_result4 = 0
        sum_frequency4 = 0
        sum_result4_2 = 0
        sum_frequency4_2 = 0
        sum_result4_3 = 0
        sum_frequency4_3 = 0

        frequency2_total = {}
        frequency2_2_total = {}
        frequency2_3_total = {}

        frequency3_total = {}
        frequency3_2_total = {}
        frequency3_3_total = {}

        frequency4_total = {}
        frequency4_2_total = {}
        frequency4_3_total = {}

        result_values = set(result)

        frequency2_values = set(frequency2)
        frequency2_2_values = set(frequency2_2)
        frequency2_3_values = set(frequency2_3)

        frequency3_values = set(frequency3)
        frequency3_2_values = set(frequency3_2)
        frequency3_3_values = set(frequency3_3)

        frequency4_values = set(frequency4)
        frequency4_2_values = set(frequency4_2)
        frequency4_3_values = set(frequency4_3)

        for name2 in result_values.intersection(frequency2_values):
            sum_result2 = sum_result2 + result[name2]
            sum_frequency2 = sum_frequency2 + frequency2[name2]
            frequency2_total[name2] = frequency2[name2]

        for name2_2 in result_values.intersection(frequency2_2_values):
            sum_result2_2 = sum_result2_2 + result[name2_2]
            sum_frequency2_2 = sum_frequency2_2 + frequency2_2[name2]
            frequency2_2_total[name2_2] = frequency2_2[name2]

        for name2_3 in result_values.intersection(frequency2_3_values):
            sum_result2_3 = sum_result2_3 + result[name2_3]
            sum_frequency2_3 = sum_frequency2_3 + frequency2_3[name2_3]
            frequency2_3_total[name2_3] = frequency2_3[name2_3]

        for name3 in result_values.intersection(frequency3_values):
            sum_result3 = sum_result3 + result[name3]
            sum_frequency3 = sum_frequency3 + frequency3[name3]
            frequency3_total[name3] = frequency3[name3]

        for name3_2 in result_values.intersection(frequency3_2_values):
            sum_result3_2 = sum_result3_2 + result[name3_2]
            sum_frequency3_2 = sum_frequency3_2 + frequency3_2[name3_2]
            frequency3_2_total[name3_2] = frequency3_2[name3_2]

        for name3_3 in result_values.intersection(frequency3_3_values):
            sum_result3_3 = sum_result3_3 + result[name3_3]
            sum_frequency3_3 = sum_frequency3_3 + frequency3[name3_3]
            frequency3_3_total[name3_3] = frequency3_3[name3_3]

        for name4 in result_values.intersection(frequency4_values):
            sum_result4 = sum_result4 + result[name4]
            sum_frequency4 = sum_frequency4 + frequency4[name4]
            frequency4_total[name4] = frequency4[name4]

        for name4_2 in result_values.intersection(frequency4_2_values):
            sum_result4_2 = sum_result4_2 + result[name4_2]
            sum_frequency4_2 = sum_frequency4_2 + frequency4_2[name4_2]
            frequency4_2_total[name4_2] = frequency4_2[name4_2]

        for name4_3 in result_values.intersection(frequency4_3_values):
            sum_result4_3 = sum_result4_3 + result[name4_3]
            sum_frequency4_3 = sum_frequency4_3 + frequency4_3[name4_3]
            frequency4_3_total[name4_3] = frequency4_3[name4_3]

        str_frequency2_total = str(frequency2_total)
        str_frequency2_2_total = str(frequency2_2_total)
        str_frequency2_3_total = str(frequency2_3_total)

        str_frequency3_total = str(frequency3_total)
        str_frequency3_2_total = str(frequency3_2_total)
        str_frequency3_3_total = str(frequency3_3_total)

        str_frequency4_total = str(frequency4_total)
        str_frequency4_2_total = str(frequency4_2_total)
        str_frequency4_3_total = str(frequency4_3_total)

        try:
            similarity2 = ((sum_result2/sum_frequency2)*100)
            if(similarity2 > 100):
                similarity2 = ((sum_frequency2/sum_result2)*100)
        except ZeroDivisionError:
            similarity2 = 0
            
        try:
            similarity2_2 = ((sum_result2_2/sum_frequency2_2)*100)
            if(similarity2_2 > 100):
                similarity2_2 = ((sum_frequency2_2/sum_result2_2)*100)
        except ZeroDivisionError:
            similarity2_2 = 0

        try:
            similarity2_3 = ((sum_result2_3/sum_frequency2_3)*100)
            if(similarity2_3 > 100):
                similarity2_3 = ((sum_frequency2_3/sum_result2_3)*100)
        except ZeroDivisionError:
            similarity2_3 = 0

        try:
            similarity3 = ((sum_result3/sum_frequency3)*100)
            if(similarity3 > 100):
                similarity3 = ((sum_frequency3/sum_result3)*100)
        except ZeroDivisionError:
            similarity3 = 0

        try:
            similarity3_2 = ((sum_result3_2/sum_frequency3_2)*100)
            if(similarity3_2 > 100):
                similarity3_2 = ((sum_frequency3_2/sum_result3_2)*100)
        except ZeroDivisionError:
            similarity3_2 = 0

        try:
            similarity3_3 = ((sum_result3_3/sum_frequency3_3)*100)
            if(similarity3_3 > 100):
                similarity3_3 = ((sum_frequency3_3/sum_result3_3)*100)
        except ZeroDivisionError:
            similarity3_3 = 0

        try:
            similarity4 = ((sum_result4/sum_frequency4)*100)
            if(similarity4 > 100):
                similarity4 = ((sum_frequency4/sum_result4)*100)
        except ZeroDivisionError:
            similarity4 = 0

        try:
            similarity4_2 = ((sum_result4_2/sum_frequency4_2)*100)
            if(similarity4_2 > 100):
                similarity4_2 = ((sum_frequency4_2/sum_result4_2)*100)
        except ZeroDivisionError:
            similarity4_2 = 0

        try:
            similarity4_3 = ((sum_result4_3/sum_frequency4_3)*100)
            if(similarity4_3 > 100):
                similarity4_3 = ((sum_frequency4_3/sum_result4_3)*100)
        except ZeroDivisionError:
            similarity4_3 = 0


        if(similarity2 == 0):
            str_similarity2 = "0"
        else:
            str_similarity2 = str(similarity2)

        if(similarity2_2 == 0):
            str_similarity2_2 = "0"
        else:
            str_similarity2_2 = str(similarity2_2)

        if(similarity2_3 == 0):
            str_similarity2_3 = "0"
        else:
            str_similarity2_3 = str(similarity2_3)

        if(similarity3 == 0):
            str_similarity3 = "0"
        else:
            str_similarity3 = str(similarity3)

        if(similarity3_2 == 0):
            str_similarity3_2 = "0"
        else:
            str_similarity3_2 = str(similarity3_2)

        if(similarity3_3 == 0):
            str_similarity3_3 = "0"
        else:
            str_similarity3_3 = str(similarity3_3)

        if(similarity4 == 0):
            str_similarity4 = "0"
        else:
            str_similarity4 = str(similarity4)

        if(similarity4_2 == 0):
            str_similarity4_2 = "0"
        else:
            str_similarity4_2 = str(similarity4_2)

        if(similarity4_3 == 0):
            str_similarity4_3 = "0"
        else:
            str_similarity4_3 = str(similarity4_3)

        similarity_rate_sorting_dict = {}
        
        similarity_rate_sorting_dict[url2] = similarity2
        similarity_rate_sorting_dict[url2_2] = similarity2_2
        similarity_rate_sorting_dict[url2_3] = similarity2_3

        similarity_rate_sorting_dict[url3] = similarity3
        similarity_rate_sorting_dict[url3_2] = similarity3_2
        similarity_rate_sorting_dict[url3_3] = similarity3_3

        similarity_rate_sorting_dict[url4] = similarity4
        similarity_rate_sorting_dict[url4_2] = similarity4_2
        similarity_rate_sorting_dict[url4_3] = similarity4_3

        sorted_dict = sorted(similarity_rate_sorting_dict.items(), key=operator.itemgetter(1), reverse=True)

        total_string = json.dumps(sorted_dict, indent=9)

        return render_template("index5.html", title="Semantic", content = total_string)
    else:
        return render_template("index5.html", title="Semantic")

if __name__ == "__main__":
    app.run()