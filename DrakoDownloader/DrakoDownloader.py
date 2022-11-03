# Se importan librerías tkinter y la necesaria de pytube
import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from pytube import YouTube

#  Ventana de aplicación
ventana = Tk()
ventana.geometry('500x200')
ventana.resizable(0, 0)  # no permite maximizar
ventana.title("Descarga videos de YouTube")
ventana.configure(bg="#424040")
ventana.iconbitmap("Draco.ico")


# función de descarga del video
def downloader():
    try:
        url = YouTube(str(link.get()))
        video = url.streams[1]
        video.download(filedialog.asksaveasfilename(
            title="Directorio para guardar..."))  # sin parámetros --> misma ubicación que el archivo
        Label(ventana, text='Video Descargado', font='arial 15', bg="#424040", fg="red").place(x=185, y=210)
        messagebox.showinfo("Todo correcto...", "Video descargado !!")
    except:
        messagebox.showwarning("Dato introducido erróneo", "Debe introducir una dirección VÁLIDA")


# Etiqueta de título
Label(ventana, text='Descargar videos de YouTube', font='arial 20', bg="#424040", fg="red").pack()

# Entrada de texto para la URL del video
link = StringVar()
Label(ventana, text='Pega aquí el link del video: ', font='arial 15', bg="#424040", fg="red").place(x=90, y=60)
entrada_URL = Entry(ventana, width=50, textvariable=link).place(x=92, y=90)


# botón de descarga
Button(ventana,
       text='Bájalo...!!',
       font='arial 15',
       bg='#706F6F',
       padx=2,
       command=downloader,
       fg="blue").place(x=180, y=150)

# bucle de ejecución
ventana.mainloop()