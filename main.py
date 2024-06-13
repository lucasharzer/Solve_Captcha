from automation.normalcaptcha import ImgCaptcha
from dotenv import load_dotenv, find_dotenv
from automation.recaptcha import ReCaptcha
import os

# Criar pasta de arquivos
load_dotenv(find_dotenv())
try:
    os.mkdir(os.path.join(os.getcwd(), os.getenv("IMG_PATH")))
except FileExistsError:
    pass
# Selecionar opções
print("\n• Opções:\n1 - ImageCaptcha\n2 - ReCaptcha")
while True:
    try:
        opcao = int(input("\nEscolha uma das opções: "))
        if opcao != 1 and opcao != 2:
            print("opção indisponível.")
        else:
            break
    except KeyboardInterrupt:
        opcao = 0
        print("programa encerrado")
        break
    except ValueError:
        print("opção inválida.")
        
# Navegação
if opcao == 1:
    navegacao = ImgCaptcha()
    navegacao.iniciar_navegacao()
elif opcao == 2:
    navegacao = ReCaptcha()
    navegacao.iniciar_navegacao()
