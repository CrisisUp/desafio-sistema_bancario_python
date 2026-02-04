import time
import textwrap
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()
CAMINHO_DATA = os.path.join("data", "usuarios.json")

# --- PERSISTÊNCIA (Nível Global) ---

def salvar_dados(usuarios, contas):
    os.makedirs("data", exist_ok=True)
    dados = {
        "usuarios": [{"cpf": u.cpf, "nome": u.nome, "data_nascimento": u.data_nascimento, "endereco": u.endereco} for u in usuarios],
        "contas": []
    }
    for conta in contas:
        dados["contas"].append({
            "numero": conta._numero,
            "agencia": conta._agencia,
            "saldo": conta._saldo,
            "cpf_cliente": conta._cliente.cpf,
            "historico": conta._historico.transacoes
        })
    with open(CAMINHO_DATA, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_dados():
    if not os.path.exists(CAMINHO_DATA):
        return [], []
    try:
        with open(CAMINHO_DATA, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
            # 1. Recria os objetos PessoaFisica
            usuarios = [PessoaFisica(**u) for u in dados.get("usuarios", [])]
            
            contas = []
            for c in dados.get("contas", []):
                cliente = next((u for u in usuarios if u.cpf == c["cpf_cliente"]), None)
                if cliente:
                    # 2. Recria o objeto ContaCorrente
                    conta = ContaCorrente(c["numero"], cliente)
                    conta._saldo = c["saldo"]
                    
                    # 3. RESTAURA O HISTÓRICO (Essencial para POO)
                    # Pegamos a lista de transações do JSON e injetamos no objeto Historico
                    if "historico" in c:
                        conta._historico._transacoes = c["historico"]
                    
                    contas.append(conta)
                    cliente.adicionar_conta(conta)
            
            return usuarios, contas
    except Exception as e:
        rprint(f"[bold red]Erro ao carregar dados: {e}[/]")
        return [], []

# --- CLASSES POO ---

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self): return self._saldo

    def sacar(self, valor):
        if valor > self._saldo:
            rprint("[bold red]@@@ Saldo insuficiente! @@@[/]\n")
            return False
        if valor > 0:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([t for t in self._historico.transacoes if t["tipo"] == "Saque"])
        if valor > self.limite:
            rprint("[bold red]@@@ Erro: Excede o limite por saque! @@@[/]\n")
        elif numero_saques >= self.limite_saques:
            rprint("[bold red]@@@ Erro: Limite de saques atingido! @@@[/]\n")
        else:
            return super().sacar(valor)
        return False

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self): pass
    @abstractmethod
    def registrar(self, conta): pass

class Saque(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta._historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta._historico.adicionar_transacao(self)

# --- FUNÇÕES DE INTERFACE ---

def menu():
    menu_text = """
    [[bold cyan]d[/]]  Depositar
    [[bold cyan]s[/]]  Sacar
    [[bold cyan]e[/]]  Extrato
    [[bold cyan]nc[/]] Nova Conta
    [[bold cyan]lc[/]] Listar Contas
    [[bold cyan]lu[/]] Listar Usuários
    [[bold cyan]nu[/]] Novo Usuário
    [[bold red]q[/]]  Sair
    """
    console.print(Panel(textwrap.dedent(menu_text), title="[bold blue]SISTEMA POO", expand=False))
    return console.input("[bold yellow]=> [/]").lower().strip()

def obter_entrada_numerica(mensagem, tipo=int):
    try:
        return tipo(console.input(mensagem))
    except ValueError:
        rprint("[bold red]@@@ Erro: Digite um número válido! @@@[/]\n")
        return None

def filtrar_conta(contas, numero_conta):
    return next((c for c in contas if c._numero == numero_conta), None)

def criar_usuario_poo(usuarios):
    cpf = console.input("CPF (somente números): ")
    if any(u.cpf == cpf for u in usuarios):
        rprint("[bold red]@@@ Erro: CPF já cadastrado! @@@[/]\n")
        return
    usuarios.append(PessoaFisica(cpf, console.input("Nome: "), console.input("Nascimento: "), console.input("Endereço: ")))
    rprint("[bold green]=== Usuário criado! ===[/]\n")

def criar_conta_poo(agencia, numero, usuarios, contas):
    cpf = console.input("CPF do titular: ")
    cliente = next((u for u in usuarios if u.cpf == cpf), None)
    if cliente:
        nova_conta = ContaCorrente(numero, cliente)
        contas.append(nova_conta)
        cliente.adicionar_conta(nova_conta)
        rprint("[bold green]=== Conta criada! ===[/]\n")
    else:
        rprint("[bold red]@@@ Usuário não encontrado! @@@[/]\n")

def exibir_extrato_poo(conta):
    table = Table(title=f"EXTRATO C/C {conta._numero}")
    table.add_column("Tipo"); table.add_column("Valor", justify="right")
    for t in conta._historico.transacoes:
        table.add_row(t["tipo"], f"R$ {t['valor']:.2f}")
    console.print(table)
    rprint(f"[bold yellow]Saldo: R$ {conta.saldo:.2f}[/]\n")

def listar_contas(contas):
    for c in contas: rprint(f"C/C: {c._numero} | Titular: {c._cliente.nome}")

def listar_usuarios(usuarios):
    for u in usuarios: rprint(f"Nome: {u.nome} | CPF: {u.cpf}")