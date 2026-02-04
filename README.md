# 🏦 Sistema Bancário em Python (Versão POO)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Este projeto consiste em um sistema bancário robusto desenvolvido para a trilha Python da DIO. A aplicação utiliza **Programação Orientada a Objetos (POO)** e interface estilizada via biblioteca `Rich`, com foco em segurança e organização de código

## 📋 Convenções Técnicas Utilizadas

### Neste projeto, o uso de caracteres especiais foi fundamental para a arquitetura

### 1. O uso do Asterisco (`*`) nas Funções

### Nas funções de transação, como o saque, utilizamos a sintaxe de **Keyword-only arguments** (Argumentos apenas nomeados):

- **Exemplo:** `def sacar(*, contas, limite, ...)`
- **Por que usamos?** O `*` obriga que, ao chamar a função, o desenvolvedor nomeie cada parâmetro (ex: `limite=500`). Isso evita confusões entre valores numéricos, garantindo que um "limite" não seja passado acidentalmente no lugar de um "valor".

### 2. O uso da Hashtag (`#`) no Código

- **Comentários de Implementação:** No arquivo `funcoes.py`, utilizamos o `#` para documentar a lógica interna e separar blocos de código.
- **Hierarquia de Documentação:** Neste arquivo README, o `#` define a estrutura de seções e subseções.

---

## 🚀 Funcionalidades

- **Gerenciamento de Usuários:** Cadastro de Clientes (Pessoa Física) com validação de CPF.
- **Gerenciamento de Contas:** Criação de Contas Correntes vinculadas a usuários.
- **Transações Bancárias:** Depósitos e Saques processados via objetos de classe.
- **Extrato Detalhado:** Histórico de transações persistente e formatado em tabelas.
- **Persistência de Dados:** Uso de arquivos JSON para salvar o estado entre sessões.

## 🏗️ Arquitetura POO

### O sistema aplica os quatro pilares da POO:

### 1. **Abstração:** Uso da classe `Transacao(ABC)` para padronizar operações.

### 2. **Herança:** `PessoaFisica` herda de `Cliente` e `ContaCorrente` herda de `Conta`.

### 3. **Encapsulamento:** Atributos como `_saldo` e `_historico` são protegidos.

### 4. **Polimorfismo:** Diferentes tipos de transação registram-se de forma única no histórico.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Rich:** Interface CLI (Tabelas, Painéis e Spinners).
- **JSON:** Armazenamento local na pasta `data/`.

## 📦 Instalação e Execução

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/desafio-sistema_bancario_python.git](https://github.com/seu-usuario/desafio-sistema_bancario_python.git)
   cd desafio-sistema_bancario_python
   ```

Instale a biblioteca Rich:

```bash
pip install rich
````

Execute a aplicação:

```bash
python src/main.py
````

📁 Estrutura de Pastas

```plaintext
.
├── data/               # Armazena o arquivo usuarios.json
├── src/                # Código fonte
│   ├── main.py         # Fluxo principal do programa
│   └── funcoes.py      # Classes POO e lógica de interface
└── README.md 
```

## Documentação do projeto

👤 Autor
Cristiano - <https://github.com/CrisisUp/desafio-sistema_bancario_python.git>
