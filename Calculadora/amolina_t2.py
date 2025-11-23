#Bibliotecas
import tkinter as tk
import os as os
from tkinter import Toplevel, Label, PhotoImage
from tkinter import messagebox
import subprocess

#ventana
ventana = tk.Tk()
ventana.title("Calculadora funcional (creo)")
ventana.configure(bg="#1a1b28")
ventana.geometry("300x400")
ventana.resizable(False, False)
pantalla = tk.Entry(ventana, fg="white", font=("arial", 25), bg="#1e2435", justify="right", width=15, borderwidth=3)
pantalla.grid(row=0, column=0, columnspan=5, padx=10, pady=20)

primer_numero = None
operacion = None

#funciones
def coming_soon():
    messagebox.showinfo("Información", "Coming Soon")

def season_pass():
    ruta = os.path.join(os.path.dirname(__file__), "image4.png")
    ventana_img = tk.Toplevel(ventana)
    ventana_img.title("Imagen abierta")
    ventana_img.configure(bg="#1e2435")
    img_tk = tk.PhotoImage(file=ruta)

    lbl = tk.Label(ventana_img, image=img_tk)
    lbl.image = img_tk 
    lbl.pack(padx=10, pady=10)


def archivo_exe():
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_exe = os.path.join(carpeta_actual, "archivo.exe")
    try:
        subprocess.Popen([ruta_exe])
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_exe}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el archivo:\n{e}")

def mostrar_ventana(valor):
    """Agrega texto o números a la pantalla."""
    pantalla.insert(tk.END, str(valor))

def borrar():
    """Borra el contenido de la pantalla."""
    pantalla.delete(0, tk.END)

def elegir_operacion(simbolo):
    """Guarda el primer número y la funcion."""
    global primer_numero, operacion
    try:
        primer_numero = float(pantalla.get())
    except ValueError:
        primer_numero = 0
    operacion = simbolo
    pantalla.delete(0, tk.END)

def resultados():
    """Ejecuta la funcion y muestra el resultado."""
    global primer_numero, operacion
    try:
        segundo_numero = float(pantalla.get())
    except ValueError:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")
    if primer_numero + segundo_numero == 2.0:
        img_win = Toplevel(ventana)
        img_win.title("Resultado 2")
        img_win.geometry("400x400")
        img_win.configure(bg="black")

        try:
            imagen = PhotoImage(file="image3.png")
            lbl = Label(img_win, image=imagen, bg="black")
            lbl.image = imagen
            lbl.pack(expand=True)
        except Exception:
            Label(img_win, text="Resultados = 2", fg="red", bg="black", font=("Arial", 20, "bold")).pack(expand=True)
  

#funcionamiento
    pantalla.delete(0, tk.END)
    try:
        if operacion == "+":
            pantalla.insert(0, primer_numero + segundo_numero)
        elif operacion == "-":
            pantalla.insert(0, primer_numero - segundo_numero)
        elif operacion == "*":
            pantalla.insert(0, primer_numero * segundo_numero)
        if operacion == "/":
            if segundo_numero == 0:
                fullscreen = Toplevel(ventana)
                fullscreen.title("Math ERROR")
                fullscreen.attributes("-fullscreen", True)
                fullscreen.configure(bg="black")
                
                try:
                    imagen_error = PhotoImage(file="image1.png")
                    lbl = Label(fullscreen, image=imagen_error, bg="black")
                    lbl.image = imagen_error
                    lbl.pack(expand=True, fill="both")
                except Exception:
                    lbl = Label(fullscreen, text="MATH ERROR", fg="red", bg="black",font=("Arial", 60, "bold"))
                    lbl.pack(expand=True, fill="both")
                    fullscreen.bind("<Escape>", lambda e: fullscreen.destroy())
                    pantalla.delete(0, tk.END)
                    pantalla.insert(0, "Math ERROR")
        
    except Exception:
        pantalla.insert(0, "Error")
    return

#configuracion botones
b1 = tk.Button(ventana, text="Ø", height=3, width=5, relief="raised", borderwidth=1, bg="#52c9dc",
               command=archivo_exe)
