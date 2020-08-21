import tkinter as tk, sys
from tkinter.simpledialog import askstring
from tkinter import font, END, WORD
from autoscrollbar import autoscrollbar

class gui:
    #   database    -The database object
    def __init__(self, database):
        self.database = database

        self.root = tk.Tk()
        self.root.title('To-Do List')
        self.root.geometry('350x400+1150+25')
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.display()

        self.root.mainloop()

    #   The main display for the program
    def display(self):
        #*  Listbox component to display the list
        self.todo = tk.Listbox(self.root, selectmode='SINGLE', activestyle='none', relief='flat', highlightthickness=1, highlightcolor='#ffffff')
        self.todo.bind('<FocusOut>', lambda e: self.todo.selection_clear(0, END))
        text = font.Font(family='Helvetica', size=12)
        self.todo.config(font=text, background='#e6f0ff')
        self.reset()

        #*  Scrollbars for the Listbox component
        scrollx = autoscrollbar(self.todo, orient='horizontal')
        scrolly = autoscrollbar(self.root, orient='vertical')

        #*  Configure the listbox and scrollbars
        self.todo.configure(yscrollcommand=scrolly.set)
        self.todo.configure(xscrollcommand=scrollx.set)
        scrollx.config(command=self.todo.xview)
        scrolly.config(command=self.todo.yview)

        #*  Button components and the frame to hold them
        buttonFrame = tk.Frame(self.root, background='#cce0ff', border=1)
        add = tk.Button(buttonFrame, text='Add', command=lambda: self.add())
        delete = tk.Button(buttonFrame, text='Delete', command=lambda: self.remove())
        clear = tk.Button(buttonFrame, text='Clear List', command=lambda: self.clear())
        clearSelected = tk.Button(buttonFrame, text='Deselect', command=lambda: self.todo.selection_clear(0, END))

        #*  Pack the GUI components into their parents
        add.pack(fill=tk.X, padx=5, pady=2)
        delete.pack(fill=tk.X, padx=5, pady=8)
        clear.pack(fill=tk.X, padx=5, pady=2)
        clearSelected.pack(fill=tk.X, padx=5, pady=8)
        buttonFrame.pack(fill=tk.Y, side=tk.LEFT)
        self.todo.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    #   Command for the add button
    def add(self):
        item = askstring('Enter Item', 'Item to add:')

        if item:
            self.database.insert(table='list', value=item)
            self.reset()

    #   Command for the remove button
    def remove(self):
        if self.todo.curselection():
            self.database.delete('list', self.todo.get(self.todo.curselection()[0]).replace(' - ', ''))    #!Remove the selected item only
            self.reset()

    #   Command for the clear button
    def clear(self):
        self.database.truncate(table='list') #!Clear the entire list
        self.reset()

    #   Reset the list
    def reset(self):
        self.todo.delete(0, self.todo.size())
        for i in self.database.select(table='list', columns='item'):
            self.todo.insert(self.todo.size(), ' - ' + str(i[0]))

        #!  Create a blank item at the end of the list box and set it as unselectable to make room for the packed horizontal scrollbar
        self.todo.insert(self.todo.size(), '')
        self.todo.itemconfig(self.todo.size() - 1, fg="gray")
        def no_selection(event, index):
            if str(self.todo.curselection()[0]) in str(index):
                self.todo.selection_clear(index)
        self.todo.bind("<<ListboxSelect>>", lambda event, index=self.todo.size() - 1: no_selection(event, self.todo.size() - 1))
