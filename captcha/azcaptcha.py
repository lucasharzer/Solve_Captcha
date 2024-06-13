from dotenv import load_dotenv, find_dotenv
from azcaptchaapi import AZCaptchaApi
from time import sleep
import requests
import os


class azCaptcha:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_captcha = os.getenv("AZCAPTCHA")
        self.img_path = os.path.join(
            os.getcwd(), os.getenv("IMG_PATH")
        )

    def solve_normal(self):
        # Encontrar a palavra da imagem
        solver = AZCaptchaApi(self.api_captcha)
        status_captcha = 0
        while True:
            try:
                with open(self.img_path, "rb") as captcha_file:
                    resultado = solver.solve(captcha_file).await_result()
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
            os.remove(self.img_path)
            return resultado
        else:
            return "erro"

    def solve_recaptcha(self, url, site_key):
        # Fazer o request para receber o token
        limite = 0
        while True:
            limite += 1
            # Primeira requisição para obter o captcha_id
            print("captcha_id...")
            endpoint_in = f"{self.endpoint}/in.php"
            data_id = {
                "key": self.apikey,
                "method": "userrecaptcha",
                "googlekey": site_key,
                "pageurl": url,
                "json": 1
            }

            status_captcha = captcha_id = 0
            while True:
                try:
                    response = requests.post(endpoint_in, data=data_id)
                    if response.ok:
                        result = response.json()
                        if result["status"] == 1:
                            captcha_id = result["request"]
                            print(f"captcha_id: {captcha_id}")
                            status_captcha = 1
                            break
                        elif result["request"] == "ERROR_USER_BALANCE_ZERO":
                            print("o captcha está sem saldo")
                            break
                        elif result["request"] == "ERROR_WRONG_USER_KEY":
                            print("Erro na chave do captcha")
                            break
                        elif result["request"] == "ERROR_TODAY_NO_SLOT_AVAILABLE_UPGRAGE_PACKAGE_OR_CHANGE_TO_USE_BALANCE":
                            print("Nenhum slot disponível hoje. Atualize seu pacote ou mude para usar o saldo disponível")
                            break
                except Exception as e:
                    print(f"Erro ao tentar obter o captcha_id: {e}")
                    
                    sleep(3)
            
            if status_captcha == 1:
                # Segunda requisição usando o captcha_id para obter o token
                print("token...")
                endpoint_res = f"{self.endpoint}/res.php"
                data_token = {
                    "key": self.apikey,
                    "action": "get",
                    "id": captcha_id
                }

                token = ""
                repetir = 0
                while True:
                    try:
                        response = requests.post(endpoint_res, data=data_token)
                        # sleep(20) # Tempo mínimo para o retorno do token
                        if response.text != "CAPCHA_NOT_READY" and "OK|" in response.text:
                            token = str(response.text).replace("OK|", "").strip()
                            break
                        elif response.text in ["ERROR_INVALID_SITEKEY", "ERROR_CAPTCHA_UNSOLVABLE"]:
                            print("\nrepetindo...")
                            repetir = 1
                            break
                        else:
                            print(f"\r{response.text}", end="", flush=True)
                    except Exception as e:
                        print(f"\rErro ao tentar obter o token: {e}", end="", flush=True)

                        sleep(3)
                
                if repetir != 1:
                    return token
            else:
                # Erro impossibilitando resolver o captcha
                return "erro"
            
            if limite == 5:
                # Excedeu o limite de tentativas para resolver o captcha
                return "erro"