b1.grid(row=2, column=0, padx=3, pady=3)
b2 = tk.Button(ventana, text="%", height=3, width=5, relief="raised", borderwidth=1, bg="#52c9dc",
               command=coming_soon)
b2.grid(row=2, column=1, padx=3, pady=3)
b3 = tk.Button(ventana, text="π", height=3, width=5, relief="raised", borderwidth=1, bg="#52c9dc",
               command=coming_soon)
b3.grid(row=2, column=2, padx=3, pady=3)
b4 = tk.Button(ventana, text="C", height=3, width=5, relief="raised", borderwidth=1, bg="#52c9dc", 
               command=borrar)
b4.grid(row=2, column=3, padx=3, pady=3)
b5 = tk.Button(ventana, text="AC", height=3, width=5, relief="raised", borderwidth=1, bg="#52c9dc", 
               command=borrar)
b5.grid(row=2, column=4, padx=3, pady=3)

b6 = tk.Button(ventana, text="7", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white", 
               command=lambda: mostrar_ventana(7))
b6.grid(row=3, column=0, padx=3, pady=3)
b7 = tk.Button(ventana, text="8", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white", 
               command=lambda: mostrar_ventana(8))
b7.grid(row=3, column=1, padx=3, pady=3)
b8 = tk.Button(ventana, text="9", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white", 
               command=lambda: mostrar_ventana(9))
b8.grid(row=3, column=2, padx=3, pady=3)
b9 = tk.Button(ventana, text="^2", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",
               command=season_pass)
b9.grid(row=3, column=3, padx=3, pady=3)
b10 = tk.Button(ventana, text="√x", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",
                command=season_pass)
b10.grid(row=3, column=4, padx=3, pady=3)

b11 = tk.Button(ventana, text="4", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
               command=lambda: mostrar_ventana(4))
b11.grid(row=4, column=0, padx=3, pady=3)
b12 = tk.Button(ventana, text="5", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
                command=lambda: mostrar_ventana(5))
b12.grid(row=4, column=1, padx=3, pady=3)
b13 = tk.Button(ventana, text="6", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
                command=lambda: mostrar_ventana(6))
b13.grid(row=4, column=2, padx=3, pady=3)
b14 = tk.Button(ventana, text="*", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc", 
                command=lambda: elegir_operacion("*"))
b14.grid(row=4, column=3, padx=3, pady=3)
b15 = tk.Button(ventana, text="/", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",  
                command=lambda: elegir_operacion("/"))
b15.grid(row=4, column=4, padx=3, pady=3)

b16 = tk.Button(ventana, text="1", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
                command=lambda: mostrar_ventana(1))
b16.grid(row=5, column=0, padx=3, pady=3)
b17 = tk.Button(ventana, text="2", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
                command=lambda: mostrar_ventana(2))
b17.grid(row=5, column=1, padx=3, pady=3)
b18 = tk.Button(ventana, text="3", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white",
                command=lambda: mostrar_ventana(3))
b18.grid(row=5, column=2, padx=3, pady=3)
b19 = tk.Button(ventana, text="+", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",  
                command=lambda: elegir_operacion("+"))
b19.grid(row=5, column=3, padx=3, pady=3)
b20 = tk.Button(ventana, text="-", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",  
                command=lambda: elegir_operacion("-"))
b20.grid(row=5, column=4, padx=3, pady=3)

b21 = tk.Button(ventana, text="0", height=3, width=5, relief="raised", borderwidth=1,bg="#1e2435", fg="white", 
                command=lambda: mostrar_ventana(0))
b21.grid(row=6, column=0, padx=3, pady=3)
b22 = tk.Button(ventana, text=".", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",
                command=lambda: mostrar_ventana("."))
b22.grid(row=6, column=1, padx=3, pady=3)
b23 = tk.Button(ventana, text="EXP", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",
                command=coming_soon)
b23.grid(row=6, column=2, padx=3, pady=3)
b24 = tk.Button(ventana, text="ANS", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc",
                command=season_pass)
b24.grid(row=6, column=3, padx=3, pady=3)
b25 = tk.Button(ventana, text="=", height=3, width=5, relief="raised", borderwidth=1,bg="#52c9dc", 
                command=resultados)
b25.grid(row=6, column=4, padx=3, pady=3)

ventana.mainloop()