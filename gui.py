import subprocess
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from urllib.parse import urlparse

class YouTubeDownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        
        self.base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.yt_dlp = os.path.join(self.base_path, "yt-dlp.exe")
        self.ffmpeg_path = os.path.join(self.base_path, "ffmpeg", "bin")
        self.output_dir = os.path.join(self.base_path, "Music")
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_window(self):
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.root.configure(bg='#2b2b2b')
        
        self.center_window()
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
    
    def setup_variables(self):
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=self.output_dir if hasattr(self, 'output_dir') else "")
        self.format_var = tk.StringVar(value="mp3")
        self.quality_var = tk.StringVar(value="best")
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            main_frame, 
            text="🎵 YouTube MP3 Downloader", 
            font=('Segoe UI', 24, 'bold'),
            bg='#2b2b2b',
            fg='#4CAF50'
        )
        title_label.pack(pady=(0, 30))

        subtitle_label = tk.Label(
            main_frame,
            text="Baixe seus vídeos favoritos em MP3",
            font=('Segoe UI', 12),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 30))
        
        url_frame = tk.Frame(main_frame, bg='#2b2b2b')
        url_frame.pack(fill=tk.X, pady=(0, 20))
        
        url_label = tk.Label(
            url_frame,
            text="🔗 Link do YouTube:",
            font=('Segoe UI', 12, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=('Segoe UI', 11),
            bg='#404040',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            insertbackground='white'
        )
        self.url_entry.pack(fill=tk.X, ipady=8)
        self.url_entry.bind('<Return>', lambda e: self.start_download())
        
        output_frame = tk.Frame(main_frame, bg='#2b2b2b')
        output_frame.pack(fill=tk.X, pady=(0, 20))
        
        output_label = tk.Label(
            output_frame,
            text="📁 Pasta de destino:",
            font=('Segoe UI', 12, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        output_entry_frame = tk.Frame(output_frame, bg='#2b2b2b')
        output_entry_frame.pack(fill=tk.X)
        
        self.output_entry = tk.Entry(
            output_entry_frame,
            textvariable=self.output_path_var,
            font=('Segoe UI', 11),
            bg='#404040',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            insertbackground='white'
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        browse_button = tk.Button(
            output_entry_frame,
            text="📂",
            command=self.browse_folder,
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            font=('Segoe UI', 12),
            cursor='hand2'
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0), ipady=8, ipadx=10)
        
        options_frame = tk.Frame(main_frame, bg='#2b2b2b')
        options_frame.pack(fill=tk.X, pady=(0, 30))

        quality_frame = tk.Frame(options_frame, bg='#2b2b2b')
        quality_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        quality_label = tk.Label(
            quality_frame,
            text="🎧 Qualidade:",
            font=('Segoe UI', 10, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        quality_label.pack(anchor=tk.W)
        
        quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["best", "320k", "256k", "192k", "128k"],
            state="readonly",
            width=10
        )
        quality_combo.pack(anchor=tk.W, pady=(5, 0))
        
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=(20, 0))
        
        self.download_button = tk.Button(
            button_frame,
            text="⬇️ Baixar",
            command=self.start_download,
            bg='#4CAF50',
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            padx=30,
            pady=10
        )
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(
            button_frame,
            text="🗑️ Limpar",
            command=self.clear_fields,
            bg='#f44336',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10
        )
        clear_button.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=540,
            mode='indeterminate'
        )
        self.progress_bar.pack(pady=(20, 0))
        
        self.status_label = tk.Label(
            main_frame,
            text="Pronto para download",
            font=('Segoe UI', 10),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        self.status_label.pack(pady=(10, 0))
        
        self.add_hover_effects()
    
    def add_hover_effects(self):
        def on_enter(e, button, color):
            button.config(bg=color)
        
        def on_leave(e, button, color):
            button.config(bg=color)
        
        self.download_button.bind("<Enter>", lambda e: on_enter(e, self.download_button, "#45a049"))
        self.download_button.bind("<Leave>", lambda e: on_leave(e, self.download_button, "#4CAF50"))
    
    def browse_folder(self):
        folder = filedialog.askdirectory(
            title="Selecione a pasta de destino",
            initialdir=self.output_path_var.get()
        )
        if folder:
            self.output_path_var.set(folder)
    
    def clear_fields(self):
        self.url_var.set("")
        self.url_entry.focus()
    
    def validate_url(self, url):
        if not url:
            return False
        
        parsed = urlparse(url)
        return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_download(self):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira um link do YouTube.")
            self.url_entry.focus()
            return
        
        if not self.validate_url(url):
            messagebox.showwarning("Aviso", "Por favor, insira um link válido do YouTube.")
            self.url_entry.focus()
            return
        
        if not os.path.exists(self.output_path_var.get()):
            messagebox.showerror("Erro", "A pasta de destino não existe.")
            return
        
        self.download_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.update_status("Baixando...")
        
        thread = threading.Thread(target=self.download_audio, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_audio(self, url):
        try:
            output_template = os.path.join(
                self.output_path_var.get(), 
                "%(playlist_title)s", 
                "%(title)s.%(ext)s"
            )
            
            cmd = [
                self.yt_dlp,
                "-x", "--audio-format", self.format_var.get(),
                "--audio-quality", self.quality_var.get(),
                "--ffmpeg-location", self.ffmpeg_path,
                "-o", output_template,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            self.root.after(0, self.download_success)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro no download: {e.stderr if e.stderr else 'Erro desconhecido'}"
            self.root.after(0, lambda: self.download_error(error_msg))
        except Exception as e:
            self.root.after(0, lambda: self.download_error(f"Erro inesperado: {str(e)}"))
    
    def download_success(self):
        self.progress_bar.stop()
        self.download_button.config(state=tk.NORMAL)
        self.update_status("Download concluído com sucesso!")
        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
        
        if messagebox.askyesno("Abrir pasta", "Deseja abrir a pasta de destino?"):
            os.startfile(self.output_path_var.get())
    
    def download_error(self, error_msg):
        self.progress_bar.stop()
        self.download_button.config(state=tk.NORMAL)
        self.update_status("Erro no download")
        messagebox.showerror("Erro", error_msg)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run()