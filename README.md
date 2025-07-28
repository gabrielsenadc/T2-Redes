# Trabalho 2 de Redes de Computadores
# Jogo da Velha
Eduardo Silva Guimarães e Gabriel Sena da Cunha

## Descrição
O código é uma simples implementação de um jogo da velha com uma interface visual e que é capaz de ser executado entre diferentes dispositivos conectados à mesma rede. O jogo funciona através de um terminal que também possibilita conversas em um chat habilitado no mesmo terminal.

Esse projeto foi desenvolvido como parte da avaliação da disciplina de Redes de Computadores e tem como objetivo a familiarização com o uso de sockets para gerar uma comunicação entre dispositivos através de uma rede.

## Tecnologias Utilizadas
Python, Pygame, Socket, Threading

## Como Executar 
### Requisitos
- Pygame
### Instruções de Execução
1- Clone o repositório:
git clone https://github.com/gabrielsenadc/T2-Redes.git

2- Instale a dependência:
~~~
pip install pygame
~~~

3- Execute o servidor: 
~~~
python3 servidor.py
~~~

4- Cada jogador, em uma mesma rede, executa o cliente:
~~~
python3 cliente.py
~~~

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
- Sessões privadas