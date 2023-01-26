from tkinter import *

ventana=Tk()
miFrame=Frame(ventana, width=1200, height=600)
miFrame.pack()
ventana.config(bg="blue")
ventana.title("VALENTIN SEBASTIAN FUENTES GARCES")

textocomentario=Text(miFrame, width=16,height=5)
textocomentario.grid(row=4, column=1, padx=10 , pady=10)

scrollvert=Scrollbar(miFrame, command=textocomentario.yview)
scrollvert.grid(row=4, column=2 , sticky=NSEW)

cuadropass=Entry(miFrame)
cuadropass.grid(row=1,column=1,padx=10, pady=10)
cuadropass.config(show="*")

cuadroNombre=Entry(miFrame)
cuadroNombre.grid(row=0, column=1, padx=10, pady=10)

cuadroApellido=Entry(miFrame)
cuadroApellido.grid(row=2 , column=1, padx=10, pady=10)

cuadriDireccion=Entry(miFrame)
cuadriDireccion.grid(row=3, column=1, padx=10, pady=10)

nombreLabel=Label(miFrame, text="Nombre:")
nombreLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)

cuadroApellido=Label(miFrame, text="Apellido", )
cuadroApellido.grid(row=2, column=0,sticky="e", padx=10, pady=10)

direccionLabel=Label(miFrame , text="Direccion")
direccionLabel.grid(row=3, column=0,sticky="e", padx=10, pady=10)

passlabel=Label(miFrame , text="Password")
passlabel.grid(row=1, column=0,sticky="e", padx=10, pady=10)

comentariosLabel=Label(miFrame, text="Comentarios:")
comentariosLabel.grid(row=4, column=0, padx=10, pady=10)
botonenvio=Button(miFrame, text="enviar")

ventana.mainloop()



    