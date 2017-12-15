#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os.path
import csv
import codecs

def scrap_search( company, city ):

    query = (company+" "+city).replace( " ", "+" )
    params = {'q':query}

    response = requests.get(
        'https://www.duckduckgo.com/html/',
        params=params,
        headers={
            "Content-Type": "text/html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0"
            }
        )
    return response.text

def load_company( company, city ):

    print( "Loading company ["+company+"] at ["+city+"]" )
    # Look if data is in the cache
    filename = "../cache/%s-%s" % ( company, city )
    if not os.path.isfile(filename) :
        text = scrap_search( company, city )
        with open(filename, "w") as cache_file:
            cache_file.write(text)

    with open( filename, "r") as file:

        soup = BeautifulSoup(file.read(),"html.parser")

        for link in soup.find('h2', class_='result__title').select('a[href]'):
            print( link['href'] )


load_company( "AVISIA", "PARIS" )
load_company( "GROUPE CIMES", "PUTEAUX" )
load_company( "communaute coeur de chartreuse", "entre deux guiers" )

with codecs.open('../test-data/10000.csv', 'r', 'latin1') as siren:
    siren_reader = csv.reader(siren, delimiter=';', quotechar='"')
    for row in siren_reader:
        siren = row[0]
        name = row[2]
        city = row[28]
        if row[47]=='NN':
            row[47] = '0' 
        emp_count = int(row[47])
        if emp_count>10:
 #           print( name+" "+city+" ("+str(emp_count)+")" )
            load_company( name, city )

