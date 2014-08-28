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
parser.add_argument('-v', '--verbose',
                    help='debug icin bisiler bas ekrana aslanim',
                    action='store_true')
args = parser.parse_args()

if args.verbose:
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

    def burry_inside_div(self, text, div_class):
        div_tag = '<div class="' + div_class + '">'
        div_close = '</div>'
        new_text = div_tag + text + div_close
        return new_text
        
    def start_fetching(self):
        yazar_adi_replaced = yazar_adi.replace(" ", "-")
        son_entry_url = self.eksi_base_url + "/biri/" + yazar_adi_replaced + "/son-entryleri"
        page_info = self.page_tree(son_entry_url).find(".//div[@class='pager']")
        if page_info is None:
            sayfa_sayisi = 1
        else:
            sayfa_sayisi = int(page_info.get('data-pagecount'))

        logging.info("yedeklenen yazar: " + yazar_adi)
        filename = yazar_adi + "_yedek.html"
        f = open(filename, "wb")

        logging.info("kaydediliyor")
        logging.info("toplam sayfa sayisi : %s" % sayfa_sayisi)

        f.write('<html><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="./style.css"><title>' + self.yazar_adi + '</title></head><body><div class="main_div"')

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
                        entry_tree.find(".//div[@class='content'][@itemprop='commentText']")).encode('utf-8').strip()
                    tarih = entry_tree.find(".//time").text.strip()
                    baslik = self.burry_inside_div(baslik, "baslik")
                    entry = self.burry_inside_div(entry, "content")
                    tarih = self.burry_inside_div(tarih, "time")

                    f.write("<h1>%s</h1><hr>\n%s\n<time>%s</time>\n\n" % (baslik, entry, tarih))

            sys.stdout.flush()

        f.write('</div></body></html>')
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
