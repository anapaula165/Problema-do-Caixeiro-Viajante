# Problema do Caixeiro Viajante
![image](https://github.com/user-attachments/assets/169fa029-69e8-4eb9-b2b1-9eb51cead1f9)

Conhecido como TSP, do inglês Travelling Salesman Problem.

"O problema do caixeiro viajante (conhecido como TSP, do inglês Travelling Salesman Problem) é um clássico da teoria dos grafos e da otimização combinatória. Ele descreve o desafio de encontrar a rota mais curta para um vendedor (ou "caixeiro viajante") que precisa visitar um conjunto de cidades uma única vez e retornar ao ponto de partida. A questão central é: qual é a rota mais curta que permite ao vendedor visitar todas as cidades e retornar ao ponto inicial?

### Características principais do problema:
Entrada: Uma lista de cidades e as distâncias entre cada par delas.
Objetivo: Determinar a rota mínima que passe por todas as cidades exatamente uma vez, voltando ao ponto de origem.
Desafios: O número de possíveis rotas cresce exponencialmente com o número de cidades, tornando o problema muito difícil de resolver para grandes conjuntos (é um problema NP-difícil)."

### Em aula
Nos foi pedido para achar a menor rota, saindo da cidade de São Paulo e passando por todos as cidades/municípios do estado de São Paulo, retornando para onde saiu. O desafio era fazer isso no menor tempo possível e sem que as linhas da rota se cruzassem.

### Solução
Optei por fazer o caminho em linha reta, ignorando as rodovias, mas usando Haversine, pois ela traça o caminho considerando a curvatura da terra.
