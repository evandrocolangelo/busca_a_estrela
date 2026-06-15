import heapq

# 1. Definição do Grafo (Cidades da Romênia e as distâncias reais das estradas)
# O custo da estrada entre duas cidades representa o g(n) acumulado
mapa_romenia = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 118), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucareste', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucareste', 101)],
    'Bucareste': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucareste', 90)],
    'Urziceni': [('Bucareste', 85), ('Vaslui', 142), ('Hirsova', 98)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# 2. Heurística h(n): Distância em Linha Reta de cada cidade até BUCARESTE
# Valores originais obtidos da tabela oficial do livro de Russell & Norvig
heuristica_bucareste = {
    'Arad': 366, 'Bucareste': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

# 3. Algoritmo de Busca A* (Versão de Busca em Grafo)
def busca_a_estrela(grafo, heuristica, inicio, objetivo):
    """
    Realiza a Busca A* no grafo fornecido.
    A ordenação da fila de prioridade baseia-se em f(n) = g(n) + h(n)
    """
    # A fronteira é uma fila de prioridades (Min-Heap)
    # Estrutura da tupla: (f_n, custo_g, cidade_atual, caminho_acumulado)
    fronteira = []
    
    # No início, o custo real g(inicio) é 0. Logo, f(inicio) = 0 + h(inicio)
    f_inicial = 0 + heuristica[inicio]
    heapq.heappush(fronteira, (f_inicial, 0, inicio, [inicio]))
    
    # Dicionário de controle para registrar o menor custo g(n) conhecido para cada cidade.
    # Isso impede o algoritmo de reprocessar caminhos piores para uma mesma cidade.
    menores_custos_g = {inicio: 0}
    
    print(f"--- Iniciando Busca A* de {inicio} para {objetivo} ---\n")
    
    while fronteira:
        # Extrai o nó que possui o MENOR valor total estimado f(n)
        f_atual, g_atual, cidade_atual, caminho = heapq.heappop(fronteira)
        
        print(f"Expandindo: {cidade_atual:15} | g(n)={g_atual:<3} | h(n)={heuristica[cidade_atual]:<3} | f(n)={f_atual}")
        
        # Teste de Objetivo: O livro salienta que o teste deve ser feito ao REMOVER o nó da fronteira
        if cidade_atual == objetivo:
            print(f"\n[Sucesso] Objetivo atingido de forma ótima!")
            return caminho, g_atual
            
        # Se o custo g atual for maior do que um caminho já descoberto para este mesmo nó, ignore-o
        if g_atual > menores_custos_g.get(cidade_atual, float('inf')):
            continue
            
        # Expandindo as cidades vizinhas
        for vizinho, custo_estrada in grafo.get(cidade_atual, []):
            # O custo g do filho é o custo do pai + a distância real da estrada até o filho
            novo_g = g_atual + custo_estrada
            
            # Se encontramos um caminho inédito ou mais barato para esse vizinho
            if novo_g < menores_custos_g.get(vizinho, float('inf')):
                menores_custos_g[vizinho] = novo_g
                
                # f(n) = g(n) + h(n)
                novo_f = novo_g + heuristica[vizinho]
                novo_caminho = list(caminho) + [vizinho]
                
                # Insere o nó atualizado na fila de prioridades
                heapq.heappush(fronteira, (novo_f, novo_g, vizinho, novo_caminho))
                
    print("\n[Falha] Fronteira esgotada. Nenhum caminho foi encontrado.")
    return None, float('inf')

# 4. Execução do Teste
cidade_origem = 'Arad'
cidade_destino = 'Bucareste'

caminho_otimo, custo_total = busca_a_estrela(mapa_romenia, heuristica_bucareste, cidade_origem, cidade_destino)

print(f"\nRota Perfeita Encontrada: {' -> '.join(caminho_otimo)}")
print(f"Distância Real Percorrida: {custo_total} km")