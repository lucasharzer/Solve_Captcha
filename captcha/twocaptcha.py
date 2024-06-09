from dotenv import load_dotenv, find_dotenv
from twocaptcha import TwoCaptcha
from time import sleep
import os


class twoCaptcha:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_captcha = os.getenv("2CAPTCHA")
        self.img_path = os.path.join(
            os.getcwd(), os.getenv("IMG_PATH")
        )

    def solve_normal(self):
        # Encontrar a palavra da imagem
        solver = TwoCaptcha(self.api_captcha)
        status_captcha = 0
        while True:
            try:
                resultado = solver.normal(self.img_path)["code"]
                status_captcha = 1
            except Exception as e:
                if str(e) == "ERROR_ZERO_BALANCE":
                    print("O captcha está sem saldo")
                    break
                elif str(e) == "ERROR_KEY_DOES_NOT_EXIST":
                    print("Erro na chave do captcha")
                    break

                sleep(3)

        if status_captcha == 1:
            os.remove(self.img_path)
            return resultado
        else:
            return "erro"

    def solve_recaptcha(self, url, site_key):
        # Fazer o request para receber o token
        solver = TwoCaptcha(self.api_captcha) 
        print("solving...")

        status_captcha = 0
        while True:
            try:
                resultado = solver.recaptcha(
                    sitekey=site_key,
                    url=url
                )
                print("captcha resolvido")
                status_captcha = 1
                break
            except Exception as e:
                if str(e) == "ERROR_ZERO_BALANCE":
                    print("O captcha está sem saldo")
                    break
                elif str(e) == "ERROR_KEY_DOES_NOT_EXIST":
                    print("Erro na chave do captcha")
                    break

                sleep(3)
        
        if status_captcha == 1:
            # Pegar Token
            token = str(resultado["code"])
            return token
        else:
            return "erro"
