# src/main.py
from funcoes import *

def main():
    # Tenta carregar os dados. Se a função não for encontrada, o erro aparece aqui.
    usuarios, contas = carregar_dados()

    AGENCIA = "0001" 

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = obter_entrada_numerica("Informe o número da conta: ")
            if numero_conta:
                conta = filtrar_conta(contas, numero_conta)
                if conta:
                    valor = obter_entrada_numerica("Informe o valor do depósito: ", float)
                    transacao = Deposito(valor)
                    # Na POO, acessamos o cliente da conta para realizar a transação
                    conta._cliente.realizar_transacao(conta, transacao)
                    salvar_dados(usuarios, contas)

        elif opcao == "s":
            numero_conta = obter_entrada_numerica("Informe o número da conta: ")
            if numero_conta:
                conta = filtrar_conta(contas, numero_conta)
                if conta:
                    valor = obter_entrada_numerica("Informe o valor do saque: ", float)
                    transacao = Saque(valor)
                    conta._cliente.realizar_transacao(conta, transacao)
                    salvar_dados(usuarios, contas)

        elif opcao == "e":
            numero_conta = obter_entrada_numerica("Informe o número da conta para extrato: ")
            if numero_conta:
                conta = filtrar_conta(contas, numero_conta)
                if conta:
                    exibir_extrato_poo(conta)

        elif opcao == "nu":
            criar_usuario_poo(usuarios)
            salvar_dados(usuarios, contas)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta_poo(AGENCIA, numero_conta, usuarios, contas)
            salvar_dados(usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            rprint("[bold blue]Saindo...[/]\n")
            break

if __name__ == "__main__":
    main()