#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os.path
import csv
import codecs
# from urlparse import urlparse
import urllib
import subprocess
import json

def get_site_info( url ):
    try:
        return json.loads(subprocess.check_output(["node", "../index", url]))
    except subprocess.CalledProcessError as e:
        print( "*** Error webanalyzing" )

def scrap_search( company, city ):

    query = (city+" "+company).replace( " ", "+" )
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

def url_for_company( company, city ):

    # Look if data is in the cache
    filename = "../cache/%s-%s" % ( company, city )
    if not os.path.isfile(filename) :
        text = scrap_search( company, city )
        with open(filename, "w") as cache_file:
            cache_file.write(text)

    with open( filename, "r") as file:

        soup = BeautifulSoup(file.read(),"html.parser")

        results = soup.find_all('h2', class_='result__title')
        total_tries = 5
        for result in results:
        # if results == None:
        #     print( "**** NO RESULTS?" )
        #     return
            for link in result.select('a[href]'):
                url =  link['href']
                parsed = urllib.parse.urlparse(url)
                # print( parsed )
                if parsed.path=="/" and parsed.query=='':
                    tentative_url = url
                    # check_url_contains( tentative_url, company )
                    return url
                total_tries -= 1
                if total_tries==0:
                    return

def extract_web_server( info ):
    for o in info:
        if "categories" in o:
            for c in o["categories"]:
                if "22" in c:
                    return o["name"]

def do_work( index, total ):

    current = 0
    with codecs.open('../test-data/test.csv', 'r', 'latin1') as siren:
        siren_reader = csv.reader(siren, delimiter=';', quotechar='"')
        for row in siren_reader:
            current += 1
            if current==1 or current%total!=index:
                continue
            siren = row[0]
            name = row[2]
            city = row[28]
            siege = int(row[35])
            if row[47]=='NN':
                row[47] = '0' 
            emp_count = int(row[47])
            if siege and emp_count>5:
                print( siren+": "+name+" "+city )
    #           print( name+" "+city+" ("+str(emp_count)+")" )
                url = url_for_company( name, city )
                if url!=None:
                    info = get_site_info( url )
                    web_server = extract_web_server( info )
                    if web_server==None:
                        web_server = ""
                    yield [ siren, url, web_server ]

import sys

index = int( sys.argv[1] )
total = int( sys.argv[2] )

with open( "out-"+str(index)+".csv", "w") as result_file:
    for [siren,web,web_server] in do_work( index, total ):
        print( [siren,web,web_server] )
        result_file.write( siren+","+web+","+web_server+"\n" )
        result_file.flush()

