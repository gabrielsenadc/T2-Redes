# Trabalho 2 de Redes de Computadores
# Jogo da Velha
Eduardo Silava Guimarães e Gabriel Sena da Cunha

## Descrição

## Tecnologias Utilizadas
Python, Pygame, Socket, Threading

## Como Executar 
### Requisitos
- Pygame
### Instruções de Execução
1- Clone o repositório:
git clone https://github.com/gabrielsenadc/T2-Redes.git

2- Instale as dependências:
pip install pygame

3- Execute o servidor: python servidor.py ou python3 servidor.py

## Como Testar
Com um terminal já executando servidor.py, abra mais um número par de terminais e execute o código do cliente (python cliente.py ou python3 cliente.py) em cada um deles. 

Cada par será redirecionado para uma sala e um jogo próprio começará. Os seguintes testes podem ser feitos (3, 4, 5 - tratamento de erros):
- Simule um jogo bem sucessido para ver as mensagens de vitória, derrota ou empate
- Mande mensagem no chat (terminal)
- Termine o programa (fechar a aba do pygame) antes da hora com apenas um jogador
- Tente fazer uma jogada fora do seu turno
- Tente fazer uma jogada incorreta (clique em uma posição já ocupada ou inexistente)

## Funcionalidades Implementadas
- Jogo da velha simples
- Múltiplas salas
- Chat entre jogadores
- Interface interativa

## Possíveis Melhorias Futuras
- Login de jogadores
- Convite por token
- Criptografia no chat


