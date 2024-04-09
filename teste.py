import psycopg2
import requests
from bs4 import BeautifulSoup

# Configurações de conexão com o banco de dados PostgreSQL
db_url = "postgres://postgres:Senha123!@easy.limemarketing.online:9001/chatbots-solucoes-globais"

# Estabelecer a conexão com o banco de dados
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# Consultar os links dos carros na base de dados
select_query = "SELECT id, link FROM produtos LIMIT 5"
cursor.execute(select_query)
carros = cursor.fetchall()

# Iterar sobre os carros e fazer o web scraping
for carro in carros:
    carro_id = carro[0]
    link = carro[1]

    # Fazer a requisição HTTP para obter o HTML da página
    response = requests.get(link)
    html = response.text

    # Analisar o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extrair os valores de preço antigo e preço de desconto
    preco_antigo = None
    preco_desconto = None

    # Tentar encontrar os elementos de preço usando diferentes seletores CSS
    selectors_preco_antigo = [
        '.preco-antigo span',
        '.preco-antigo-detalhe span',
        'h2.preco-antigo span',
        'h2.text-right span'
    ]

    selectors_preco_desconto = [
        '.preco-detalhe span',
        '.indigo-text span',
        'h2.text-right span'
    ]

    for selector in selectors_preco_antigo:
        element = soup.select_one(selector)
        if element:
            preco_antigo = element
            break

    for selector in selectors_preco_desconto:
        element = soup.select_one(selector)
        if element:
            preco_desconto = element
            break

    if preco_antigo and preco_desconto:
        valor = preco_antigo.text.strip().replace('R$', '').replace('.', '').replace(',', '.')
        valor_desconto = preco_desconto.text.strip().replace('R$', '').replace('.', '').replace(',', '.')

        # Atualizar os campos de valor e valor de desconto na base de dados
        update_query = "UPDATE produtos SET valor = %s, valor_desconto = %s WHERE id = %s"
        cursor.execute(update_query, (valor, valor_desconto, carro_id))
        conn.commit()

        print(f"Dados atualizados para o carro ID: {carro_id}")
    else:
        print(f"Não foi possível extrair os preços para o carro ID: {carro_id}")

# Fechar a conexão com o banco de dados
cursor.close()
conn.close()
