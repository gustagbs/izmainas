import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pyodbc
import sqlite3
import csv

class izmainas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Stundu izmaiņu informātors")
        self.grid()
        self.pogas()
        self.rows = []

    def pogas(self):







        # ramis pogai 
        self.inputram = tk.Frame(self)
        self.inputram.grid(row=1, column=0, columnspan=12)
        
        self.skollabel = tk.Label(self.inputram, text="Skolotaajs:")
        self.skollabel.grid(row=0, column=0)
        self.skolvar = tk.StringVar()
        
        # labels prieks ui
        self.klasulabels = []
        self.klasuievade = []
        for i in range(1, 11):
            label = tk.Label(self.inputram, text=f"stunda {i}:")
            label.grid(row=0, column=i+1)
            self.klasulabels.append(label)

        # row pievienosanas poga
        self.addrowbutton = tk.Button(self, text="Pievienot līniju", command=self.add_row)
        self.addrowbutton.grid(row=2, column=0, columnspan=12)

        # save poga
        self.savebut = tk.Button(self, text="Saglabāt", command=self.save_inputs)
        self.savebut.grid(row=3, column=0, columnspan=12)
    def add_row(self):
        # row lists
        new_row = []

       
        teacher_var = tk.StringVar(self.inputram)
        teacher_var.set("Izvēlies skolotāju")

        teacher_dropdown = tk.OptionMenu(self.inputram, teacher_var, "Zinta", "Purmnale", "Vevere")#šeit var mierīgi papildināt cik grib, garumzīmes nav jo programma nespēj dekodēt.
        teacher_dropdown.grid(row=len(self.rows)+1, column=0)
        new_row.append(teacher_dropdown)

        class_entries = []
        for i in range(1, 11):
            entry = tk.Entry(self.inputram)
            entry.grid(row=len(self.rows)+1, column=i+1)
            class_entries.append(entry)

        # pievieno rows 
        new_row.extend(class_entries)
        self.rows.append(new_row)

        # pievieno skolotaju
        new_row.append(teacher_var)
        


    def save_inputs(self):
        # save lodzins
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if not filename:
            return
        

        
        with open(filename, "w") as file:
            # header
            header = ["Skolotajs"]
            header.extend([f"Stunda {i}" for i in range(1, 11)])
            file.write(",".join(header) + "\n")
            

            
            for row in self.rows:
            # paņem inpututs
                class_entries = [entry.get() for entry in row[1:]]

                #raksta input info
                
                row_data = [class_entries[10]]
                row_data.extend(class_entries[0:10])
                file.write(",".join(row_data) + "\n")
      

        with open(filename, 'r') as csvfile: #šī visa daļa nav īsti pabeigta, jo nemāku lietot sqlite tabulas veidošanas rīkus pareizi pythona

            csv_file_reader = csv.reader(csvfile,delimiter=',')
            for row in csv_file_reader:
                print(row)  
            savien=sqlite3.connect("izmainas.db")
            cursor = savien.cursor()    
            cursor.execute("create table IF NOT EXISTS izmainas(Skolotaajs text,Stunda_1 text,stunda_2 text,stunda_3 text,stunda_4 text,stunda_5 text,stunda_6 text,stunda_7 text,stunda_8 text,stunda_9 text,stunda_10 text);")
            for row in csv_file_reader:
            
                for i in range(len(row)):
                    
                    sk=row[0]
                    pirma=row[1]
                    otra=row[2]
                    tresa=row[3]
                    ceturt = row[4]
                    piekta= row[5]
                    sesta = row[6]
                    septita = row[7]
                    astota = row[8]
                    devita=row[9]
                    desmit=row[10]
                    ieviet=f"INSERT INTO izmainas VALUES ('{sk}','{pirma}','{otra}','{tresa}','{ceturt}','{piekta}','{sesta}','{septita}','{astota}','{devita}','{desmit}')"
                    cursor.execute(ieviet)
            
            with savien:#man bija vajadzigs lai vins caur sql serveri izveidot tabulu, nevis saglaba datus pavisam sql tapec arī nav commit. Sanāktu ka pēc programmasas darbibas nekas nebūs saglabājies datubāze
                cursor.execute("SELECT * FROM izmainas")
                
                print(cursor.fetchall())#šōbrīd viņš visu saglabā sql servēri tabulās, taču nevaru atrast kā lai printē smukas tabulas, ja tas tiek darīts caur python nevis pašu sqlite3
            


        


            
        
        


 



root = tk.Tk()
app = izmainas(master=root)
app.mainloop()
