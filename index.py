from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from collections import Counter

# Configurações do webdriver
def iniciar_driver():  
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Extrai os dados de uma página
def extrair_dados_pagina(driver, url):  
    driver.get(url)
    time.sleep(11)
    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    dados = []

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tags = ", ".join([tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")])
        print(f"{text}")
        print(f"{author}")
        print(f"{tags}")

        dados.append({
            'Citação': text,
            'Autor': author,
            'Tags': tags
        })

    return dados

# Verifica se existe botão "Next"
def proxima_pagina(driver):  
    try:
        driver.find_element(By.CLASS_NAME, "next")
        return True
    except:
        return False
    
# Salva os dados em CSV
def salvar_em_csv(dados, nome_arquivo="quotes.csv"):  
    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8")
    print("Dados salvos em quotes.csv")

# Ler e analisa a planilha os dados salvos no arquivo CSV depois retorna os dados solicitados
def leitura_e_analise(): 
    df = pd.read_csv("quotes.csv")
    total_citacoes = len(df)
    autor_mais_recorrente = df["Autor"].value_counts().idxmax()
    autor_qtd = df["Autor"].value_counts().max()

    todas_tags = []
    for tags in df["Tags"]:
        tags_separadas = [tag.strip() for tag in str(tags).split(',')]
        todas_tags.extend(tags_separadas)

    tag_mais_comum, tag_qtd = Counter(todas_tags).most_common(1)[0]

    print(f"Total de citações: {total_citacoes}")
    print(f"Autor mais recorrente: {autor_mais_recorrente} ({autor_qtd} vezes)")
    print(f"Tag mais utilizada: {tag_mais_comum} ({tag_qtd} vezes)")
    
# Percorre todas as paginas, extrai os dados, salva em csv, lê a planilha e processa os dados
def main(): 
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
    leitura_e_analise()
    driver.quit()
    
if __name__ == "__main__":
    main()