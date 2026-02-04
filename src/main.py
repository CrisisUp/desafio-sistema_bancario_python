# src/main.py
from funcoes import *

def main():
    usuarios, contas = carregar_dados()

    LIMITE_SAQUES = 3
    LIMITE_VALOR_SAQUE = 500
    NUMERO_SAQUES = 0
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(contas)
            salvar_dados(usuarios, contas)

        elif opcao == "s":
            # Chame a função de saque passando a lista de contas
            sacou = sacar(contas=contas, limite=LIMITE_VALOR_SAQUE, numero_saques=NUMERO_SAQUES, limite_saques=LIMITE_SAQUES)
            if sacou:
                NUMERO_SAQUES += 1

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)
            salvar_dados(usuarios, contas)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                salvar_dados(usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            rprint("[bold red]@@@ Operação inválida! Por favor, selecione novamente a operação desejada. @@@[/]\n")

if __name__ == "__main__":
    main()