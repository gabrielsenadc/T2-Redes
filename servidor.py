import socket
import threading

HOST = '127.0.0.1'
PORTA = 12345

fila_espera = []
lock = threading.Lock()

def criar_tabuleiro():
    return [' ' for _ in range(9)]

def imprimir_tabuleiro(tabuleiro, vez):
    if vez: t = 'T'
    else: t = 't'

    for i in range(9):
        if tabuleiro[i] == 'X': t += '1'
        elif tabuleiro[i] == 'O': t += '2'
        else: t += '0'

    return t

def verificar_vencedor(tabuleiro):
    combinacoes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colunas
        [0, 4, 8], [2, 4, 6]              # diagonais
    ]
    for c in combinacoes:
        if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != ' ':
            return tabuleiro[c[0]]
    if ' ' not in tabuleiro:
        return 'empate'
    return None

def enviar_para_ambos(j1, j2, msg):
    j1.sendall(msg.encode())
    j2.sendall(msg.encode())

def lidar_jogo(jogador1, jogador2):
    tabuleiro = criar_tabuleiro()
    jogadores = [(jogador1, 'X'), (jogador2, 'O')]
    turno = 0
    ativos = [True]  # usada como flag para encerrar as threads de escuta

    enviar_para_ambos(jogador1, jogador2, "\n--- Jogo da Velha Iniciado ---\n")
    enviar_para_ambos(jogador1, jogador2, "Chat ativado. Você pode enviar mensagens a qualquer momento.\n")

    def escutar_chat(remetente, receptor, simbolo):
        # Thread que escuta mensagens do jogador e as redireciona como chat ou jogada
        nonlocal tabuleiro, turno

        while ativos[0]:
            try:
                msg = remetente.recv(1024).decode().strip()
                if not msg:
                    break

                # Se for número de 0 a 8, pode ser jogada
                if msg.isdigit() and int(msg) in range(9):
                    pos = int(msg)

                    # Verifica se é o turno do remetente
                    jogador_atual = jogadores[turno % 2][0]
                    if remetente != jogador_atual:
                        remetente.sendall("⚠️ Não é seu turno.\n".encode())
                        continue

                    if tabuleiro[pos] != ' ':
                        remetente.sendall("⚠️ Posição ocupada. Tente outra.\n".encode())
                        continue

                    tabuleiro[pos] = simbolo
                    resultado = verificar_vencedor(tabuleiro)


                    if resultado == simbolo:
                        enviar_para_ambos(jogador1, jogador2, f"{imprimir_tabuleiro(tabuleiro, False)}")
                        enviar_para_ambos(jogador1, jogador2, f"\n✅ Jogador {simbolo} venceu!\n")
                        break
                    elif resultado == 'empate':
                        enviar_para_ambos(jogador1, jogador2, f"{imprimir_tabuleiro(tabuleiro, False)}")
                        enviar_para_ambos(jogador1, jogador2, "\n⚪ Empate!\n")
                        break
                    else:
                        turno += 1
                        jogador1.sendall(f"{imprimir_tabuleiro(tabuleiro, jogador1 == jogadores[turno % 2][0])}\n".encode())
                        jogador2.sendall(f"{imprimir_tabuleiro(tabuleiro, jogador2 == jogadores[turno % 2][0])}\n".encode())
                else:
                    # É uma mensagem comum (chat)
                    receptor.sendall(f"[Jogador {simbolo}]: {msg}\n".encode())
            except:
                break

        ativos[0] = False
        remetente.close()
        receptor.close()

    # Envia o primeiro tabuleiro e avisa quem começa
    jogador1.sendall(f"{imprimir_tabuleiro(tabuleiro, jogador1 == jogadores[0][0])}\n".encode())
    jogador2.sendall(f"{imprimir_tabuleiro(tabuleiro, jogador2 == jogadores[0][0])}\n".encode())

    # Cria threads para escutar mensagens de cada jogador
    threading.Thread(target=escutar_chat, args=(jogador1, jogador2, 'X'), daemon=True).start()
    threading.Thread(target=escutar_chat, args=(jogador2, jogador1, 'O'), daemon=True).start()

def lidar_com_cliente(cliente):
    cliente.sendall("Aguardando outro jogador...\n".encode())
    with lock:
        fila_espera.append(cliente)
        if len(fila_espera) >= 2:
            j1 = fila_espera.pop(0)
            j2 = fila_espera.pop(0)
            threading.Thread(target=lidar_jogo, args=(j1, j2), daemon=True).start()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"Servidor ouvindo em {HOST}:{PORTA}...")

    while True:
        cliente, _ = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(cliente,), daemon=True).start()

if __name__ == "__main__":
    iniciar_servidor()

