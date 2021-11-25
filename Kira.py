import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import sqlite3


class Menu_Inicio:
    db_GlassWork = "GlassWork.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title('Kira')
        window.geometry('800x600')
        window.resizable(False, False)
        self.image = PhotoImage(file='C:/Users/Documentos/Desktop/Aplicacion_Final/Final.png')
        ttk.Label(window, image=self.image).place(x=0, y=0)
        Exit = ttk.Button(window, text='Salir', command=self.ExitAp).place(x= 700, y=560)

        # Creo un frame
        # Creo el espacio para que el usuario ingrese su codigo
        # Creo el boton de Busqueda:

        Frame1 = LabelFrame(self.wind, text='Buscador', font='Harrington')
        Frame1.config(bg='Linen')
        Frame1.config(padx=10, pady=10)
        Frame1.grid(row=1, column=3, columnspan=3, pady=50)
        Frame1.place(x=150, y=10)

        Label(Frame1, text='Ingrese el codigo de perfil: ', bg='Linen', font='Harrington').grid(row=1, column=0)

        #Declaro la variable para almacenar el dato de busqueda:

        self.busqueda_codigo = StringVar()
        self.code = Entry(Frame1, textvariable=self.busqueda_codigo)
        self.code.focus()
        self.code.grid(row=1, column=1)

        Scr = ttk.Button(Frame1, text='Buscar', command=self.Buscar).grid(row=2, columnspan=5, padx=10, pady=10, sticky=W + E)


        self.var = StringVar(window)
        self.var.set('')
        options = ['Linea_Modena', 'Linea_ModenaRPT', 'LineaA30', 'LineaA40RPT', 'Linea_Modena']

        self.options = ttk.OptionMenu(Frame1, self.var, *options, command=self.BuscarPorOption)
        self.options.config(width=20)
        self.options.grid(row=1, column=2, columnspan=3, padx=10, pady=10)

        # Creo la tabla donde se veran las descripciones

        self.tree = ttk.Treeview(self.wind, columns=("#0","#1"))
        self.tree.grid(row=2, column=2, columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.heading('#1', text='Descripcion', anchor=CENTER)
        self.tree.heading('#2', text='Peso', anchor=CENTER)
        self.tree.place(x=108, y=155)
        self.Buscar()

        # Creo el frame de calculadora
        # Vuelvo a crear un espacio para que el usuario pueda ingresar la cantidad que solicita saber
        # Creo el boton de Busqueda:

        Frame2 = LabelFrame(self.wind, text='Calculadora', font='Harrington', bg='Linen')
        Frame2.config(padx=20, pady=20)
        Frame2.grid(row=8, column=3, columnspan=3, pady=50)
        Frame2.place(x=205, y=390)

        Label(Frame2, text='Ingres la operación a realizar: ', font='Harrington', bg='Linen').grid(row=3, column=0)
        self.cant = Entry(Frame2)
        self.cant.grid(row=3, column=1)

        Cal = ttk.Button(Frame2, text='Calcular',  command= lambda :self.Calcular(self.res_titulo)).grid(row=5, columnspan=2, padx=10, pady=10, sticky=W + E)

        #Creo la caja donde se mostrara el resultado de la operacion
        self.res_titulo=StringVar()
        self.res_titulo.set('')
        res=Label(window, text='$', textvariable= self.res_titulo, padx=5, pady=5, width=50)
        res.place(x=218, y = 550)


    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_GlassWork) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()

        return result

    def ExitAp(self):
        aux = messagebox.askokcancel(title='Confirmacion', message='Confirma salir de la aplicacion?')
        if aux == 1:
            window.destroy()

    def Calcular(self, res_titulo):
        ecuacion = self.cant.get()
        result = eval(ecuacion)
        self.res_titulo.set(result)

    def get_tabla(self, tabla):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = 'SELECT * FROM ' + tabla
        if self.busqueda_codigo.get() != '' :
            query = 'SELECT * FROM ' + tabla + ' WHERE codigo LIKE \'%' + self.busqueda_codigo.get() + '%\''

        db_rows = self.run_query(query)

        for row in db_rows:
            self.tree.insert('', END, text=row[0], values=(row[1],row[2]))

    def BuscarPorOption(self, value):
        self.get_tabla(value)

    def Buscar(self):
        self.get_tabla(self.var.get())


if __name__ == '__main__':
    window = Tk()
    app = Menu_Inicio(window)
    window.mainloop()
