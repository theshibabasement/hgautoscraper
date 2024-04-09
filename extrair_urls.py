import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse

# URL base do site
base_url = "https://hgautos.com.br/carros/"
# Lista para armazenar as URLs encontradas
urls_encontradas = []

# Função para extrair as URLs de uma página
def extrair_urls(url):
    print(f"Extraindo URLs da página: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            # Verificar se a URL é relativa ou absoluta
            if not urlparse(href).netloc:
                # Converter URL relativa em absoluta
                href = urljoin(base_url, href)
            # Adicionar a URL à lista se pertencer ao mesmo domínio
            if urlparse(href).netloc == urlparse(base_url).netloc and href.startswith(base_url):
                urls_encontradas.append(href)
                print(f"URL encontrada: {href}")

# Função para percorrer as páginas e extrair as URLs recursivamente
def percorrer_paginas(url):
    extrair_urls(url)

    # Verificar as URLs encontradas e percorrer as páginas ainda não visitadas
    for url in urls_encontradas:
        if url not in visitadas:
            visitadas.add(url)
            print(f"Visitando página: {url}")
            percorrer_paginas(url)

# Conjunto para armazenar as URLs visitadas
visitadas = set()

# Iniciar a extração de URLs a partir da página inicial
print(f"Iniciando a extração de URLs a partir da página: {base_url}")
percorrer_paginas(base_url)

# Remover duplicatas da lista de URLs encontradas
urls_encontradas = list(set(urls_encontradas))

# Salvar as URLs em um arquivo CSV
with open('urls.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    writer.writerows([[url] for url in urls_encontradas])

print(f"Extração concluída. {len(urls_encontradas)} URLs foram salvas no arquivo 'urls.csv'.")
