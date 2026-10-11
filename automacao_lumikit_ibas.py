"""
Automação para abertura do Lumikit Show e Art-Net FreeStyle.

Este programa possui como finalidade abrir de forma correta o Lumikit Show
utilizando a interface SL1000 USB, realizando as aberturas na ordem correta
e automatizada logo após ligar o computador.

Ele foi projetado para rodar em um computador antigo com HDD e Windows 8.1.
Por esse motivo, necessita de um tempo de espera inicial de 2 minutos e
13 segundos. 

Os 13 segundos correspondem à abertura dos executáveis e os 2 minutos ao
tempo de inicialização do Windows. Caso queira alterar este tempo, modifique
o valor de TEMPO_ESPERA_MS.
"""

__author__ = "Natan Vanini da Rosa"
__version__ = "1.0.0"

import sys
from time import sleep
from subprocess import Popen
import tkinter as tk
from tkinter import messagebox

import win32gui
import pyautogui
from PIL import Image, ImageTk

# Diretórios
DIR_FREESTYLE_ARTNET = r"C:\FreeStyler\Art-Net to DMX.exe"
DIR_PAI_LUMIKIT = r"C:\Program Files\Lumikit"
DIR_LUMIKIT_ICONE = f"{DIR_PAI_LUMIKIT}/Automacao/icone_lumikit.jpg"
DIR_LUMIKIT_ACAP = f"{DIR_PAI_LUMIKIT}/LumikitACAP.exe"
DIR_LUMIKIT_SHOW = f"{DIR_PAI_LUMIKIT}/LumikitSHOW.exe"
# Temporização - Predefinição 2 minutos (120000ms)
TEMPO_ESPERA_MS = 120000
# Constantes de Controle do Windows (win32gui)
WM_CLOSE = 0x0010
WM_SYSCOMMAND = 0x0112
SC_MINIMIZE = 0xF020


class Animacao:
    def __init__(self, container_principal, estilo_texto):
        print("Criando animacao")
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.frame_atual = 0
        self.rodando = False

        # Criação do Label
        self.label_status = tk.Label(
            container_principal,
            **estilo_texto,
            text="",
            font=("Arial", 30, "bold")
        )
        self.label_status.pack(side="right", padx=(0, 20))

    # Inicializa a animação
    def start(self):
        if not self.rodando:
            print("Inicializando animacao")
            self.rodando = True
            self.atualiza_frame()

    # Atualiza o frame atual utilizando como base o indice de frame_atual
    def atualiza_frame(self):
        if not self.rodando:
            return
        
        try:
            # Alteração texto selecionando frame via indice
            self.label_status.config(text=f"{self.frames[self.frame_atual]}")
            # Alteração indice frame_atual e verificação de looping
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            # Temporização de 80ms para cada chamada
            self.label_status.after(80, self.atualiza_frame)
        except tk.TclError:
            pass # Ignorando erro

    # Parada da animação e limpeza do texto
    def stop(self):
        if self.rodando:
            print("Encerrando animacao")
            self.rodando = False
        try:
            self.label_status.config(text="")
        except tk.TclError:
            pass # Ignorando erro

