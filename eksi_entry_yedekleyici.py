# -*- coding: utf8 -*-
import urllib2
from bs4 import BeautifulSoup

def get_page_data(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = response.read()
    return data

def soup_data(data):
    soup = BeautifulSoup(data)
    return soup

def start_fetching():
    yazar_adi = raw_input("yazar adini girin: \n")
    yazar_adi_replaced = yazar_adi.replace(" ", "-")
    son_entry_url = "https://eksisozluk.com/biri/" + yazar_adi_replaced + "/son-entryleri"

    filename = yazar_adi + " yedek.txt"
    f = open(filename, "wb")
    f.write("yedeklenen yazar: " + yazar_adi + "\n\n\n")
    f.write("-----------------------------------------\n\n\n")

    son_entryleri_soup = soup_data(get_page_data(son_entry_url))

    sayfa_sayisi = int(son_entryleri_soup.find("div", attrs={'class': 'pager'})['data-pagecount'])
    for i in range(1, sayfa_sayisi + 1):
        sayfa_url = son_entry_url + "?p=" + str(i)
        sayfa_soup = soup_data(get_page_data(sayfa_url))
        
        entry_urls = sayfa_soup.find_all("ul", attrs={'class': 'topic-list'})[1]
        a = entry_urls.find_all("a") # all a tags under ul tag
        for link in a:
            entry_url = "https://eksisozluk.com" + str(link['href'])
            entry_soup = soup_data(get_page_data(entry_url))

            baslik = entry_soup.find("h1", attrs={'id': 'title'})['data-title'].encode('utf-8')
            entry = entry_soup.find("div", attrs={'class': 'content', 'itemprop': 'commentText'}).text.encode('utf-8')
            f.write(baslik + ":\n")
            f.write(entry + "\n\n")

    f.close()

start_fetching()