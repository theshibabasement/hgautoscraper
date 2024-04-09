import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_sitemap_urls(url):
    sitemap_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_url = urljoin(url, href)
            if is_valid_url(absolute_url) and absolute_url.startswith(url):
                sitemap_urls.append(absolute_url)

    return sitemap_urls

def generate_sitemap(url):
    sitemap_urls = get_sitemap_urls(url)

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for sitemap_url in sitemap_urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{sitemap_url}</loc>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    with open('sitemap.xml', 'w') as file:
        file.write(xml_content)

    print("Sitemap gerado com sucesso!")

# URL do site
url = "https://hgautos.com.br/"

# Gerar o sitemap
generate_sitemap(url)