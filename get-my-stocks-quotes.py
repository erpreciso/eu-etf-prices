#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 16:00:55 2019

@author: erpreciso

Get quotes for the ISIN list from the IngDiBa pages (div class "price) 
and save in a text file comma-delimited name,isin,price.

"""

import datetime as dt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import locale
import os

locale.setlocale( locale.LC_ALL, '')

folder = '/home/erpreciso/Dropbox/records/financial-records/investing/my-quotes'

f = os.path.join(folder, str(dt.date.today()) + '_quotes.txt')
f2 = os.path.join(folder, 'current_quotes.txt')

names_list = [
        '1. Deka DAX',
        '2. Euro Inflation Linked',
        '3. Germany Govt',
        '4. Emerging Markets',
        '5. TecDAX',
        '6. Ishares MSCI World',
        '7. Global Govt Bonds',
        '8. SPDR MSCI World',
        ]

isin_list = [
        'DE000ETFL060',
        'LU0290358224',
        'DE000A0D8Q31',
        'LU1681045370',
        'DE0005933972',
        'IE00B4L5Y983',
        'LU0378818131',
        'IE00BFY0GT14',
        ]

def get_price(isin):
    url = 'https://wertpapiere.ing.de/DE/Showpage.aspx?pageID=30&ISIN=' + isin
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out    
    raw_price = soup.find('div','price').contents[0]    
    string_price = re.sub('[^0-9,.]+', '', raw_price)    
    price = locale.atof(string_price)    
    return(price)
        
prices = [get_price(isin) for isin in isin_list]

with open(f, 'w') as file:
    for i in range(len(isin_list)):
        s = ','.join([names_list[i], isin_list[i], str(prices[i]), '\n'])
        file.write(s)

with open(f2, 'w') as file:
    for i in range(len(isin_list)):
        s = ','.join([names_list[i], isin_list[i], str(prices[i]), '\n'])
        file.write(s)
