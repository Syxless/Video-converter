import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from moviepy.editor import VideoFileClip
import threading


ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  

def convert_video(input_path, output_filename, bitrate='3000k', fps=30, progress_callback=None):
    try:
        video = VideoFileClip(input_path)
        output_path = os.path.join("output", output_filename)

        if output_filename.endswith('.gif'):
            video.write_gif(output_path, fps=fps)  
        else:
            video.write_videofile(output_path, bitrate=bitrate, fps=fps, codec='libx264', progress_bar=False)

        messagebox.showinfo("Succès", "Conversion terminée avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la conversion : {e}")
    finally:
        if progress_callback:
            progress_callback(100)  


def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Tous les fichiers vidéo", "*.mp4;*.avi;*.mov;*.mkv;*.flv;*.webm")])
    input_entry.delete(0, ctk.END)
    input_entry.insert(0, filename)

def start_conversion():
    input_file = input_entry.get()
    output_filename = output_entry.get()
    bitrate = bitrate_entry.get() or '3000k'
    fps = int(fps_entry.get() or 30)

    if not input_file or not output_filename:
        messagebox.showerror("Erreur", "Veuillez spécifier un fichier d'entrée et un nom de fichier de sortie.")
        return

    
    progress_bar.set(0)
    
    
    threading.Thread(target=convert_video_with_progress, args=(input_file, output_filename, bitrate, fps)).start()

def update_progress(value):
    progress_bar.set(value)
    root.update_idletasks()

def convert_video_with_progress(input_file, output_filename, bitrate, fps):
    for progress in range(0, 101, 10):  
        update_progress(progress)
        convert_video(input_file, output_filename, bitrate, fps, progress_callback=update_progress)

root = ctk.CTk()
root.title("Convertisseur Vidéo")

if not os.path.exists("output"):
    os.makedirs("output")

frame = ctk.CTkFrame(root, width=400, height=400, corner_radius=15)
frame.pack(pady=20, padx=20)

ctk.CTkLabel(frame, text="Fichier vidéo d'entrée:").pack(pady=5)
input_entry = ctk.CTkEntry(frame, width=300)
input_entry.pack(pady=5)
ctk.CTkButton(frame, text="Parcourir", command=browse_file).pack(pady=5)

ctk.CTkLabel(frame, text="Nom du fichier de sortie:").pack(pady=5)
output_entry = ctk.CTkEntry(frame, width=300)
output_entry.pack(pady=5)

ctk.CTkLabel(frame, text="Bitrate:").pack(pady=5)
bitrate_entry = ctk.CTkEntry(frame, width=100)
bitrate_entry.pack(pady=5)

ctk.CTkLabel(frame, text="FPS:").pack(pady=5)
fps_entry = ctk.CTkEntry(frame, width=100)
fps_entry.pack(pady=5)

ctk.CTkButton(frame, text="Convertir", command=start_conversion).pack(pady=10)

progress_bar = ctk.CTkProgressBar(frame, width=300)
progress_bar.pack(pady=10)

root.mainloop()