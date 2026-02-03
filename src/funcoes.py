import time
import textwrap
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

# --- UTILITÁRIOS (Reutilização de Código) ---

def obter_entrada_numerica(mensagem, tipo=int):
    """Garante que a entrada seja um número e evita quebras por letras."""
    try:
        valor = console.input(mensagem)
        return tipo(valor)
    except ValueError:
        rprint("[bold red]@@@ Erro: Entrada inválida! Digite apenas números. @@@[/]\n")
        return None

def filtrar_conta(contas, numero_conta):
    """Busca uma conta na lista pelo número."""
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)
    if not conta:
        rprint("[bold yellow]@@@ Erro: Conta não encontrada! @@@[/]\n")
    return conta

def processar_operacao(mensagem="Processando..."):
    with console.status(f"[bold green]{mensagem}") as status:
        time.sleep(1.2)

# --- FUNÇÕES PRINCIPAIS ---

def menu():
    menu_text = """
    [[bold cyan]d[/]]  Depositar
    [[bold cyan]s[/]]  Sacar
    [[bold cyan]e[/]]  Extrato
    [[bold cyan]nc[/]] Nova Conta
    [[bold cyan]lc[/]] Listar Contas
    [[bold cyan]lu[/]] Listar Usuários
    [[bold cyan]nu[/]] [blue]Novo Usuário[/]
    [[bold red]q[/]]  Sair
    """
    console.print(Panel(textwrap.dedent(menu_text), title="[bold blue]MENU SISTEMA BANCÁRIO", expand=False))
    return console.input("[bold yellow]=> [/]").lower().strip()

def depositar(contas):
    numero_conta = obter_entrada_numerica("Informe o número da conta: ")
    if numero_conta is None: return

    conta = filtrar_conta(contas, numero_conta)
    if not conta: return

    valor = obter_entrada_numerica(f"Valor do depósito para [bold cyan]{conta['usuario']['nome']}[/]: ", float)
    
    if valor and valor > 0:
        processar_operacao("Registrando depósito...")
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        rprint(f"[bold green]=== Depósito de R$ {valor:.2f} realizado com sucesso! ===[/]\n")
    else:
        rprint("[bold red]@@@ Operação falhou! Valor inválido. @@@[/]\n")

def sacar(*, contas, limite, numero_saques, limite_saques):
    numero_conta = obter_entrada_numerica("Informe o número da conta para saque: ")
    if numero_conta is None: return False

    conta = filtrar_conta(contas, numero_conta)
    if not conta: return False

    valor = obter_entrada_numerica("Informe o valor do saque: ", float)
    if valor is None: return False

    saldo = conta.get("saldo", 0)
    
    if valor > saldo:
        rprint("[bold red]@@@ Erro: Saldo insuficiente. @@@[/]\n")
    elif valor > limite:
        rprint("[bold red]@@@ Erro: O valor excede o limite por saque. @@@[/]\n")
    elif numero_saques >= limite_saques:
        rprint("[bold orange]@@@ Erro: Limite máximo de saques atingido. @@@[/]\n")
    elif valor > 0:
        processar_operacao("Contando notas...")
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        rprint("[bold green]=== Saque realizado com sucesso! ===[/]\n")
        return True
    
    return False

def exibir_extrato(contas):
    numero_conta = obter_entrada_numerica("Informe o número da conta para extrato: ")
    if numero_conta is None: return

    conta = filtrar_conta(contas, numero_conta)
    if conta:
        table = Table(title=f"\nEXTRATO - Conta {numero_conta}", title_style="bold blue")
        table.add_column("Descrição", style="cyan")
        table.add_column("Valor", justify="right", style="green")

        movimentacoes = conta.get("extrato", "").split("\n")
        for mov in movimentacoes:
            if mov and ":" in mov:
                desc, val = mov.split(":")
                table.add_row(desc.strip(), val.strip())

        console.print(table)
        rprint(f"\n[bold yellow]Saldo Atual:[/][bold green] R$ {conta['saldo']:.2f}[/]")
        rprint(f"[bold white]Titular:[/][italic] {conta['usuario']['nome']}[/]")

def criar_usuario(usuarios):
    cpf = console.input("Informe o CPF (somente números): ")
    
    if not (cpf.isdigit() and len(cpf) == 11):
        rprint("[bold red]@@@ Erro: CPF inválido! Deve conter 11 dígitos. @@@[/]\n")
        return

    if any(u["cpf"] == cpf for u in usuarios):
        rprint("[bold red]@@@ Erro: Já existe um usuário com este CPF! @@@[/]\n")
        return

    nome = console.input("Nome completo: ")
    data_nasc = console.input("Data de nascimento (dd-mm-aaaa): ")
    endereco = console.input("Endereço (logradouro, nro - bairro - cidade/sigla): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nasc, "cpf": cpf, "endereco": endereco})
    rprint("[bold green]=== Usuário criado com sucesso! ===[/]\n")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = console.input("Informe o CPF do usuário: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario:
        processar_operacao("Gerando conta...")
        rprint("[bold green]=== Conta criada com sucesso! ===[/]\n")
        return {
            "agencia": agencia, 
            "numero_conta": numero_conta, 
            "usuario": usuario, 
            "saldo": 0, 
            "extrato": ""
        }
    
    rprint("[bold red]@@@ Usuário não encontrado! @@@[/]\n")
    return None

def listar_contas(contas):
    if not contas:
        rprint("[bold yellow]Não há contas cadastradas.[/]\n")
        return
    table = Table(title="CONTAS ATIVAS")
    table.add_column("Agência", style="magenta")
    table.add_column("C/C", style="yellow")
    table.add_column("Titular", style="white")
    for c in contas:
        table.add_row(c['agencia'], str(c['numero_conta']), c['usuario']['nome'])
    console.print(table)

def listar_usuarios(usuarios):
    if not usuarios:
        rprint("[bold yellow]Não há usuários cadastrados.[/]\n")
        return
    table = Table(title="USUÁRIOS CADASTRADOS", title_style="bold magenta")
    table.add_column("Nome", style="cyan")
    table.add_column("CPF", style="yellow")
    table.add_column("Endereço", style="green")
    for u in usuarios:
        table.add_row(u["nome"], u["cpf"], u["endereco"])
    console.print(table)