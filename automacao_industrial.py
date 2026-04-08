import os #Importação para uso do comando de limpar tela

class SistemaAutomacaoIndustrial:
    def __init__(self):
        # Configurações de qualidade
        self.PESO_MIN = 95
        self.PESO_MAX = 105
        self.CORES_PERMITIDAS = ["azul", "verde"]
        self.COMPRIMENTO_MIN = 10
        self.COMPRIMENTO_MAX = 20
        self.CAPACIDADE_CAIXA = 10

        # Armazenamento de dados
        self.pecas_aprovadas = []
        self.pecas_reprovadas = [] # Lista de dicionários com {id, motivos, dados}
        self.caixas = []

    def validar_peca(self, peca):
        """
        Avalia se uma peça atende aos critérios de qualidade.
        Retorna (True, []) se aprovada ou (False, [motivos]) se reprovada.
        """
        motivos = []
        
        # Validação de Peso
        if not (self.PESO_MIN <= peca['peso'] <= self.PESO_MAX):
            motivos.append(f"Peso fora do limite ({peca['peso']}g)")
            
        # Validação de Cor
        if peca['cor'].lower() not in self.CORES_PERMITIDAS:
            motivos.append(f"Cor não permitida ({peca['cor']})")
            
        # Validação de Comprimento
        if not (self.COMPRIMENTO_MIN <= peca['comprimento'] <= self.COMPRIMENTO_MAX):
            motivos.append(f"Comprimento fora do limite ({peca['comprimento']}cm)")
            
        return (not motivos, motivos)

    def adicionar_peca(self, peca):
        """Processa uma única peça e a encaminha para aprovação ou reprovação."""
        # Verificar se o ID já existe para evitar duplicatas
        todos_ids = [p['id'] for p in self.pecas_aprovadas] + [p['id'] for p in self.pecas_reprovadas]
        if peca['id'] in todos_ids:
            return False, "Erro: ID já cadastrado no sistema."

        aprovada, motivos = self.validar_peca(peca)
        
        if aprovada:
            self.pecas_aprovadas.append(peca)
            # Lógica de embalagem (caixas)
            if not self.caixas or len(self.caixas[-1]) >= self.CAPACIDADE_CAIXA:
                self.caixas.append([peca])
            else:
                self.caixas[-1].append(peca)
            return True, "Peça APROVADA e enviada para embalagem."
        else:
            self.pecas_reprovadas.append({
                "id": peca['id'],
                "motivos": motivos,
                "dados": peca
            })
            return True, f"Peça REPROVADA. Motivos: {', '.join(motivos)}"

    def remover_peca(self, id_peca):
        """Remove uma peça do sistema pelo ID (aprovada ou reprovada)."""
        # Tentar remover das reprovadas
        for i, p in enumerate(self.pecas_reprovadas):
            if p['id'] == id_peca:
                self.pecas_reprovadas.pop(i)
                return True

        # Tentar remover das aprovadas e atualizar caixas
        encontrada = False
        for i, p in enumerate(self.pecas_aprovadas):
            if p['id'] == id_peca:
                self.pecas_aprovadas.pop(i)
                encontrada = True
                break
        
        if encontrada:
            # Reconstruir as caixas para manter a integridade (re-empacotar tudo)
            novas_caixas = []
            for p in self.pecas_aprovadas:
                if not novas_caixas or len(novas_caixas[-1]) >= self.CAPACIDADE_CAIXA:
                    novas_caixas.append([p])
                else:
                    novas_caixas[-1].append(p)
            self.caixas = novas_caixas
            return True

        return False
    def gerar_relatorio(self):
        """Gera o relatório final consolidado."""
        print("\n" + "="*50)
        print("RELATÓRIO FINAL DE PRODUÇÃO")
        print("="*50)
        print(f"Total Aprovadas: {len(self.pecas_aprovadas)}")
        print(f"Total Reprovadas: {len(self.pecas_reprovadas)}")
        print(f"Caixas Totais: {len(self.caixas)}")
        
        caixas_fechadas = sum(1 for c in self.caixas if len(c) == self.CAPACIDADE_CAIXA)
        print(f"Caixas Fechadas (10/10): {caixas_fechadas}")
        print("="*50)
#Função de limpar tela, para deixar o uso do sistema mais amigável
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
#Função do menu do sistema, essa é chamada assim que o sistema é iniciado. Por ela que as demais funções são chamadas
def main():
    sistema = SistemaAutomacaoIndustrial()
    
    while True:
        print("\n--- SISTEMA DE AUTOMAÇÃO INDUSTRIAL ---")
        print("1. Cadastrar nova peça")
        print("2. Listar peças (Aprovadas/Reprovadas)")
        print("3. Remover peça cadastrada")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final e Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            try:
                id_p = int(input("ID da peça: "))
                peso = float(input("Peso (g): "))
                cor = input("Cor (azul/verde): ").strip().lower()
                comp = float(input("Comprimento (cm): "))
                
                nova_peca = {"id": id_p, "peso": peso, "cor": cor, "comprimento": comp}
                sucesso, msg = sistema.adicionar_peca(nova_peca)
                print(f"\n{msg}")
            except ValueError:
                print("\nErro: Insira valores numéricos válidos para ID, peso e comprimento.")

        elif opcao == "2":
            print("\n--- PEÇAS APROVADAS ---")
            for p in sistema.pecas_aprovadas:
                print(f"ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | Comp: {p['comprimento']}cm")
            
            print("\n--- PEÇAS REPROVADAS ---")
            for p in sistema.pecas_reprovadas:
                print(f"ID: {p['id']} | Motivos: {', '.join(p['motivos'])}")

        elif opcao == "3":
            try:
                id_rem = int(input("Digite o ID da peça para remover: "))
                if sistema.remover_peca(id_rem):
                    print(f"\nPeça {id_rem} removida com sucesso. Caixas atualizadas.")
                else:
                    print("\nErro: ID não encontrado.")
            except ValueError:
                print("\nErro: Digite um ID numérico.")

        elif opcao == "4":
            print("\n--- CAIXAS FECHADAS (Capacidade 10/10) ---")
            encontrou = False
            for i, caixa in enumerate(sistema.caixas, 1):
                if len(caixa) == sistema.CAPACIDADE_CAIXA:
                    print(f"Caixa #{i}: [ID's: {', '.join(str(p['id']) for p in caixa)}]")
                    encontrou = True
            if not encontrou:
                print("Nenhuma caixa foi fechada ainda.")

        elif opcao == "5":
            sistema.gerar_relatorio()
            print("Encerrando sistema...")
            break
        
        else:
            print("\nOpção inválida!")
        
        input("\nPressione Enter para continuar...")
        limpar_tela()
#Validador para chamada da interface do sistema, caso o script seja solicitado diretamente no mesmo diretório
if __name__ == "__main__":
    main()