# -*- coding: utf8 -*-
import urllib2
from bs4 import BeautifulSoup

yazar_adi = raw_input("yazar adini girin: \n")
yazar_adi_replaced = yazar_adi.replace(" ", "-")

entry_sayisi = 0

filename = yazar_adi + " yedek.txt"
f = open(filename, "wb")
f.write("yedeklenen yazar: " + yazar_adi + "\n\n\n")
f.write("-----------------------------------------\n\n\n")

son_entry_url = "https://eksisozluk.com/biri/" + yazar_adi_replaced + "/son-entryleri"
son_entry_request = urllib2.Request(son_entry_url)
son_entry_response = urllib2.urlopen(son_entry_request)
son_entry_data = son_entry_response.read()

soup = BeautifulSoup(son_entry_data)
sayfa_sayisi = int(soup.find("div", attrs={'class': 'pager'})['data-pagecount'])
for i in range(1, sayfa_sayisi + 1):
    sayfa_url = son_entry_url + "?p=" + str(i)
    sayfa_request = urllib2.Request(sayfa_url)
    sayfa_response = urllib2.urlopen(sayfa_request)
    sayfa_data = sayfa_response.read()
    sayfa_soup = BeautifulSoup(sayfa_data)
    
    entry_urls = sayfa_soup.find_all("ul", attrs={'class': 'topic-list'})[1]
    a = entry_urls.find_all("a") # all a tags under ul tag
    for link in a:
        entry_sayisi += 1
        entry_url = "https://eksisozluk.com" + str(link['href'])
        entry_page_request = urllib2.Request(entry_url)
        entry_page_response = urllib2.urlopen(entry_page_request)
        entry_page_data = entry_page_response.read()
        entry_soup = BeautifulSoup(entry_page_data)

        baslik = entry_soup.find("h1", attrs={'id': 'title'})['data-title'].encode('utf-8')
        entry = entry_soup.find("div", attrs={'class': 'content', 'itemprop': 'commentText'}).text.encode('utf-8')
        f.write(baslik + ":\n")
        f.write(entry + "\n\n")

f.close()