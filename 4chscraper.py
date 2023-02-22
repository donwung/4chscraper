from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request
from requests import get
import re
import os
import urllib.request
import shutil
import sys
app = Flask(__name__)


def parse_url(thread_URL):

    req = urllib.request.Request(
        thread_URL, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    f = open('C:\\Users\\John\\Desktop\\Programming\\Projects\\4chscraper\\html_in.html', encoding="utf-8")
    html_doc = response.read()
    print(response)
    f.close()

    soup = BeautifulSoup(html_doc, 'html.parser')

    links = soup.find_all("a", class_="fileThumb")

    return links


# print(resource)
# content = resource.read().decode(resource.headers.get_content_charset())

def download(url, file_name):
    with open("./static/"+file_name, "wb") as file:
        res = get(url)
        # this writes the content
        file.write(res.content)

        # TODO: delete
        # os.remove("temp/1676914568692510.png")


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

        # this 
        # TODO: refactor this
        hosting = re.sub(f"{postNum}{fileExt}", "", _link)
        # print(hosting)

        oneFile = [postNum, fileExt]
        allImgs.append(oneFile)
        fileName = postNum + fileExt

        # this enables a download
        if not os.path.exists(f"./static/{fileName}"):
            download(_link, fileName)

    return render_template("out.html", allImgs=allImgs)
    # return render_template("out.html")


@app.route("/keep_selected", methods=["POST"])
def keep_selected():
    data = {
        **request.form
    }
    print(f"data to keep: {data}")
    # deletes static folder and rebuilds static folder
    # shutil.rmtree("./static")
    # # print(hosting)
    # if not os.path.exists("./static"):
    #     os.makedirs("./static")

    for file in os.listdir("./static"):
        print(file)
        if file  not in data.keys():
            os.remove(f"./static/{file}")
            

    # for fileName in data.keys():
    #     print(fileName)

    #     if os.path.exists(f"./static/{fileName}"):
    #         # TODO: deletes at name
    #         os.remove(f"./static/{fileName}")
    #         # download(_link, fileName)

        # postNum = re.findall("[0123456789]", _link)
        # postNum = flattenPostNumArr(postNum)

        # fileExt = re.findall("\.[a-z]+", _link)
        # fileExt = fileExt[1]

        # # TODO: refactor this
        # hosting = re.sub(f"{postNum}{fileExt}", "", _link)
        # # print(hosting)

        # oneFile = [postNum, fileExt]
        # allImgs.append(oneFile)
        # fileName = postNum + fileExt

    # deletes static folder and rebuilds static folder
    # shutil.rmtree("./static")
    # # print(hosting)
    # if not os.path.exists("./static"):
    #     os.makedirs("./static")

    # for link in data.keys():
    #     print(link)
        # download(hosting+link, link)
    return redirect("/")
# add a route to trigger a request to start downloading
