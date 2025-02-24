import streamlit as st  
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import networkx as nx
import itertools



# Função para buscar as coordenadas geográficas usando o Geopy
def get_coordinates(address):
    geolocator = Nominatim(user_agent="distance_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Função para calcular a distância entre dois pontos
def calculate_distance(point1, point2):
    return geodesic(point1, point2).km

# Função para resolver o Problema do Caixeiro Viajante (TSP) e encontrar a melhor rota
def solve_tsp(distances, start_point):
    # Todos os pontos (endereços) para a busca do caminho mínimo
    points = list(distances.keys())
    points.remove(start_point)  # Remove o ponto de origem das permutações
    shortest_path = None
    min_distance = float('inf')

    # Gerando todas as permutações possíveis dos pontos restantes para encontrar a menor rota
    for perm in itertools.permutations(points):
        # Adiciona o ponto de origem no início da permutação
        current_path = [start_point] + list(perm)
        total_distance = 0

        # Calcula a distância total para essa permutação
        for i in range(len(current_path) - 1):
            total_distance += distances[current_path[i]][current_path[i + 1]]
        total_distance += distances[current_path[-1]][current_path[0]]  # Considera o retorno ao ponto inicial

        # Atualizando a melhor rota
        if total_distance < min_distance:
            min_distance = total_distance
            shortest_path = current_path

    return shortest_path, min_distance
####################################################################################################################################

#with st.sidebar:
    

st.title("Calculadora para Fechamento de Frete Avulso")


st.header("Dados Veículo")
valor_veículo = st.number_input("Valor do Veículo/Investimento (R$)")
valor_ipva = st.number_input("Valor do IPVA (R$)")
valor_seguro = st.number_input("Valor do Seguro (R$)")
consumo_medio = st.number_input("Consumo Médio (Km/L)")
if consumo_medio == 0:
    st.warning("O valor do Consumo Médio não pode ser zero! Por favor, insira um valor maior que zero.")
tipo_frete = st.selectbox("Tipo de Frete / Percentual de Lucro",  ["Nacional","Internacional", "Carga Pesada ou Especializada", "Carga Geral", "Definir Percentual %"])
if tipo_frete == "Definir Percentual %":
    valor_percentual_lucro = st.number_input("Valor da Porcentagem Esperada de Lucro")
elif tipo_frete == "Nacional":
    valor_percentual_lucro = 20
    st.write(f"Valor Percentual: {valor_percentual_lucro}%")
elif tipo_frete == "Internacional":
    valor_percentual_lucro = 30
    st.write(f"Valor Percentual: {valor_percentual_lucro}%")
elif tipo_frete == "Carga Pesada ou Especializada":
    valor_percentual_lucro = 40 
    st.write(f"Valor Percentual: {valor_percentual_lucro}%")
elif tipo_frete == "Carga Geral":
    valor_percentual_lucro = 15
    st.write(f"Valor Percentual: {valor_percentual_lucro}%")
    
velocidade_media = st.number_input("Velocidade Média", step=1, format="%d")
if velocidade_media == 0:
    st.warning("O valor da Velocidade Média não pode ser zero! Por favor, insira um valor maior que zero.")


    

st.header("Mão de Obra")
salario_motorista = st.number_input("Salário Motorista (R$)")
salario_ajudante = st.number_input("Salário Ajudante (R$)")
qtd_ajudantes = st.slider('Quantidade de Ajudantes Necessários', 1, 5)
#qtd_ajudantes = st.number_input("Quantidade de Ajudantes Necessários", step=1, format="%d") # não permite valor quebrado
custos_adicionais_equipe = st.number_input("Custos com Almoço, Translado, Estada, Dentre Outros (R$)")


st.header("Dados do Frete")
distancia_cliente = st.number_input("Distância da sua Base/Garagem até o Cliente/Ponto de Coleta")
###qtd_km_rota = st.number_input("Quilômetragem do Percurso (Km)") rtroquei pelo min_distance
qtd_pontos = st.slider('Quantidade de Pontos de Parada, incluindo o ponto inicial ', 1, 8)

# Inicializando variáveis
address1 = address2 = address3 = address4 = address5 = address6 = address7 = address8 = None

# Atribuindo valores aos endereços conforme o número de pontos selecionado
if qtd_pontos == 1:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
elif qtd_pontos == 2:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
elif qtd_pontos == 3:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero, Recife")
elif qtd_pontos == 4:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero, Recife")
    address4 = st.text_input("Endereço 4", "Aeroporto do Recife, Recife")
elif qtd_pontos == 5:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero, Recife")
    address4 = st.text_input("Endereço 4", "Aeroporto do Recife, Recife")
    address5 = st.text_input("Endereço 5", "Boa Viagem, Recife")
elif qtd_pontos == 6:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero, Recife")
    address4 = st.text_input("Endereço 4", "Aeroporto do Recife")
    address5 = st.text_input("Endereço 5", "Boa Viagem, Recife")
    address6 = st.text_input("Endereço 6", "Shopping Recife, Recife")
elif qtd_pontos == 7:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero, Recife")
    address4 = st.text_input("Endereço 4", "Aeroporto do Recife")
    address5 = st.text_input("Endereço 5", "Boa Viagem, Recife")
    address6 = st.text_input("Endereço 6", "Shopping Recife, Recife")
    address7 = st.text_input("Endereço 7", "Praia de Pina, Recife")
elif qtd_pontos == 8:
    address1 = st.text_input("Ponto de Coleta/Armazem/Ponto 0", "UPA Imbiribeira")
    address2 = st.text_input("Endereço 2", "Hospital das Clínicas, Recife")
    address3 = st.text_input("Endereço 3", "Praça do Marco Zero")
    address4 = st.text_input("Endereço 4", "Aeroporto do Recife")
    address5 = st.text_input("Endereço 5", "Boa Viagem, Recife")
    address6 = st.text_input("Endereço 6", "Shopping Recife, Recife")
    address7 = st.text_input("Endereço 7", "Praia de Pina, Recife")
    address8 = st.text_input("Endereço 8", "Parque da Jaqueira, Recife")
# Continuar dessa maneira até o máximo de 20
# Isso pode ser repetido para até 20 pontos, da mesma forma que você já fez para 5 pontos

# ... Repita esse padrão até o ponto 20

# Construindo a lista de endereços com as variáveis existentes
addresses = [address for address in [address1, address2, address3, address4, address5, 
                                     address6, address7, address8] 
             if address and address.strip()]



tempo_médio_descarregamento = st.number_input("Tempo Médio de Descarregamento (Minutos)", step=1, format="%d") # não permite valor quebrado 
retorno = st.selectbox("Viagem com Retorno a Base",  ["Sim", "Não"])

tx_de_ocupacao = st.slider("Taxa de Ocupação do Veículo %", 25, 100, 75, 25)



st.header("Dados de Custo com a Rota")
valor_litro_combustivel = st.number_input("Valor do Litro do Combustível (R$)")
if valor_litro_combustivel == 0:
    st.warning("O valor do litro de combustível não pode ser zero! Por favor, insira um valor maior que zero.")
custo_pedagio = st.number_input("Custo com Pedágio (R$)")

calcular = st.button("Calcular")

#addresses = [address1, address2, address3, address4, address5]
    
#addresses = [address for address in addresses if address.strip()]
#if not addresses:
    #st.warning("Por favor, preencha ao menos um endereço para calcular a rota.")   
       
        




   ##ao clicar no botão 
if calcular:

##### resolvendo rota
    coordinates = []
    for address in addresses:
        coords = get_coordinates(address)
        if coords:
            coordinates.append(coords)
        else:
            st.warning(f"Não foi possível encontrar o endereço: {address}")
        
        # Criando o grafo
    G = nx.Graph()

        # Adicionar nós no grafo (endereço como nó)
    for i, address in enumerate(addresses):
        G.add_node(address, pos=coordinates[i])

        # Calcular as distâncias e adicionar as arestas com os pesos
    distances = {}
    for i in range(len(addresses)):
        for j in range(i + 1, len(addresses)):
            dist = calculate_distance(coordinates[i], coordinates[j])
            G.add_edge(addresses[i], addresses[j], weight=dist)
            if addresses[i] not in distances:
                distances[addresses[i]] = {}
            if addresses[j] not in distances:
                distances[addresses[j]] = {}
            distances[addresses[i]][addresses[j]] = dist
            distances[addresses[j]][addresses[i]] = dist

    # Resolver o Problema do Caixeiro Viajante (TSP) e encontrar a melhor rota
    shortest_path, min_distance = solve_tsp(distances, address1)
     # Calcular a distância do último ponto para o primeiro ponto
    ultimo_ponto = shortest_path[-1]  # Último ponto da rota
    primeiro_ponto = shortest_path[0]  # Primeiro ponto da rota

        # Calcular a distância entre o último ponto e o primeiro ponto
    km_retorno = distances[ultimo_ponto][primeiro_ponto]
    
    #Delcaração de Variavéis

    carga_horaria = 220
    percentual_horextra = 50
    percetual_custo_folha = 43
    dias_uteis_2025 = 253  
    dias_mês = 30
    depreciacao = 8.65
    percentual_manutencao = 30
    
    if retorno == "Sim":
        qtd_km_rota = min_distance +km_retorno
    elif retorno == "Não":
        qtd_km_rota = min_distance


    ###custos individuais
    custo_depreciacao_diario = (((valor_veículo * depreciacao)/100)/dias_uteis_2025)
    custo_ipva_diario = valor_ipva / dias_uteis_2025
    custo_seguro_diario = valor_seguro / dias_uteis_2025
    diaria_manutenção = (((valor_veículo * percentual_manutencao)/100)/dias_uteis_2025)
    diaria_motorista = ((((salario_motorista*percetual_custo_folha)/100)+salario_motorista)/dias_mês)
    diaria_ajudante = ((((salario_ajudante*percetual_custo_folha)/100)+salario_ajudante)/dias_mês)*qtd_ajudantes
    consumo_combustivel = ((qtd_km_rota/consumo_medio)*valor_litro_combustivel)
    tempo_aproximado_total = ((tempo_médio_descarregamento*qtd_pontos)/60)+(qtd_km_rota/velocidade_media)
    valorextra = tempo_aproximado_total - 8
    hora_extra_motorista = ((salario_motorista / carga_horaria)*(percentual_horextra/100))+(salario_motorista / carga_horaria)
    hora_extra_ajudante = ((salario_ajudante / carga_horaria)*(percentual_horextra/100))+(salario_ajudante / carga_horaria)
    

    ###somas dos custos
    total_veiculo = custo_depreciacao_diario + custo_ipva_diario + custo_seguro_diario + diaria_manutenção
    total_equipe = diaria_motorista + diaria_ajudante + custos_adicionais_equipe
    total_rota = consumo_combustivel + custo_pedagio
    total = total_veiculo + total_equipe + total_rota


    ###lucros e retorno 
    valor_a_cobrar = (((valor_percentual_lucro*total)/100)+total)
    lucro = valor_a_cobrar - total

    ####rota
    
    


    #Contas para considerações finais

    custo_extra_motorista = hora_extra_motorista * valorextra
    custo_extra_ajudante = hora_extra_ajudante * valorextra * qtd_ajudantes
    total_extra = custo_extra_ajudante + custo_extra_motorista


    ##### Calculos para o ROI

    roi = (lucro / valor_veículo)*100
    playback_invest = valor_veículo / lucro
    playback_invest = round(playback_invest)
    lucro1 = round(lucro)
    qtd_playback_invest = list(range(1, playback_invest + 1))
    valores_acumulados = [lucro * item for item in qtd_playback_invest]
    roi_data = {
        "Qtd" : qtd_playback_invest,
        "Valor" : valores_acumulados
    }
    df_roi = pd.DataFrame(roi_data)

    graf_roi = px.bar(df_roi, x='Qtd', y='Valor', title='Gráfico de Linhas')
    graf_roi.update_layout(
        title_text='Projeção de Retorno de Investimento',# para deixa o titulo em branco


    )

    
    ###Dados para Gráficos##########################################################################################################################

    custos_veiculo = {
        "Custo": ["Depreciação", "IPVA", "Seguro", "Manutenção"],
        "Valor": [custo_depreciacao_diario, custo_ipva_diario, custo_seguro_diario, diaria_manutenção],

    }

    df_custos_veiculos = pd.DataFrame(custos_veiculo)
    graf_custo_veiculo = px.pie(df_custos_veiculos, 
                   names="Custo", 
                   values="Valor", 
                   title= "",
                   labels={"Custo": "Tipo de Custo", "Valor": "Custo Diário (R$)"})
                   
    graf_custo_veiculo.update_layout(
    #title_font_size=18 , # Ajuste o tamanho do título 
    title_text='Dristibuição do Custo do Veículo',# para deixa o titulo em branco
    font_size=16,
    
    
    )
    ###Grafico de Bolhas - Custo Totais
    custo_total = {

        "Custo": ["Depreciação", "IPVA", "Seguro", "Manutenção", "Motorista", "Ajudante", "Despesas",  "Pedágio", "Combustível"],
        "Valor": [custo_depreciacao_diario, custo_ipva_diario, custo_seguro_diario, diaria_manutenção, diaria_motorista, diaria_ajudante, custos_adicionais_equipe, custo_pedagio, consumo_combustivel ],
        "Tamanho da Bolha": [custo_depreciacao_diario, custo_ipva_diario, custo_seguro_diario, diaria_manutenção, diaria_motorista, diaria_ajudante, custos_adicionais_equipe, custo_pedagio, consumo_combustivel ],

    }

    df_custo_total = pd.DataFrame(custo_total)

    graf_custo_total = px.scatter(df_custo_total, 
                                    x="Custo", 
                                    y="Valor", 
                                    size="Tamanho da Bolha", 
                                    text="Custo",  # Exibe o nome de cada custo na bolha
                                    title="Impacto de Cada Categoria no Custo Total da Viagem",
                                    labels={"Custo": "Tipo de Custo", "Valor": "Custo Diário (R$)"})


    graf_custo_total.update_layout(
        title_font_size=18,  # Tamanho da fonte do título
        showlegend=False,  # Não exibe a legenda (opcional)
        xaxis_title="Tipo de Custo",  # Título do eixo X
        yaxis_title="Custo Diário (R$)",  # Título do eixo Y
    )


    ##### Grafico de Rosca - Custos Totais
   ##########################################################################################################################
 
    custos_totais = {

         "Custo" :["Veículo", "Equipe", "Rota"],
         "Valores" : [total_veiculo,total_equipe, total_rota],
         
    }

    df_custos_totais = pd.DataFrame(custos_totais)

    graf_custos_totais = go.Figure(data=[go.Pie(labels=df_custos_totais['Custo'], values=df_custos_totais['Valores'], pull=[0, 0.2, 0, 0])])
    graf_custos_totais.update_layout(title_text="Dristibuição dos Custos Totais")
# Exibindo o gráfico no Streamlit
    
            
##########################################################################################################################

# Pagina Principal Começa Aqui

    with st.expander("Clique para ver os parâmetros utilizados"):
            st.write("Aqui estão as informações adicionais que você pode visualizar.")
   
    st.markdown("<br><br>", unsafe_allow_html=True)
        
        

    col7, col8 , col9 = st.columns(3)

    with col7:
           
        st.markdown(f"""
        <div style="background-color: #4CAF50; padding: 10px; border-radius: 10px; color: white; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center;">
            <h3>Custo Total</h3>
            <p style="font-size: 22px">R${total:,.2f}</p>
                
        </div>
        """, unsafe_allow_html=True)

    with col8:

        st.markdown(f"""
        <div style="background-color: #4CAF50; padding: 10px; border-radius: 10px; color: white; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center;">
            <h3>Valor Frete</h3>
            <p style="font-size: 22px">R${valor_a_cobrar:,.2f}</p>
                
        </div>
        """, unsafe_allow_html=True)

    with col9:

        st.markdown(f"""
        <div style="background-color: #4CAF50; padding: 10px; border-radius: 10px; color: white; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h3>Lucro</h3>
            <p style="font-size: 22px">R${lucro:,.2f}</p>
                
        </div>
        """, unsafe_allow_html=True)

        
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader(f"Custos Totais")   
    with st.expander("Clique para ver a Descrição dos Custos Totais"):
         st.plotly_chart(graf_custo_total)
         st.plotly_chart(graf_custos_totais)
         col3, col4, col5 = st.columns(3)

         col3.write(f"Veículo: R${total_veiculo:,.2f} ")
         col4.write(f"Equipe: R${total_equipe:,.2f} ")  
         col5.write(f"Rota: R${total_rota:,.2f} ")
         st.subheader(f"Total: R${total:,.2f} ")
         
    
    #st.markdown("<br><br><br><br>", unsafe_allow_html=True)### pula linha
     #########################################################################################################################
          
    st.subheader("Custo do Veículo")
    with st.expander("Clique para ver a Distribuição de Custo do Veículo"):
        
        st.plotly_chart(graf_custo_veiculo)
        col1, col2= st.columns(2)

        
        col1.write(f"Custo Diário Aproximado de Depreciação: R${custo_depreciacao_diario:,.2f}")
        col1.write(f"Custo Diário Aproximado de IPVA: R${custo_ipva_diario:,.2f}")
        col2.write(f"Custo Diário Aproximado de Seguro: R${custo_seguro_diario:,.2f} ")
        col2.write(f"Custo Diário Aproximado de Manutenção: R${diaria_manutenção:,.2f} ")
        st.subheader(f"Total: R${total_veiculo:,.2f} ")

        
    ##########################################################################################################################


    col3, col4 = st.columns(2)
    col3.subheader(f"Custo da Equipe")
    with col3.expander("Clique para ver a Distribuição de Custo da Equipe"):
            st.write(f"Custo Diário Aproximado com Motorista: R${diaria_motorista:,.2f}")
            st.write(f"Custo Diário Aproximado com ajudante: R${diaria_ajudante:,.2f}")
            st.write(f"Custo Diário Aproximado com a Equipe: R${custos_adicionais_equipe:,.2f}")
            st.write(f"Total: R${total_equipe:,.2f} ")
  

    col4.subheader(f"Custo da Rota")
    with col4.expander("Clique para ver a Distribuição de Custo da Rota"):
            st.write(f"Custo Aproximado com Combustível: R${consumo_combustivel:,.2f}")
            st.write(f"Custo Aproximado com Pedágio: R${custo_pedagio:,.2f}")
            st.write(f"Total: R${total_rota:,.2f} ")
           
    st.subheader("Detalhe da Rota")
    with st.expander("Clique para ver a Rota Sugerida"):
        st.write(f"A melhor rota começando em '{address1}' é:")
        st.write(" -> ".join(shortest_path))
        st.write(f"Distância total da melhor rota: {min_distance:.2f} km")
        st.write(f"O tempo aproximado total contabilizando o descarragemanto é de: {tempo_aproximado_total:,.2f} horas.")
            

    st.subheader("Detalhe do ROI")
    with st.expander("Clique para ver a Rota Sugerida"):
    #st.write(f"{qtd_playback_invest}")
        st.plotly_chart(graf_roi)
        st.write(f"Em aproxidamente {playback_invest:,.0f} viagens como essa, o retorno do investimento no veículo seria obtido")
        #st.dataframe(df_roi)
    ################################################################################################
    st.subheader("Considerações")
    #####if das considerações
    ###
    with st.expander("Clique para ver as Considerações Finais"):
        if  tx_de_ocupacao in [25,50]:
            if retorno == "Sim":
                if tempo_aproximado_total > 8:####Ocupação/Tempo
                    st.write(f"Recomenda-se uma análise detalhada da Gestão do Tempo, visto que poderá haver custos adicionais com horas extras. O tempo total estimado para o percurso, incluindo os pontos de descarregamento, é de {tempo_aproximado_total:,.2f} horas.")
                    st.write(f"O valor aproximado das horas extras do motorista é de R$ {custo_extra_motorista:,.2f}")
                    st.write(f"e do ajudante de R$ {custo_extra_ajudante:,.2f}.")
                    st.write(f"O custo total estimado com horas extras é de R$ {total_extra:,.2f}.")
                    st.write(f"Explorar a possibilidade de agregar outros fretes ao veículo, caso haja um acordo com o cliente, oferecendo até mesmo um desconto, já que o veículo está ocupando apenas {tx_de_ocupacao}% de sua capacidade.")
                elif  7 <= tempo_aproximado_total < 8:###ocupação/possivel hora extra
                    st.write(f"Explorar a possibilidade de agregar outros fretes ao veículo, caso haja um acordo com o cliente, oferecendo até mesmo um desconto, já que o veículo está ocupando apenas {tx_de_ocupacao}% de sua capacidade.")
                    st.write(f"Observe que ainda poderá haver acréscimo de horas extras, pois o retorno ainda não foi contabilizado na estimativa.")
                elif tempo_aproximado_total <7 :####Ocupação/
                    st.write(f"Explorar a possibilidade de agregar outros fretes ao veículo, caso haja um acordo com o cliente, oferecendo até mesmo um desconto, já que o veículo está ocupando apenas {tx_de_ocupacao}% de sua capacidade.")
            
            elif retorno == "Não":
                if tempo_aproximado_total > 8:####Ocupação/Tempo/Custo
                    st.write(f"Recomenda-se uma análise detalhada da Gestão do Tempo, visto que poderá haver custos adicionais com horas extras. O tempo total estimado para o percurso, incluindo os pontos de descarregamento, é de {tempo_aproximado_total:,.2f} horas.")
                    st.write(f"O valor aproximado das horas extras do motorista é de R$ {custo_extra_motorista:,.2f}")
                    st.write(f"e do ajudante de R$ {custo_extra_ajudante:,.2f}.")
                    st.write(f"O custo total estimado com horas extras é de R$ {total_extra:,.2f}.")
                    st.write(f"Explorar a possibilidade de agregar outros fretes ao veículo, caso haja um acordo com o cliente, oferecendo até mesmo um desconto, já que o veículo está ocupando apenas {tx_de_ocupacao}% de sua capacidade.")
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")
                elif 7 <= tempo_aproximado_total < 8: ###Custo/possivel hora extra  
                    st.write(f"Observe que ainda poderá haver acréscimo de horas extras, pois o retorno ainda não foi contabilizado na estimativa.")
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")
                elif tempo_aproximado_total <7:##Custo
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")
               
        
        elif retorno == "Não":
            if tx_de_ocupacao in [75,100]:
                if 7 <= tempo_aproximado_total < 8: ###Custo/possivel hora extra  
                    st.write(f"Observe que ainda poderá haver acréscimo de horas extras, pois o retorno ainda não foi contabilizado na estimativa.")
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")
                elif tempo_aproximado_total <7:##Custo
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")
                elif tempo_aproximado_total > 8:###Custo/Tempo
                    st.write(f"Recomenda-se uma análise detalhada da Gestão do Tempo, visto que poderá haver custos adicionais com horas extras. O tempo total estimado para o percurso, incluindo os pontos de descarregamento, é de {tempo_aproximado_total:,.2f} horas.")
                    st.write(f"O valor aproximado das horas extras do motorista é de R$ {custo_extra_motorista:,.2f}")
                    st.write(f"e do ajudante de R$ {custo_extra_ajudante:,.2f}.")
                    st.write(f"O custo total estimado com horas extras é de R$ {total_extra:,.2f}.")
                    st.write(f"Verifique com o contratante a possibilidade de ajustar o valor do custo de retorno, pois este é impactado pelo consumo de combustível, estimado em torno de R$ {((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel :,.2f}.")
                    st.write(f"Esse ajuste pode afetar diretamente o lucro, reduzindo-o de R$ {lucro:,.2f}") 
                    st.write(f" Para R$ {lucro - (((distancia_cliente + qtd_km_rota)/consumo_medio) * valor_litro_combustivel):,.2f}.")


        elif retorno == "Sim":
            if tx_de_ocupacao in [75,100]:
                if tempo_aproximado_total > 8:####Tempo
                    st.write(f"Recomenda-se uma análise detalhada da Gestão do Tempo, visto que poderá haver custos adicionais com horas extras. O tempo total estimado para o percurso, incluindo os pontos de descarregamento, é de {tempo_aproximado_total:,.2f} horas.")
                    st.write(f"O valor aproximado das horas extras do motorista é de R$ {custo_extra_motorista:,.2f}")
                    st.write(f"e do ajudante de R$ {custo_extra_ajudante:,.2f}.")
                    st.write(f"O custo total estimado com horas extras é de R$ {total_extra:,.2f}.")                    
                elif  tempo_aproximado_total < 8:####sem problemas/
                    st.write(f"Após análise, constatamos que não há impedimentos ou complicações na rota, garantindo que o percurso seja realizado conforme o planejado, sem impactos no tempo estimado ou custos adicionais. A operação está fluindo dentro das expectativas.")


     
        
            
else:          
 st.warning("Por favor, insira os parâmetros para obter o resutado.")  # Mensagem atualizada





  
st.markdown(f"""






""", unsafe_allow_html=True)
