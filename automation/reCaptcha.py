from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.by import By
# - Captcha usado (2Captcha)
from captcha.twocaptcha import twoCaptcha
# - Captcha alternativo (AzCaptcha)
# from captcha.azcaptcha import azCaptcha
from selenium import webdriver
from time import sleep
import os


class ReCaptcha:
    def __init__(self):
        # Variáveis
        load_dotenv(find_dotenv())
        self.url = os.getenv("URL_RECAPTCHA")
        self.api_captcha = os.getenv("API_CAPTCHA")

        self.tag_iframe = "iframe"
        self.id_enviar = "recaptcha-demo-submit"
        self.class_sucesso = "recaptcha-success"

        # Navegador
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # - Captcha usado (2Captcha)
        self.twocaptcha = twoCaptcha()
        # - Captcha alternativo (AzCaptcha)
        # self.azcaptcha = azCaptcha()

    def abrir_navegador(self):
        # Entrar no site
        self.driver.get(self.url)
        self.driver.maximize_window()

    def fechar_navegador(self):
        # Sair do site
        self.driver.close()

    def resolver_captcha(self, site_key):
        # - Captcha usado (2Captcha)
        result = self.twocaptcha.solve_recaptcha(self.url, site_key)
        # - Captcha usado (2Captcha)
        # result = self.azcaptcha.solve_recaptcha(self.url, site_key)
        # Colocar o token no site
        self.driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = " + "'" + result + "'")

    def realizar_teste(self):
        # Pegar o link do captcha
        while True:
            try:
                link_captcha = ""
                iframes = self.driver.find_elements(By.TAG_NAME, self.tag_iframe)
                for iframe in iframes:
                    if iframe.get_attribute("title") == "reCAPTCHA":
                        link_captcha = iframe.get_attribute("src") 
                        
                if len(link_captcha) != 0:
                    break
            except:
                pass
        
        # Pegar o site key do captcha
        site_key = str(link_captcha[link_captcha.find("&k=")+3:link_captcha.find("&co=")]).strip()

        # Resolver captcha
        self.resolver_captcha(site_key)

        # Clicar em Enviar
        enviar = self.driver.find_element(By.ID, self.id_enviar)
        enviar.click()

        while True:
            try:
                msg_sucesso = self.driver.find_element(By.CLASS_NAME, self.class_sucesso).text
                if msg_sucesso:
                    print(msg_sucesso)
                    break
            except:
                pass
        
        sleep(2)
            
    def iniciar_navegacao(self):
        self.abrir_navegador()
        self.realizar_teste()
        self.fechar_navegador()
