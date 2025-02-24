import streamlit as st

# Título da página
st.title("Calculadora de Frete Avulso: Otimize seus Custos de Transporte")

# Descrição principal
st.write("""
Nossa **Calculadora de Frete Avulso** foi desenvolvida para ajudar empresas e transportadoras a calcular de forma simples e precisa os custos de um frete avulso. 
Ela leva em consideração diversos fatores, como o valor do veículo, custos operacionais, salários de equipe, despesas com combustível e pedágios, além das condições da rota, como distância e tempo de viagem.

Além de calcular os custos totais do frete, a ferramenta gera um relatório completo que inclui:

- **Custo do Veículo**: Depreciação, IPVA, seguro, e manutenção.
- **Equipe**: Salários do motorista e ajudante, além de custos adicionais com alimentação e estada.
- **Rota**: Combustível, pedágios e tempo de viagem.
- **Lucro Estimado**: Cálculo do valor do frete e o lucro obtido com base no percentual de lucro inserido.

Além disso, o relatório também oferece detalhes adicionais para ajudar na tomada de decisão:
""")

# Subtítulo - Como Funciona
st.subheader("Como Funciona?")

# Descrição de como funciona a calculadora
st.write("""
A calculadora utiliza os dados inseridos para calcular os custos totais de um frete, com detalhamento completo das despesas envolvidas, incluindo:

- **Custo do Veículo**: Depreciação, IPVA, seguro, e manutenção.
- **Equipe**: Salários do motorista e ajudante, além de custos adicionais com alimentação e estada.
- **Rota**: Combustível, pedágios e tempo de viagem.

Além disso, você poderá ver o **valor do frete**, o **lucro estimado** e outros custos relacionados, como a **taxa de ocupação do veículo** e o **tempo de descarregamento** no destino.
""")

# Subtítulo - Objetivo da Calculadora
st.subheader("Objetivo da Calculadora")

# Descrição sobre o objetivo da ferramenta
st.write("""
O principal objetivo da nossa ferramenta é permitir que você tenha uma visão clara dos custos envolvidos, 
para tomar decisões mais informadas sobre o valor a ser cobrado pelo frete, garantindo a rentabilidade do seu negócio 
e evitando surpresas no orçamento.
""")

# Chamada para ação
st.write("Experimente agora e faça os cálculos de forma rápida e eficiente!")

# Detalhe do ROI (Retorno sobre o Investimento)
st.subheader("Possibilidades no Relatório Gerado")

# Descrição das possibilidades geradas no relatório
st.write("""
Quando o cálculo do frete é concluído, o relatório gerado incluirá também as seguintes informações:

- **ROI (Retorno sobre o Investimento)**: Em quantas viagens aproximadamente, o retorno do investimento no veículo seria obtido.
  
- **Considerações Finais**: fornecerão insights detalhados sobre a operação do frete, com base nas condições inseridas, incluindo:
        
    1. Gestão do Tempo:
    - Caso o tempo total estimado para o percurso seja superior a 8 horas, será sugerida uma análise detalhada, pois poderá haver custos adicionais com **horas extras** para o motorista e ajudante.

    2. Taxa de Ocupação do Veículo:
    - Se o veículo estiver com baixa taxa de ocupação (25% ou 50%), será recomendada a possibilidade de **agregar outros fretes** ao veículo, visando otimizar os custos e aumentar a eficiência.
    - Para ocupações mais altas (75% ou 100%), o foco será analisar o impacto do **tempo de viagem** e **custos adicionais**, como horas extras e consumo de combustível.

    *3. Ajustes no Custo de Retorno:**
    - Se o valor do **custo de retorno** não for devidamente considerado, ou se o retorno não for otimizado, o relatório sugerirá a necessidade de ajustar esse custo, que impacta diretamente no **lucro final**.

    4. Impacto no Lucro:
        - Ajustes no **custo de retorno** ou **horas extras** podem resultar em **redução do lucro estimado**. O relatório calculará esse impacto e mostrará como ele afeta o valor final do frete.

    5. Viabilidade da Rota:
    - Se todos os parâmetros estiverem dentro dos padrões esperados, a análise indicará que **não há impedimentos ou complicações na rota**, garantindo que a operação seja concluída dentro do tempo e orçamento planejado.
""")





