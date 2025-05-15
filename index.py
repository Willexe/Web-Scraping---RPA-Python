from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

def iniciar_driver():  # Configurações do webdriver
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extrair_dados_pagina(driver, url):  # Extrai os dados de uma página
    driver.get(url)
    time.sleep(11)
    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    dados = []

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tag = quote.find_element(By.CLASS_NAME, "tags").text
        print(f"{text}")
        print(f"{author}")
        print(f"{tag}")

        dados.append({
            'Citação': text,
            'Autor': author,
            'Tags': tag
        })

    return dados

def proxima_pagina(driver):  # Verifica se existe botão "Next"
    try:
        driver.find_element(By.CLASS_NAME, "next")
        return True
    except:
        return False

def salvar_em_csv(dados, nome_arquivo="quotes.csv"):  # Salva os dados em CSV
    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8")
    print("Citações salvas em quotes.csv")

def main(): # Percorre todas as paginas e extrai os dados
    driver = iniciar_driver()
    base_url = "https://quotes.toscrape.com/js-delayed/page/{}/"
    page = 1
    todas_citacoes = []

    while True:
        dados = extrair_dados_pagina(driver, base_url.format(page))
        todas_citacoes.extend(dados)

        if proxima_pagina(driver):
            page += 1
            time.sleep(1.5)
        else:
            break
    salvar_em_csv(todas_citacoes)
    time.sleep(10)



if __name__ == "__main__":
    main()