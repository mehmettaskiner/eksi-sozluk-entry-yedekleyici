# -*- coding: utf-8 -*-
import timeit
import sys
import logging
import urllib2
import argparse
from argparse import RawTextHelpFormatter
from lxml import html

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('-y', '--yazar',
                    help='yedegini cikarmak istediginiz yazarin nicki')
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

class entry_yedek():
    def __init__(self):
        self.yazar_adi = ''
        self.eksi_base_url = 'https://eksisozluk.com'

    def stringify_children(self, node):
        if node is None:
            return ''

        s = node.text
        if s is None:
            s = ''
        for child in node:
            s += html.tostring(child, encoding='unicode')
        return s

    def page_tree(self, url):
        try:
            request = urllib2.Request(url)
            page_data = urllib2.urlopen(request).read()
            return html.fromstring(page_data)
        except urllib2.HTTPError:
            print 'bu yazari (%s) bulamadim...' % self.yazar_adi
            exit()

    def start_fetching(self):
        yazar_adi_replaced = yazar_adi.replace(" ", "-")
        son_entry_url = self.eksi_base_url + "/basliklar/istatistik/" + yazar_adi_replaced + "/son-entryleri"
        ikinci_sayfa_url = son_entry_url + '?p=' + str(2);

        page_info = self.page_tree(ikinci_sayfa_url).find(".//div[@class='pager']")

        if page_info is None:
            sayfa_sayisi = 1
        else:
            sayfa_sayisi = int(page_info.get('data-pagecount'))

        print "PAGE INFO::::::::" + str(sayfa_sayisi)

        logging.info("yedeklenen yazar: " + yazar_adi)
        filename = yazar_adi_replaced + "_yedek.txt"
        f = open(filename, "wb")

        logging.info("kaydediliyor")
        logging.info("toplam sayfa sayisi : %s" % sayfa_sayisi)

        for i in range(1, sayfa_sayisi + 1):
            logging.info("islenilen sayfa : %s " % i)
            sayfa_url = son_entry_url + "?p=" + str(i)
            a = self.page_tree(sayfa_url).findall(".//ul[@class='topic-list']//a")
            for link in a:
                logging.info("baslik : %s - link : %s" % (link.text.strip(), link.get('href')))
                entry_tree = self.page_tree(self.eksi_base_url + str(link.get('href')))
                if entry_tree is not None:
                    baslik = entry_tree.find(".//h1[@id='title']").get('data-title').encode('utf-8').strip()
                    entry = self.stringify_children(
                        entry_tree.find(".//div[@class='content']")).encode('utf-8').strip()

                    tarih = entry_tree.find(".//a[@class='entry-date permalink']").text.strip()

                    f.write("%s\n%s\n%s\n\n" % (baslik, entry, tarih))

            sys.stdout.flush()

        f.close()


if __name__ == "__main__":
    start = 0
    if args.yazar is None:
        yazar_adi = raw_input("yazar adini girin: ")
    else:
        yazar_adi = args.yazar
    if yazar_adi:
        ey = entry_yedek()
        ey.yazar_adi = yazar_adi
        start = timeit.default_timer()
        ey.start_fetching()
    else:
        print 'o isim buraya yazilacak'

    stop = timeit.default_timer()

    print 'Toplam %s saniye surdu tum islem... ' % int(stop - start)
