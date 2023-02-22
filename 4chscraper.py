from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request
from requests import get
import re
import os
import urllib.request
import shutil
import sys
app = Flask(__name__)

# reads url, puts it into soup, returns all hrefs ie web files
def parse_url(thread_URL):
    req = urllib.request.Request(
        thread_URL, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    html_doc = response.read()
    # print(response)
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all("a", class_="fileThumb")
    return links

# downloads file into static folder
def download(url, file_name):
    with open("./static/"+file_name, "wb") as file:
        res = get(url)
        file.write(res.content)

# after getting a regex match array, this flattens an array of characters 
def flattenPostNumArr(arr):
    res = ""
    for i in range(1, len(arr)):
        res = res + arr[i]
    return res

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_imgs", methods=["POST"])
def get_imgs():
    allImgs = []
    data = {
        **request.form
    }
    print(data)

    links = parse_url(data['thread_URL'])
    for link in links:
        _link = "https:"+link.get("href")
        # print(_link)

        postNum = re.findall("[0123456789]", _link)
        postNum = flattenPostNumArr(postNum)

        fileExt = re.findall("\.[a-z]+", _link)
        fileExt = fileExt[1]

        oneFile = [postNum, fileExt]
        allImgs.append(oneFile)
        fileName = postNum + fileExt

        # this downloads one file named as the post number
        if not os.path.exists(f"./static/{fileName}"):
            download(_link, fileName)

    return render_template("out.html", allImgs=allImgs)


@app.route("/keep_selected", methods=["POST"])
def keep_selected():
    data = {
        **request.form
    }

    for file in os.listdir("./static"):
        print(file)
        if file  not in data.keys():
            os.remove(f"./static/{file}")
            
    return redirect("/")