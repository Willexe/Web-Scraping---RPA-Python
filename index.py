from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = "https://quotes.toscrape.com/js-delayed/page/{}/" #URL para web scraping

page = 1 # Conta paginas
dados = [] # Lista de dados

while True:
    try:
        # Acessa a url
        driver.get(url.format(page))
        
        # Espera para carregar as citações
        time.sleep(11) 

        # Encontra a class "quote""
        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        # Percorre o site pegando os dados (Citação, Autor, Tags)
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tag = quote.find_element(By.CLASS_NAME, "tags").text
            print(f"{text}")
            print(f"{author}")
            print(f"{tag}")

            # Armazena os dados na lista
            dados.append({
                'Citação': text,
                'Autor': author,
                'Tags': tag
            })

        # Avança para as proximas páginas
        try:
            next_button = driver.find_element(By.CLASS_NAME, "next")
            page += 1
            time.sleep(1.5)
        except:
            break
    except:
        break

# Cria DataFrame e salva como CSV
df = pd.DataFrame(dados)
df.to_csv("quotes.csv", index=False, encoding="utf-8")

time.sleep(100)