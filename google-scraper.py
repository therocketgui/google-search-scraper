import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus, quote
from urllib.error import HTTPError, URLError
from random import randint
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import ssl
import csv
import datetime

# INFOS #

# Search API : https://asciimoo.github.io/searx/dev/search_api.html

# Infos
# The searX API direct call Google, Bing and Yahoo Search APIs without any limits / securities + it's anonymous

class Google():

    def __init__(self, q):
        self.q = q

        return

    def create_url(self, page_number):
        encoded_query = urlencode({'q' : self.q})
        url = "https://searx.ch/search?" + encoded_query + "&pageno=" + str(page_number)
        return url

    def call_url(self, page_number):
        url = self.create_url(page_number)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        #print("Query URL :")
        #print(url)
        response = urlopen(url, context=ctx)
        string = response.read().decode('utf-8')
        soup = BeautifulSoup(string, 'lxml')

        print('Scraping... '+str(url)+'\n')
        return soup

    def website_list(self):
        website_list = []

        for i in range(1,3):

            soup = self.call_url(i)

            for attrs in soup.find_all("div", {"class":"result result-default"}): 
                try:
                    title = str(attrs.h4.text)
                    description = str(attrs.p.text)
                    link = str(attrs.a['href'])

                    website = {'title':title.replace(",", " "), 'link':link, 'description': description.replace(",", " ")}

                    website_list.append(website)
                except Exception as e:
                    print(e)

        return website_list

    def print_csv(self,website_list):
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
        filename='results-'+date+'.csv'

        with open(filename, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Title', 'Url', 'Description'])

            for website in website_list:
                filewriter.writerow([website['title'], website['link'], website['description']])

        return

if __name__ == "__main__":

    scrap = Google("site:*.co.uk “request callback”")
    rlist=scrap.website_list()
    scrap.print_csv(rlist)