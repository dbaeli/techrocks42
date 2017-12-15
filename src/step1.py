#!/usr/local/bin/python3

from bs4 import BeautifulSoup

html_doc = """
<html>
    <head>
    <title>Titre de votre site</title>
    </head>
    <body>
        <p>Texte à lire 1</p>
        <p>Texte à lire 2</p>
    </body>
</html>
"""
soup = BeautifulSoup(html_doc,"html.parser")
    
for p in soup.find_all('p'):
    print( p )
