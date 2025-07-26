import socket
import threading
from time import sleep
import pygame
import queue

HOST = '127.0.0.1'
PORTA = 12345

class Jogo:
    def __init__(self, dados):
        self.tabuleiro = [[dados[1], dados[2], dados[3]],
                          [dados[4], dados[5], dados[6]],
                          [dados[7], dados[8], dados[9]]]
        
        if dados[0] == 'T': self.vez = True
        else: self.vez = False

    def atualiza(self, dados):
        self.tabuleiro = [[dados[1], dados[2], dados[3]],
                          [dados[4], dados[5], dados[6]],
                          [dados[7], dados[8], dados[9]]]
        
        if dados[0] == 'T': self.vez = True
        else: self.vez = False
        


def desenha_linha_vertical(janela, n_linha):
    linha_cor = (255, 128, 0)
    linha_inicio = (n_linha*100, 0)
    linha_fim = (n_linha*100, 300)
    linha_espessura = 8

    pygame.draw.line(janela, linha_cor, linha_inicio, linha_fim, linha_espessura)

def desenha_linha_horizontal(janela, n_linha):
    linha_cor = (255, 128, 0)
    linha_inicio = (0, n_linha*100)
    linha_fim = (janela.get_width(), n_linha*100)
    linha_espessura = 8

    pygame.draw.line(janela, linha_cor, linha_inicio, linha_fim, linha_espessura)

def desenha_tabuleiro(janela, vez):
    fundo_cor = (0, 0, 0)
    janela.fill(fundo_cor)

    for n_linha in range(1, 3):
        desenha_linha_vertical(janela, n_linha)
        desenha_linha_horizontal(janela, n_linha)

    if vez: 
        pygame.font.init() 
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render('Sua vez', False, (255, 255, 255))
        janela.blit(text_surface, ((janela.get_width() - text_surface.get_width())/2, janela.get_height() - 50))

def desenha_x(janela, linha, coluna):
    x_inicio = (coluna * 100) + 10
    x_fim = ((coluna + 1) * 100) - 10

    y_cima = (linha * 100) + 10
    y_baixo = ((linha + 1) * 100) -10

    linha_espessura = 8
    pygame.draw.line(janela, (255, 0, 0), (x_inicio, y_cima), (x_fim, y_baixo), linha_espessura)
    pygame.draw.line(janela, (255, 0, 0), (x_inicio, y_baixo), (x_fim, y_cima), linha_espessura)

def desenha_o(janela, linha, coluna):
    x = (coluna * 100) + 50
    y = (linha * 100) + 50

    centro = (x, y)
    linha_espessura = 8
    pygame.draw.circle(janela, (0, 0, 255), centro, 40, linha_espessura)

def desenha_marcadores(janela, jogo):
    for linha in range(3):
        for coluna in range(3):
            marcador = jogo[linha][coluna]
            if marcador == '1':
                desenha_x(janela, linha, coluna)
            elif marcador == '2':
                desenha_o(janela, linha, coluna)

def desenha_resultado(janela, text):
    if text == 'X':
        pygame.font.init() 
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render('Jogador X venceu!', False, (255, 255, 255))
        janela.blit(text_surface, ((janela.get_width() - text_surface.get_width())/2, janela.get_height() - 50))

    elif text == 'O':
        pygame.font.init() 
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render('Jogador O venceu!', False, (255, 255, 255))
        janela.blit(text_surface, ((janela.get_width() - text_surface.get_width())/2, janela.get_height() - 50))

    else:
        pygame.font.init() 
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render('Empate!', False, (255, 255, 255))
        janela.blit(text_surface, ((janela.get_width() - text_surface.get_width())/2, janela.get_height() - 50))

def receber_mensagens(sock, q):
    while True:
        try:
            dados = sock.recv(1024).decode()
            if not dados:
                print("Servidor encerrou a conexão.")
                break
            msgs = dados.split('\n')
            for msg in msgs:
                if len(msg) > 0:
                    q.put(msg)
        except:
            print("Erro ao receber mensagem.")
            break

def ler_chat(sock):
    while True:
        try:
            entrada = input()
            if entrada.strip() == "":
                continue
            print("\033[A\033[2K", end='')
            sock.sendall(entrada.encode())
        except:
            print("Erro ao enviar. Encerrando.")
            break

def cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORTA))
    except:
        print("Não foi possível conectar ao servidor.")
        return
    
    pygame.init()
    pygame.display.init()

    janela = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("Jogo da velha")

    jogo = Jogo('t000000000')
    
    desenha_tabuleiro(janela, jogo.vez)
    desenha_marcadores(janela, jogo.tabuleiro)
    pygame.display.update()

    executando = True

    q = queue.Queue()

    # Thread para receber mensagens do server
    threading.Thread(target=receber_mensagens, args=(sock, q), daemon=True).start()

    # Thread para ler mensagens do chat
    threading.Thread(target=ler_chat, args=(sock,), daemon=True).start()

    # Envia mensagens (jogadas ou chat)
    while executando:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executando = False
                print("Jogo encerrado. Você saiu.")
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                linha = pos[1] // 100
                coluna = pos[0] // 100

                if linha < 3 and coluna < 3:
                    entrada = linha * 3 + coluna
                    sock.sendall(str(entrada).encode())

        try:
            text = q.get(block=False)
            if text[0] == 'T' or text[0] == 't': # Tabuleiro novo
                jogo.atualiza(text)
            elif text[0] == 'X' or text[0] == 'O' or text[0] == 'E': # Jogo finalizou normalmente
                desenha_tabuleiro(janela, jogo.vez)
                desenha_marcadores(janela, jogo.tabuleiro)
                desenha_resultado(janela, text[0])
                pygame.display.update()
                sleep(3)
                break
            elif text[0] == 'J': # Algum jogador saiu da partida
                print(text)
                break
            else: # Mensagem normal
                print(f"{text}")
                continue
        except queue.Empty:
            continue


        desenha_tabuleiro(janela, jogo.vez)
        desenha_marcadores(janela, jogo.tabuleiro)
        pygame.display.update()
        

    pygame.quit()    
    sock.close()

if __name__ == "__main__":
    cliente()

