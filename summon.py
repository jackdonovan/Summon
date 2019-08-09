from bs4 import BeautifulSoup as bs
import re
import time
import urllib.request as ur


# get your list of urls / sitemap exported from burp
with open("inputFiles/sitemap.txt") as f:
    sites = f.readlines()
sites = [x.strip() for x in sites]

# list of words you want to inlcude as "keys"
with open("inputFiles/keys.txt") as f:
    keyWords = f.readlines()
keyWords = [x.strip() for x in keyWords]


for site in sites:
    for word in keyWords:
        try:
            # retrieves page
            htmlRequest = ur.urlopen(site, timeout=5)
        except HTTPError as e:
            print(e.read())
        # gets page markup
        responseBytes = htmlRequest.read()

        # decode page
        responseDecoded = responseBytes.decode("utf8")
        htmlRequest.close()

        # use b-soup to cleanup and search for words were looking for
        soup = bs(responseDecoded, 'html.parser')
        if(soup.find_all(string=re.compile(word), recursive=True)):
            print(
                "<><><><><><>FOUND<><><><><><>WORD: ", word, "<><><><><><>\n",
                "<> Url to page with key: ", site, "<>\n",
                soup.find_all(string=re.compile(word), recursive=True), "\n",
                "<><><><><><><><><><><><><><><><><><><><><><><><><><> "
            )
        # sleep as to not do too many requests at the same time
        time.sleep(5)
ur.urlcleanup()