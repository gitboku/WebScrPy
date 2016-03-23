# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from _io import open
from _datetime import datetime
import re

if __name__ == '__main__':
    
    #Encoding of amazon is "cp932".
    URL = "http://www.amazon.co.jp/gp/bestsellers/books"
      
    #BeautifulSoup is a library processes HTML and XML files.
    #Constractor of BeautifulSoup is a file object of HTML file or charactors.
    #"urlopen()" is a method of urlli.request.
    html = urlopen(URL).read().decode('cp932')
    soup = BeautifulSoup(html, "html.parser")
    itemRowLists = soup.find_all("div", attrs={"class": "zg_itemRow"})#type(itemRowLists) -> bs4.element.ResultSet
     
    fileName = datetime.now().strftime("%Y%m%d%H")+".txt"
#     fileName = "test.txt"
    f = open(fileName, "w")#reading:"r" writing:"w" exclusive:"x" adding:"a"
         
    for itemRow in itemRowLists:
        rank    = itemRow.find("span", attrs={"class": "zg_rankNumber"}).text.replace(".", "").strip()
        title   = itemRow.find("div", attrs={"class": "zg_title"}).text
        byline  = itemRow.find("div", attrs={"class": "zg_byline"}).text.replace(",", "").strip()
        review  = itemRow.find("div", attrs={"class": "zg_reviews"}).text.strip()
        patP    = re.compile('5つ星のうち \d.\d')
        reviewP = patP.findall(review)
        patN    = re.compile('(.+)')
        reviewN = patN.findall(review)
        if(len(reviewP) == 0):
            reviewP ="NA"
            reviewN = "NA"
        else:
            reviewP = reviewP.pop(0).replace("5つ星のうち ", "")
            reviewN = reviewN.pop(1).strip().replace("(", "").replace(")", "").replace(",", "")
        platform = itemRow.find("div", attrs={"class": "zg_bindingPlatform"}).text.strip()
        price   = itemRow.find("p", attrs={"class": "priceBlock"}).text.replace("￥", "").replace("価格：", "").replace(",", "").strip()
        
        outputText = rank + "," + title + "," + byline + "," + reviewP + "," + reviewN + "," + platform + "," + price
        
        print(outputText)
        f.write(outputText + "\n")
         
    f.close()
    print("(`・言・´)")