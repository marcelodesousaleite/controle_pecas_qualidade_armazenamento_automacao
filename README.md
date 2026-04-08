### Protótipo de Automação Industrial - Controle de Qualidade

Este projeto é um sistema lógico desenvolvido em Python para automatizar a inspeção e o empacotamento de peças em uma linha de montagem industrial. O objetivo é substituir processos manuais, reduzindo falhas e aumentando a eficiência operacional.

### Funcionamento

O sistema opera através de uma interface de linha de comando (CLI) que permite gerenciar o fluxo de produção. O raciocínio lógico segue estes passos:

1. **Entrada de Dados:** O operador insere as propriedades da peça (ID, Peso, Cor, Comprimento).
2. **Validação de Qualidade:** O sistema verifica se a peça atende aos requisitos:
    - **Peso:** Entre 95g e 105g.
    - **Cor:** Somente "azul" ou "verde".
    - **Comprimento:** Entre 10cm e 20cm.
3. **Classificação:**
    - **Aprovada:** A peça é enviada para uma caixa de armazenamento.
    - **Reprovada:** A peça é registrada em uma lista separada com o motivo específico da falha.
4. **Gestão de Caixas:** Cada caixa comporta exatamente **10 peças**. Quando uma caixa atinge o limite, o sistema a "fecha" e inicia uma nova automaticamente.
5. **Listagem de caixas** fechadas e **listagem de peças** aprovadas/reprovadas
6. **Remoção e reestruturação** das das peças nas caixas, caso a peça removida seja uma peça aprovada.

### Como Rodar o Programa

### Pré-requisitos

- Ter o **Python 3.x** instalado em seu computador.

### Passo a Passo

1. Copie o código do arquivo `automacao_industrial.py` para uma pasta local.
2. Abra o terminal ou prompt de comando.
3. Navegue até a pasta onde o arquivo foi salvo.
4. Execute o comando:

```
python automacao_industrial.py
```
### Exemplos de Uso

**Entrada de Dados (Opção 1)**

Ao selecionar a opção de cadastro, o sistema solicitará:

- **ID:** `101`
- **Peso:** `100`
- **Cor:** `azul`
- **Comprimento:** `15`

**Saída no Terminal (Aprovação)**

```
Peça APROVADA e enviada para embalagem.
```
**Saída no Terminal (Reprovação)**

Se os dados forem: ID: `102`, Peso: `110`, Cor: `vermelho`, Comprimento: `5`:

```
Peça REPROVADA. Motivos: Peso fora do limite (110.0g), Cor não permitida (vermelho), Comprimento fora do limite (5.0cm)
```
**Relatório Final (Opção 5)**

Ao encerrar o turno, o sistema gera um resumo como este:

```
==================================================
RELATÓRIO FINAL DE PRODUÇÃO
==================================================
Total Aprovadas: 12
Total Reprovadas: 2
Caixas Totais: 2
Caixas Fechadas \(10/10\): 1
==================================================
```
### Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas:** `os` (para limpeza de tela)
