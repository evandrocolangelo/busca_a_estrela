# Busca A* (A Estrela) — Explicação Detalhada do Código Python

Este repositório apresenta a implementação detalhada do algoritmo de **Busca A*** baseado no livro *"Inteligência Artificial: Uma Abordagem Moderna"* de **Stuart Russell e Peter Norvig**. 

O código resolve o clássico problema de encontrar a rota de menor custo entre as cidades de **Arad** e **Bucareste** no mapa da Romênia. Diferente da Busca Gulosa, o algoritmo A* garante a solução **ótima** (o caminho mais curto possível) combinando o custo do caminho já percorrido com a estimativa heurística para o destino.

---

## 1. A Equação do A* no Código

A Busca A* seleciona os nós combinando duas funções:
$$f(n) = g(n) + h(n)$$

* **$g(n)$:** O custo real do caminho do estado inicial até o nó atual $n$. No código, ele representa a soma das distâncias em quilômetros das estradas percorridas.
* **$h(n)$:** A estimativa heurística do custo do nó $n$ até o objetivo. Usamos a distância em linha reta até Bucareste.
* **$f(n)$:** O custo total estimado da solução mais barata que passa pelo nó $n$.

---

## 2. Estrutura de Dados e Componentes

### A. O Grafo do Ambiente (`mapa_romenia`)
O mapa é representado usando uma estrutura de **Lista de Adjacência** em um dicionário Python. Cada cidade possui uma lista de tuplas indicando seus vizinhos diretos e a distância real entre eles ($g(n)$).

```python
mapa_romenia = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    # ... conexões reais do livro
}

```

### B. A Função Heurística (`heuristica_bucareste`)

Um dicionário contendo o cálculo pré-computado da distância em linha reta até o destino final (Bucareste). Note que $h(\text{Bucareste}) = 0$.

```python
heuristica_bucareste = {
    'Arad': 366,
    'Bucareste': 0,
    # ... dados informados
}

```

### C. A Fronteira (`fronteira`)

Uma fila de prioridade implementada via biblioteca nativa `heapq` (Min-Heap). Cada elemento inserido é uma tupla estruturada da seguinte forma:


$$\text{(f\_atual, g\_atual, cidade\_atual, caminho\_acumulado)}$$


O Python organiza os elementos automaticamente com base no primeiro valor da tupla (`f_atual`). Logo, o nó com o menor custo estimado total $f(n)$ é sempre extraído primeiro.

### D. Tabela de Controle de Custos (`menores_custos_g`)

Em vez de um conjunto simples de visitados (comum em buscas cegas), o algoritmo A* para Grafos utiliza um dicionário para mapear e registrar o menor custo $g(n)$ real encontrado até o momento para cada cidade visitada.

```python
menores_custos_g = {inicio: 0}

```

---

## 3. Fluxo de Execução Passo a Passo

A função principal `busca_a_estrela` opera seguindo esta lógica:

### Passo 1: Inicialização

O nó inicial (**Arad**) é inserido na fronteira. Como a distância percorrida $g$ inicial é `0`, seu `f_inicial` é puramente sua heurística (`0 + 366`). O dicionário `menores_custos_g` registra que o custo para estar em Arad é `0`.

### Passo 2: O Loop de Seleção Ótima

Enquanto houver elementos na `fronteira`, o algoritmo realiza as seguintes etapas:

1. **Extração:** Remove o nó com o menor valor de $f(n)$ usando `heapq.heappop`.
2. **Teste de Objetivo:** O código faz o teste do objetivo estritamente **no momento em que o nó é retirado da fronteira** (e nunca quando ele é gerado), garantindo a otimalidade do algoritmo. Se a cidade for Bucareste, a busca para e o caminho é retornado.
3. **Validação de Caminho Obsoleto:** O comando `if g_atual > menores_custos_g.get(...)` verifica se o nó que acabou de sair da fila representa um caminho pior/mais caro do que um que já descobrimos e processamos antes. Se for pior, ele é descartado.

### Passo 3: Expansão de Nós Filhos

Para cada vizinho da cidade atual, o algoritmo:

1. Calcula o novo custo acumulado: $\text{novo\_g} = \text{g\_atual} + \text{custo\_da\_estrada}$.
2. Compara esse valor com o que já conhecemos para esse vizinho. Se o `novo_g` for menor (ou se for a primeira vez que vemos a cidade), nós atualizamos a tabela `menores_custos_g`.
3. Calcula o valor total estimado do filho: $\text{novo\_f} = \text{novo\_g} + h(\text{vizinho})$.
4. Cria o histórico da rota atualizada (`novo_caminho`) e insere a tupla resultante de volta na fila de prioridades (`heapq.heappush`).

---

## 4. Por que este código encontra a rota ideal?

Diferente do comportamento míope da busca gulosa — que escolhe a cidade de *Fagaras* em Sibiu apenas porque a linha reta parecia melhor, resultando em uma rota total de **450 km** — a nossa implementação da Busca A* corrige o percurso dinamicamente.

Ao ponderar o custo gasto nas estradas ($g(n)$), o A* percebe a tempo que a descida por *Rimnicu Vilcea* e *Pitesti* compensa mais matematicamente. O programa encerra com sucesso exibindo o trajeto perfeitamente ótimo descrito por Russell & Norvig:

```text
Rota Perfeita Encontrada: Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucareste
Distância Real Percorrida: 418 km

```

---

## 5. Como Executar

O script utiliza estritamente as bibliotecas padrões do Python 3 (sem necessidade de instalar pacotes via `pip`).

```bash
python busca_a_estrela.py

```

```

---

