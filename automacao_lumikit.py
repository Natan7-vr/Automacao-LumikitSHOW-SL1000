import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
from PIL import Image, ImageTk
import time # Tempo de delay
import subprocess # Abertura de aplicativos
import sys # Encerrar o programa
import pyautogui # Clicar Enter
import pygetwindow as gw
import win32gui # Minimizar janelas
import win32con # Minimizar janelas

def rodar_animacao():
  global frame_atual # Alterar frames
  try:
    label_status.config(text=f"{frames_animacao[frame_atual]}")
    frame_atual = (frame_atual + 1) % len(frames_animacao) # Frame passado
    janela.after(80, rodar_animacao) # Loop .after
  except tk.TclError: # Ignora erro desnecessário
    pass

try:
  janela = tk.Tk() # Cria janela
  janela.overrideredirect(True) # Remoção barra superior
  janela.protocol("WM_DELETE_WINDOW", lambda: None) # Impede de encerrar com Alt + F4

  # Definição tamnanho janela e tela
  largura_janela = 600
  altura_janela = 110
  largura_tela = janela.winfo_screenwidth()
  altura_tela = janela.winfo_screenheight()
  x = (largura_tela // 2) - (largura_janela // 2)
  y = (altura_tela // 2) - (altura_janela // 2)

  # Personalização inicial
  janela.title("Inicializando Lumikit Show...")
  janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}") # Centralização
  janela.configure(bg="#363636")

  # Janela sobre posta
  janela_final = tk.Frame(janela, bg="#BFBFBF")
  janela_final.pack(fill='both', expand=True, padx=4, pady=4)

  # Conteiner (Alinha imagens e texto)
  container_principal = tk.Frame(janela_final, bg="#BFBFBF")
  container_principal.pack(fill="both", expand=True, padx=20, pady=20)

  # Imagem
  try:
    img_original = Image.open(r"C:\Program Files\Lumikit\Automacao\icone_lumikit.jpg")
    img_redimencionada = img_original.resize((64, 64)) # Redimenciona a imagem
    img_final = ImageTk.PhotoImage(img_redimencionada) # Utilia a imagem redimencionada
  except Exception:
    img_final = ImageTk.PhotoImage(Image.new('RGB', (64, 64), color=(255, 191, 0)))

  label_imagem = tk.Label(container_principal, image=img_final, bg="#BFBFBF")
  label_imagem.image = img_final
  label_imagem.pack(side="left", anchor="center", padx=(0, 20))

  # Conteiner Texto
  container_texto = tk.Frame(container_principal, bg="#BFBFBF")
  container_texto.pack(side="left", anchor="center")

  # Titulo
  titulo = tk.Label(container_texto, bg="#BFBFBF", fg="black", text="Abrindo Lumikit Show...", font=Font(size=22, weight="bold", family="Arial")) #Instancia
  titulo.pack(anchor="w") # Posição

  # Observação
  subtitulo = tk.Label(container_texto, bg="#BFBFBF", fg="black", text="Não interaja com o computador durante o processo", font=Font(size=12, family="Arial")) #Instancia
  subtitulo.pack(anchor="w", pady=(5, 0)) # Posição


  # ANIMAÇÂO CARREGAMENTO
  frames_animacao = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
  frame_atual = 0

  label_status = tk.Label(container_principal, text="", font=("Arial", 30, "bold"), bg="#BFBFBF", fg="black")
  label_status.pack(side="right", padx=(0, 20))
  rodar_animacao()


  # TEMPO DE ESPERA INICIAL
  janela.after(120000, janela.destroy) # Finalização janela e tempo de 2min
  janela.mainloop() # Inicia janela


  # ABERTURA ART-NET DE FREESTYLE
  
  subprocess.Popen([r"C:\FreeStyler\Art-Net to DMX.exe"], shell=False)
  time.sleep(3)

  # Selecionar janela popup Art-Net
  hwnd_popup_Art_Net = win32gui.FindWindow(None, "ArtNetToDMX")
  if hwnd_popup_Art_Net:
    win32gui.ShowWindow(hwnd_popup_Art_Net, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd_popup_Art_Net)
    print("Janela Popup Art-Net selecionada com sucesso")
  else:
    print("Janela Popup Art-Net não encontrada")
  
  time.sleep(2)
  pyautogui.press('enter')
  time.sleep(1)
  pyautogui.press('enter')
  time.sleep(2)

  # Fecha a janela Art-Net para ficar em segundo plano
  hwnd_Art_Net = win32gui.FindWindow(None, "to DMX")
  if hwnd_Art_Net:
    WM_CLOSE = 0x0010

    win32gui.PostMessage(hwnd_Art_Net, WM_CLOSE, 0, 0)
    print("Janela Art-Net fechada com sucesso")
  else:
    print("Janela Art-Net não encontrada")


  # ABERTURA ACAP LUMIKIT
  
  time.sleep(2)

  subprocess.Popen([r"C:\Program Files\Lumikit\LumikitACAP.exe"], shell=False)

  time.sleep(2)

  pyautogui.press('down', presses=6, interval=0.2)

  # Minimiza janela ACAP
  hwnd_ACAP = win32gui.FindWindow(None, "Lumikit ACAP")
  if hwnd_ACAP:
    WM_SYSCOMMAND = 0x0112
    SC_MINIMIZE = 0xF020
    win32gui.PostMessage(hwnd_ACAP, WM_SYSCOMMAND, SC_MINIMIZE, 0)
    print("Janela ACAP mininizada com sucesso")
  else:
    print("Janela ACAP não encontrada")


  # ABERTURA LUMIKIT SHOW
  
  subprocess.Popen([r"C:\Program Files\Lumikit\LumikitSHOW.exe"], shell=False)

  sys.exit() # Finalização


except Exception as e:
  print(f"Erro: {e}")
  messagebox.showerror("Erro de Aplicação", f"Ocorreu um erro:\n{str(e)}")
