#! /usr/bin/env python
# coding: utf-8
# -*- coding: utf_8 -*-

import csv
import requests
from BeautifulSoup import BeautifulSoup

HOST = 'http://brushup.narihiro.info/'

def getPageData(url):
    res = requests.get(url)
    if not res.ok:
        return [], None

    soup = BeautifulSoup(res.content, fromEncoding='utf-8')

    titles = soup.findAll('div', attrs={'class': 'show-title'})
    titles = [el.find('a').text.encode('utf-8') for el in titles]

    bodies = soup.findAll('div', attrs={'class': 'show-body'})
    bodies = [reduce(lambda a,b: a+b.__str__('utf-8'), el.findAll('p'), '') for el in bodies]

    next = soup.find('a', attrs={'class': 'next_page'})
    return zip(titles, bodies), next['href'] if next else None


def getPagesData(host, url):
    pages = []
    while url:
        page, url = getPageData(host + url)
        pages += page
    return pages


def getBrushupData(user, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerows(getPagesData(HOST, user + '/completed'))
        writer.writerows(getPagesData(HOST, user + '/list'))
        writer.writerows(getPagesData(HOST, user + '/today'))


if __name__ == '__main__':
    getBrushupData('kojit', 'brushup.csv')

# vim: set et :
