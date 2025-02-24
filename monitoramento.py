import os
import time
import hashlib
import logging
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuração do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Variáveis globais
DIRECTORY_TO_WATCH = ""
observer = None

# Função para calcular o hash de um arquivo
def calculate_file_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Erro ao calcular hash do arquivo {filepath}: {e}")
        return None

# Classe para lidar com eventos do sistema de arquivos
class MyHandler(FileSystemEventHandler):
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def on_modified(self, event):
        if not event.is_directory:
            filepath = event.src_path
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                log_message = f"Arquivo modificado: {filepath} - Hash: {file_hash}"
                logging.info(log_message)
                self.log_callback(log_message)

    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                log_message = f"Arquivo criado: {filepath} - Hash: {file_hash}"
                logging.info(log_message)
                self.log_callback(log_message)

    def on_deleted(self, event):
        if not event.is_directory:
            filepath = event.src_path
            log_message = f"Arquivo deletado: {filepath}"
            logging.info(log_message)
            self.log_callback(log_message)

# Função para iniciar o monitoramento
def start_monitoring():
    global DIRECTORY_TO_WATCH, observer
    DIRECTORY_TO_WATCH = filedialog.askdirectory()
    if not DIRECTORY_TO_WATCH:
        log_message = "Nenhum diretório selecionado. Monitoramento cancelado."
        logging.error(log_message)
        log_callback(log_message)
        return

    log_message = f"Monitorando diretório: {DIRECTORY_TO_WATCH}"
    logging.info(log_message)
    log_callback(log_message)

    event_handler = MyHandler(log_callback)
    observer = Observer()
    observer.schedule(event_handler, path=DIRECTORY_TO_WATCH, recursive=True)
    observer.start()

# Função para parar o monitoramento
def stop_monitoring():
    global observer
    if observer:
        observer.stop()
        observer.join()
        log_message = "Monitoramento parado."
        logging.info(log_message)
        log_callback(log_message)

# Função para salvar logs em um arquivo
def save_logs():
    logs = log_area.get("1.0", tk.END)
    if not logs.strip():
        messagebox.showwarning("Aviso", "Nenhum log para salvar.")
        return

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open("logs/monitoramento_logs.txt", "w") as f:
        f.write(logs)
    log_message = "Logs salvos em 'logs/monitoramento_logs.txt'."
    logging.info(log_message)
    log_callback(log_message)

# Função para limpar a área de log
def clear_logs():
    log_area.delete("1.0", tk.END)
    log_callback("Área de logs limpa.")

# Função para exibir logs na interface
def log_callback(message):
    log_area.insert(tk.END, message + "\n")
    log_area.see(tk.END)  # Rola para o final do texto

# Interface gráfica
window = tk.Tk()
window.title("Monitoramento de Ameaças - Blue Team")
window.geometry("800x600")

# Botões
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Iniciar Monitoramento", command=start_monitoring)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Parar Monitoramento", command=stop_monitoring)
stop_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Salvar Logs", command=save_logs)
save_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Limpar Logs", command=clear_logs)
clear_button.pack(side=tk.LEFT, padx=5)

# Área de log
log_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=30)
log_area.pack(padx=10, pady=10)

# Iniciar a interface
window.mainloop()