class Janela:
        # Corpo Principal
        try:
            print("Criando janela")

            # Criação janela - Título e cor
            janela = tk.Tk()
            janela.title("Inicializando Lumikit Show...")
            janela.configure(bg="#363636")
            # Remoção barra superior
            janela.overrideredirect(True)
            # Impedimento do encerramento com Alt + F4
            janela.protocol("WM_DELETE_WINDOW", lambda: None)

            # DIMENSIONANDO JANELA - Definição tamanho janela e tela
            print("Dimensionando janela")
            largura_janela = 600
            altura_janela = 110
            largura_tela = janela.winfo_screenwidth()
            altura_tela = janela.winfo_screenheight()
            x = (largura_tela // 2) - (largura_janela // 2)
            y = (altura_tela // 2) - (altura_janela // 2)
            # Centralização janela
            janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

            # Janela sobre posta
            janela_final = tk.Frame(janela, bg="#BFBFBF")
            janela_final.pack(fill='both', expand=True, padx=4, pady=4)

            # Conteiner (Alinhamento imagens e texto)
            container_principal = tk.Frame(janela_final, bg="#BFBFBF")
            container_principal.pack(fill="both", expand=True, padx=20, pady=20)

            # Imagem - Icone
            try:
                img_original = Image.open(DIR_LUMIKIT_ICONE)
                print(f"Icone encontrado - {DIR_LUMIKIT_ICONE}")
                # Redimensiona a imagem
                img_redimensionada = img_original.resize((64, 64))
                # Utiliza a imagem redimensionada
                img_final = ImageTk.PhotoImage(img_redimensionada)
            except (FileNotFoundError, OSError):
                print(f"Icone nao encontrado - {DIR_LUMIKIT_ICONE}")
                # Criação de imagem substituta
                img_final = ImageTk.PhotoImage(
                    Image.new(
                        'RGB',
                        (64, 64),
                        color=(255, 191, 0)
                    )
                )
            print("Aplicando icone")
            label_imagem = tk.Label(container_principal, image=img_final, bg="#BFBFBF")
            label_imagem.image = img_final
            label_imagem.pack(side="left", anchor="center", padx=(0, 20))

            # Estilo base textos
            estilo_texto = {
                "bg": "#BFBFBF",
                "fg": "black"
            }
            # Conteiner texto
            container_texto = tk.Frame(container_principal, bg="#BFBFBF")
            container_texto.pack(side="left", anchor="center")

            # Titulo
            titulo = tk.Label(
                container_texto,
                **estilo_texto,
                text="Abrindo Lumikit Show...",
                font=("Arial", 22, "bold")
            )
            titulo.pack(anchor="w") # Posição

            # Observação
            subtitulo = tk.Label(
                container_texto,
                **estilo_texto,
                text="Não interaja com o computador durante o processo",
                font=("Arial", 12)
            )
            subtitulo.pack(anchor="w", pady=(0, 0)) # Posição

            # ANIMAÇÂO CARREGAMENTO - Criação objeto e inicialização do método
            loading = Animacao(container_principal, estilo_texto)
            print("Chamando animacao")
            loading.start()

            # CONTROLE PRINCIPAL - Temporização, finalização e inicio janela
            janela.after(TEMPO_ESPERA_MS, janela.destroy)
            janela.mainloop()
            print("Janela finalizada")
        except Exception as e:
            print(f"Erro: {e}")
            messagebox.showerror("Erro de Aplicacao", f"Ocorreu um erro:\n{str(e)}")

def automacao():
    try:
        # ABERTURA FREESTYLE ART-NET
        print("Executando FreeStyle Art-Net")
        Popen([DIR_FREESTYLE_ARTNET], shell=False)
        print("Art-Net inicializado")
        sleep(3)

        # Selecionar janela popup Art-Net para continuar
        hwnd_popup_artnet = win32gui.FindWindow(None, "ArtNetToDMX")
        if hwnd_popup_artnet:
            try:
                # Parametro 9 utilizado substitui win32con.SW_RESTORE
                win32gui.ShowWindow(hwnd_popup_artnet, 9)
                win32gui.SetForegroundWindow(hwnd_popup_artnet)
                print("Janela Popup Art-Net selecionada com sucesso")
            except Exception as err:
                print(f"Nao foi possivel trazer a janela para frente: {err}") 
        else:
            print("Janela Popup Art-Net nao encontrada")
        sleep(2)
        pyautogui.press('enter')
        sleep(1)
        pyautogui.press('enter')
        sleep(2)

        # Fecha a janela Art-Net para ficar em segundo plano
        hwnd_artnet = win32gui.FindWindow(None, "to DMX")
        if hwnd_artnet:
            win32gui.PostMessage(hwnd_artnet, WM_CLOSE, 0, 0)
            print("Janela Art-Net fechada com sucesso")
        else:
            print("Janela Art-Net nao encontrada")
        sleep(2)

        # ABERTURA ACAP LUMIKIT
        print("Executando Lumikit ACAP")
        Popen([DIR_LUMIKIT_ACAP], shell=False)
        print("Lumikit ACAP inicializado")
        sleep(2)

        # CONFIGURAÇÂO MICROFONE MAIS DE BAIXO
        print("Configurando microfone")
        pyautogui.press('down', presses=6, interval=0.2)

        # Minimização janela Lumikit ACAP
        hwnd_acap = win32gui.FindWindow(None, "Lumikit ACAP")
        if hwnd_acap:
            win32gui.PostMessage(hwnd_acap, WM_SYSCOMMAND, SC_MINIMIZE, 0)
            print("Janela ACAP minimizada com sucesso")
        else:
            print("Janela ACAP nao encontrada para minimizacao")

        # ABERTURA LUMIKIT SHOW
        print("Executando LumikitSHOW")
        Popen([DIR_LUMIKIT_SHOW], shell=False)
        print("LumikitSHOW inicializado")

        print("Automacao concluida")
        sys.exit() # Finalização
    except Exception as e:
        print(f"Erro: {e}")
        messagebox.showerror("Erro de Aplicacao", f"Ocorreu um erro:\n{str(e)}")

# Criação e inicialização objeto Janela
janela = Janela()
# Inicialização automação principal
automacao()