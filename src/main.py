# src/main.py
from funcoes import *

def main():
    usuarios = []
    contas = []
    LIMITE_SAQUES = 3
    limite = 500
    numero_saques = 0
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(contas)

        elif opcao == "s":
            # Chame a função de saque passando a lista de contas
            sacou = sacar(contas=contas, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            if sacou:
                numero_saques += 1

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nu":
            criar_usuario(usuarios) # Agora 'usuarios' está definido acima!

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

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