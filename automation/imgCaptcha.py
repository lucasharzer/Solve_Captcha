from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twocaptcha import TwoCaptcha
from selenium import webdriver
from time import sleep
import urllib.request
import os


class ImgCaptcha:
    def __init__(self):
        # Variáveis
        load_dotenv(find_dotenv())
        self.url = os.getenv("URL_NORMAL")
        self.api_captcha = os.getenv("API_CAPTCHA")
        self.img_path = os.getenv("IMG_PATH")

        self.class_principal = "Fy-pBtSfc-ohWKkLxXbEn"
        self.class_botao = "_2GdSQFyFsS_fwGYHfE8OsE"
        self.class_form = "YmAJ3qvByGUGe3dLw_PF-"
        self.class_msg_sucesso = "j4U8b8WW7BD_DOSsopoys"
        self.class_msg_fracasso = "_1Or-n9RKBk1X_Bc_vZYSf4"
        self.id_input = "simple-captcha-field"
        self.tag_button = "button"
        self.tag_svg = "svg"
        self.tag_img = "img"

        # Navegador
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def abrir_navegador(self):
        # Entrar no site
        self.driver.get(self.url)
        self.driver.maximize_window()

    def fechar_navegador(self):
        # Sair do site
        self.driver.close()

    def resolver_captcha(self):
        # Encontrar a palavra da imagem
        solver = TwoCaptcha(self.api_captcha)
        result = solver.normal(self.img_path)["code"]
        os.remove(self.img_path)
        return result

    def realizar_teste(self):
        while True:
            # Acessar o campo da imagem
            while True:
                try:
                    div = self.driver.find_element(By.CLASS_NAME, self.class_principal)
                    if div:
                        break
                except:
                    pass
            
            # Fechar aviso de cookies
            try:
                self.driver.find_element(By.CLASS_NAME, self.class_botao).click()
            except:
                pass
            
            # Pegar o link da imagem
            link_img = div.find_element(By.TAG_NAME, self.tag_img).get_attribute("src")

            # Baixar a imagem
            urllib.request.urlretrieve(link_img, self.img_path)

            while True:
                if os.path.exists(self.img_path):
                    break
                else:
                    pass
            
            # Resolver captcha
            print("solving...")
            resultado = self.resolver_captcha()
            
            # Preencher resultado
            campo_resultado = self.driver.find_element(By.ID, self.id_input)
            campo_resultado.send_keys(resultado)

            # Pegar botões
            check = reset = ""
            form = self.driver.find_element(By.CLASS_NAME, self.class_form)
            for botao in form.find_elements(By.TAG_NAME, self.tag_button):
                if "Check" in botao.text:
                    check = botao
                elif "Reset" in botao.text:
                    reset = botao
            
            check.click()

            # Verificar status
            status = 0
            while True:
                try:
                    mensagem_sucesso = self.driver.find_element(By.CLASS_NAME, self.class_msg_sucesso).text
                    if "successfully" in mensagem_sucesso:
                        print(mensagem_sucesso)
                        status = 1
                        break
                except:
                    try:
                        mensagem_fracasso = self.driver.find_element(By.CLASS_NAME, self.class_msg_fracasso).text
                        if "Incorrect" in mensagem_fracasso:
                            print(mensagem_fracasso)
                            status = 2
                            break
                    except:
                        pass
            
            if status == 1:
                break
            else:
                reset.click()

    def iniciar_navegacao(self):
        self.abrir_navegador()
        self.realizar_teste()
        sleep(2)
        self.fechar_navegador()
