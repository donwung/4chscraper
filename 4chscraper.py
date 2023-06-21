from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request
from requests import get
import re
import os
import urllib.request
import shutil
import sys
import threading
import time
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
    data = {
        **request.form
    }
    print(data)

    links = parse_url(data['thread_URL'])
    all_imgs = download_all_images_from_links(links)

    return render_template("out.html", allImgs=all_imgs)


def dl_img_at_indices(links, all_imgs, increment, start):
    for link_i in range(start - 1, len(links), increment):
        _link = "https:"+links[link_i].get("href")

        postNum = re.findall("[0123456789]", _link)
        postNum = flattenPostNumArr(postNum)

        fileExt = re.findall("\.[a-z]+", _link)
        fileExt = fileExt[1]

        oneFile = [postNum, fileExt]
        all_imgs.append(oneFile)
        fileName = postNum + fileExt

        # this downloads one file named as the post number
        if not os.path.exists(f"./static/{fileName}"):
            download(_link, fileName)
    return all_imgs


def download_all_images_from_links(links):
    all_imgs = []

    number_of_threads = 4

    t1 = threading.Thread(
        target=dl_img_at_indices, args=(links, all_imgs, number_of_threads, 1))
    t2 = threading.Thread(
        target=dl_img_at_indices, args=(links, all_imgs, number_of_threads, 2))
    t3 = threading.Thread(
        target=dl_img_at_indices, args=(links, all_imgs, number_of_threads, 3))
    t4 = threading.Thread(
        target=dl_img_at_indices, args=(links, all_imgs, number_of_threads, 4))

    start = time.time()
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # for link in links:
    #     _link = "https:"+link.get("href")
    #     # print(_link)

    #     postNum = re.findall("[0123456789]", _link)
    #     postNum = flattenPostNumArr(postNum)

    #     fileExt = re.findall("\.[a-z]+", _link)
    #     fileExt = fileExt[1]

    #     oneFile = [postNum, fileExt]
    #     all_imgs.append(oneFile)
    #     fileName = postNum + fileExt

    #     # this downloads one file named as the post number
    #     if not os.path.exists(f"./static/{fileName}"):
    #         download(_link, fileName)
    end = time.time()
    print("exec time: {}".format(end-start))
    return all_imgs


@app.route("/keep_selected", methods=["POST"])
def keep_selected():
    data = {
        **request.form
    }

    for file in os.listdir("./static"):
        print(file)
        if file not in data.keys():
            os.remove(f"./static/{file}")

    return redirect("/")
