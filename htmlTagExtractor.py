
#for extracting links which are stored under <a> tag using BeautifulSoup
from bs4 import BeautifulSoup
from urllib.parse import urljoin

extracted_url = set()

#Extract href value(links) from <a> tag
def find_a_tag(htmltext, base_url):
    soup = BeautifulSoup(htmltext, 'html.parser')
    for tag in soup.findAll('a', href=True):
            url = urljoin(base_url, tag['href'])
            extracted_url.add(url)

def fetch_url():
    return extracted_url
