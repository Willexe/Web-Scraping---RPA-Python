from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from collections import Counter
from SendEmail import enviar_email_com_anexo
from dotenv import load_dotenv
import os

# Configurações do webdriver
def iniciar_driver():  
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Extrai os dados de uma página
def extrair_dados_pagina(driver, url):  
    driver.get(url)
    WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))
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
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print("Dados salvos em quotes.csv")

# Ler e analisa a planilha os dados salvos no arquivo CSV depois separa: Total de citações, Autor mais recorrente, Tag mais usada
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

    # Criação das colunas e linhas da planilha Resumo_analise
    resumo_dict = {
        "Descrição": ["Total de citações", "Autor mais recorrente", "Tag mais usada"],
        "Valor": [total_citacoes, autor_mais_recorrente, tag_mais_comum],
        "Quantidade": ["", autor_qtd, tag_qtd]
    }

    # Retorno no console dos dados: Total de citações, Autor mais recorrente, Tag mais usada
    print(f"Total de citações: {total_citacoes}")
    print(f"Autor mais recorrente: {autor_mais_recorrente} ({autor_qtd} vezes)")
    print(f"Tag mais utilizada: {tag_mais_comum} ({tag_qtd} vezes)")

    # Criação da planilha
    resumo_df = pd.DataFrame(resumo_dict)
    resumo_df.to_csv("Resumo_analise.csv", index=False, encoding="utf-8-sig")
    print("Resumo Salvo em resumo_analise.csv")
    return total_citacoes, autor_mais_recorrente, autor_qtd, tag_mais_comum, tag_qtd

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

    # Captura as variavéis da função leitura_e_analise para usar no body do email
    total, autor, autor_vezes, tag, tag_vezes = leitura_e_analise()
    
    leitura_e_analise()
    driver.quit()

    # Titulo do email
    subject = "Web-Scraping - RPA-Python - Desafio"

    # Descrição
    body = (
        "Prezado,\n\n"
        "Segue em anexo os arquivos `quotes.csv` com as citações coletadas e `Resumo_analise.csv` com o resumo de dados.\n"
        f"Resumo da análise:\n\n"
        f"Total de citações: {total}\n"
        f"Autor mais recorrente: {autor}({autor_vezes} vezes)\n"
        f"Tag mais utilizada: {tag} ({tag_vezes} vezes)\n\n"
        "Atenciosamente,\n"
        "William Barbosa"
    )

    # Carrega os arquivos .env (Armazena credenciais sensíveis)
    load_dotenv()

    # Pega os dados salvos no .env
    sender_email = os.getenv("EMAIL_REMETENTE")
    password = os.getenv("SENHA")
    receiver_email = os.getenv("EMAIL_DESTINATARIOS").split(",")
    
    # Chama a função no SendEmail.py com os dados sensivéis (Email's e Senha) do .env
    enviar_email_com_anexo(
        sender=sender_email,
        password=password,
        recipient=receiver_email,
        subject=subject,
        body=body,
        arquivos= ["quotes.csv", "Resumo_analise.csv"]
    )
if __name__ == "__main__":
    main()