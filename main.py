from automation.imgCaptcha import ImgCaptcha
from automation.reCaptcha import ReCaptcha


# Selecionar opções
print("\n• Opções:\n1 - ImageCaptcha\n2 - ReCaptcha")
while True:
    try:
        opcao = int(input("\nEscolha uma das opções: "))
        if opcao != 1 and opcao != 2:
            print("opção indisponível.")
        else:
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
