# Descrição
Web scraping, também conhecido como "raspagem da web", é o processo de extração automática de dados de sites da internet. É uma técnica usada para coletar informações publicamente disponíveis, geralmente com a ajuda de scripts ou programas, e transformá-las em dados estruturados para posterior análise.

# Sobre o projeto
Esse projeto de automação em Python coleta as Citações, Autores e Tags contidas no site _https://quotes.toscrape.com/js-delayed/page/1/_ por meio do Selenium  (Framework de automação de navegador de código aberto que permite aos usuários automatizar interações com navegadores web).
Após coletar os dados utiliza-se o Pandas (Biblioteca Python de código aberto usada para manipulação e análise de dados) para gerar uma planilha com os dados e analisar a quantidade de citações, o autor mais recorrente e a tag mais utilizada.
No final envia os arquivos por e-mail com o resumo no corpo da mensagem e a planilha feita no Pandas em anexo.

# Tecnologias utilizadas
- Python 3.x
- Selenium
- Pandas
- Python-dotenv
- SMTP (envio de e-mails)

# Instruções


#### Para executar o programa da melhor forma é necessario:
* Instalar o Python
* Instalar o Selenium (pip install selenium)
* Instalar o Pandas (pip install pandas)

pip install -r requirements.txt 

(Irá instalar todas as dependêcias)

#### No arquivo .env substitua o e-mail do remetente, senha (Para contas Gmail, ative a autenticação de dois fatores e crie uma senha de aplicativo), e-mail do destinatário, após isso coloque .env no gitignore para que suas credencias não sejam colocadas no GitHub

#### Por fim execute o projeto no terminal
- python index.py

#### Ao final, os arquivos quotes.csv e Resumo_analise.csv serão gerados e enviados por e-mail.
