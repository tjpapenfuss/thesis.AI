import re

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

def cleanURL(URL):
    try:
       URL = URL.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    
    #format entry to enable netloc parse
    if not (URL.startswith('//') or URL.startswith('http://') or URL.startswith('https://')):URL = '//' + URL
    URL = urlparse(URL).netloc
    URL = URL.lower()
    #remove www
    w = "www."
    if w in URL:
        URL = URL.replace("www.","")
    else:
        URL = URL
    return(URL)

def clean_page(URL,domain=None):
    try:
        URL = URL.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    primary = cleanURL(URL)
    secondary = urlparse(URL).path
    if primary == '':
    	primary = cleanURL(domain)       
    return(primary+secondary)

