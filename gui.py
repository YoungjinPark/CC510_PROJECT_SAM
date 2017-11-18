# reference: https://www.python-course.eu/tkinter_entry_widgets.php
from tkinter import *
import time
import main

fields = 'Missile Launch Speed (100 - 1000)', 'Aircraft Initial Heading Angle (-90deg - 90deg)'

global values

values = []

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      values.append(float(text))
   root.destroy()

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)

      lab = Label(row, width=40, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Start Animation',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()
   main.runSimulation(values)