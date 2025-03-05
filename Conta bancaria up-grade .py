from datetime import datetime
from typing import List

class ContaBancaria:
    """Classe que representa uma conta bancária com operações básicas."""
    
    def __init__(self, titular: str):
        self.titular = titular.strip().title()
        self._saldo = 0.0
        self._historico: List[str] = []
        self._taxa_saque = 2.0
        self._limite_saque_diario = 1000.0

    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta."""
        return self._saldo

    def _registrar_operacao(self, mensagem: str) -> None:
        """Registra uma operação no histórico com data e hora."""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._historico.append(f"[{data_hora}] {mensagem}")

    def depositar(self, valor: float) -> bool:
        """Realiza um depósito na conta."""
        try:
            if valor <= 0:
                raise ValueError("O valor do depósito deve ser positivo.")
            self._saldo += valor
            self._registrar_operacao(f"Depósito: R$ {valor:.2f}")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def sacar(self, valor: float) -> bool:
        """Realiza um saque da conta com taxa."""
        try:
            if valor <= 0:
                raise ValueError("O valor do saque deve ser positivo.")
            custo_total = valor + self._taxa_saque
            if custo_total > self._saldo:
                raise ValueError("Saldo insuficiente para realizar o saque.")
            if valor > self._limite_saque_diario:
                raise ValueError(f"Limite de saque diário é R$ {self._limite_saque_diario:.2f}")
            
            self._saldo -= custo_total
            self._registrar_operacao(f"Saque: R$ {valor:.2f} (Taxa: R$ {self._taxa_saque:.2f})")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def extrato(self) -> None:
        """Exibe o extrato completo da conta."""
        print(f"\n=== Extrato da Conta de {self.titular} ===")
        if not self._historico:
            print("Nenhuma operação realizada ainda.")
        else:
            for operacao in self._historico:
                print(operacao)
        print(f"Saldo atual: R$ {self._saldo:.2f}")
        print("=" * 40)

def obter_valor(mensagem: str) -> float:
    """Obtém um valor numérico do usuário com validação."""
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Por favor, digite um valor numérico válido.")

def menu_operacoes() -> str:
    """Exibe o menu e retorna a opção escolhida."""
    print("\n=== Sistema Bancário ===")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Ver Extrato")
    print("4. Sair")
    return input("Escolha uma operação (1-4): ").strip()

def main():
    """Função principal do sistema bancário."""
    print("Bem-vindo ao Sistema Bancário!")
    while True:
        try:
            nome = input("Digite o nome do titular da conta: ").strip()
            if not nome:
                raise ValueError("O nome não pode ser vazio.")
            break
        except ValueError as e:
            print(f"Erro: {e}")

    conta = ContaBancaria(nome)
    print(f"Conta criada com sucesso para {conta.titular}!")

    operacoes = {
        '1': lambda: conta.depositar(obter_valor("Valor a depositar: R$ ")),
        '2': lambda: conta.sacar(obter_valor("Valor a sacar: R$ ")),
        '3': conta.extrato,
        '4': lambda: "sair"
    }

    while True:
        opcao = menu_operacoes()
        
        if opcao in operacoes:
            if opcao == '4':
                print(f"Obrigado por usar nossos serviços, {conta.titular}!")
                break
            resultado = operacoes[opcao]()
            if resultado is True:
                print("Operação realizada com sucesso!")
        else:
            print("Opção inválida! Por favor, escolha entre 1 e 4.")

if __name__ == "__main__":
    main()