from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
input("Pressione Enter para fechar o navegador...")

driver.quit()
