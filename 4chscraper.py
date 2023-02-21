from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request
from requests import get
import re
import os
import urllib.request

app = Flask(__name__)

req = urllib.request.Request("https://boards.4chan.org/gif/thread/24563804", headers={'User-Agent': 'Mozilla/5.0'}) 
response = urllib.request.urlopen(req)
f = open('C:\\Users\\John\\Desktop\\Programming\\Projects\\4chscraper\\html_in.html', encoding="utf-8")
html_doc = response.read()
print(response)
f.close()

soup = BeautifulSoup(html_doc, 'html.parser')
 
links = soup.find_all("a", class_="fileThumb") 
allImgs = []
 

# print(resource)
# content = resource.read().decode(resource.headers.get_content_charset())

def download(url, file_name): 
    with open("./static/"+file_name, "wb") as file:
        res = get(url)
        # this writes the content
        # file.write(res.content) 

        # TODO: delete
        # os.remove("temp/1676914568692510.png") 

def flattenPostNumArr (arr):
    res = ""
    for i in range(1,len(arr)):
        res = res + arr[i]
    return res

for link in links: 
    _link = "https:"+link.get("href")
    # print(_link)


    postNum = re.findall("[0123456789]", _link)
    postNum = flattenPostNumArr(postNum)

    fileExt = re.findall("\.[a-z]+", _link)
    fileExt = fileExt[1]
    
    # TODO: refactor this
    hosting = re.sub(f"{postNum}{fileExt}", "", _link)
    # print(hosting)

    oneFile = [postNum, fileExt]
    allImgs.append(oneFile)
    fileName = postNum + fileExt

    # this enables a download
    # download(_link, fileName)

@app.route("/")
def hello_world():
    return render_template("out.html", allImgs = allImgs)

@app.route("/keep_selected", methods=["POST"])
def keep_selected():
    data = {
        **request.form
    }
    print(hosting)

    for link in data.keys():
        print(link)
    return redirect("/")
#add a route to trigger a request to start downloading 