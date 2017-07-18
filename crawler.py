"""Base class for webcrawler that communicates with Tor client."""

import socket
import socks
import requests
from bs4 import BeautifulSoup
import time
import warnings
import os
from collections import defaultdict
import json

# Stem is a module for dealing with tor
from stem import Signal
from stem.control import Controller
from stem.connection import authenticate_none, authenticate_password
import re
from time import sleep
import urllib2
from TorCrawler import TorCrawler


robotre= re.compile('images-amazon\.com/captcha/')

#this parsing method returns a string
def getOccupationLocation(textList):
    for i in xrange(len(textList)):
        resultString = ""
        stringGen = textList[i:i+len("occupationLocationList")]
        if stringGen == "occupationLocationList":
            j = i + len("occupationLocationList") + 2
            while textList[j] != "]":
                resultString = resultString+textList[j]
                j = j + 1
            return resultString+"]"


def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=3)
        return True
    except: 
        return False

def check_network():
    while(not internet_on()): 
        print "the network is down"
        sleep(300)




mySet=set()
with open('LaptopReviewer.txt') as f:
    myList=[]
    for line in f:
        id=line.strip()
        #check for repetitive ids
        if id not in mySet: 
            mySet.add(id)
            myList.append(id)

print "the number of reviewers is"
print len(myList)

#opening a file to write to it
myFile = open('Locations2.txt','w')

# checks internet connection
check_network()
#setting up the tor crawler

crawler = TorCrawler(ctrl_pass="2110168")

#the for loop to get locations
for id_ in range(14669,20000):        

    
    url = "http://www.amazon.com/gp/cdp/member-reviews/" + myList[id_]
    

      
      ##another layer of error handling
    htmlpage, code = crawler.get(url)


    if htmlpage is not None: 
        resultList = getOccupationLocation(htmlpage.encode('ascii', 'ignore'))
        if resultList!="[]": 
            data = {}
            data['asin'] = myList[int(id_)]
            data['ocupationList']=resultList
            json.dump(data, myFile)
            myFile.write('\n')
            myFile.flush()
            print resultList
          
        else: 
            print "the reviewer does not have an address and the reviewerID is"
            print myList[id_]
       

    if htmlpage is None or code != 200:
        print "code!=200!" 
        check_network()
        print "moving on to the next reviewer and rotating IP"
        crawler.rotate()
        sleep(300)

    else:
        if robotre.search(htmlpage):
    	   print('ROBOT!, rotating IP and sleeping for 60 seconds')
           check_network()
           crawler.rotate()
           sleep(60)


    print id_



    
                   
