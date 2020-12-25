import sys
import tkinter as tk
from tkinter import END, WORD, font, messagebox
from tkinter.simpledialog import askstring

from autoscrollbar import autoscrollbar


class gui:
    def __init__(self, database):
        """

        Args:
            database (str): The database object
        """
        self.database = database

        self.root = tk.Tk()
        self.root.title('To-Do List')
        self.root.geometry('250x100+975+25')
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.display()

        self.root.mainloop()

    def display(self):
        """The main display for the program
        """
        #*  Listbox component to display the list
        self.todo = tk.Listbox(self.root, width=30, selectmode='SINGLE', activestyle='none', relief='flat', highlightthickness=1, highlightcolor='#ffffff')
        self.todo.bind('<FocusOut>', lambda e: self.todo.selection_clear(0, END))
        self.todo.bind("<Button-3>", self.showMenu)
        self.reset()
        text = font.Font(family='Helvetica', size=12)
        self.todo.config(font=text, background='#e6f0ff')

        #*  Scrollbars for the Listbox component
        scrollx = autoscrollbar(self.todo, orient='horizontal')
        scrolly = autoscrollbar(self.todo, orient='vertical')

        #*  Configure the listbox with the scrollbars
        self.todo.configure(yscrollcommand=scrolly.set)
        self.todo.configure(xscrollcommand=scrollx.set)
        scrollx.config(command=self.todo.xview)
        scrolly.config(command=self.todo.yview)

        #*  Commands in the menu
        self.menu = tk.Menu(self.todo, tearoff=0)
        self.menu.add_command(label='Add', command=lambda: self.add())
        self.menu.add_command(label='Edit', command=lambda: self.edit())
        self.menu.add_command(label='Delete', command=lambda: self.remove())
        self.menu.add_command(label='Clear List', command=lambda: self.clear())

        #*  Pack the GUI components
        self.todo.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def showMenu(self, event):
        """Shows the menu on right click

        Args:
            event (Event): The mouse event
        """
        #*  Check if an item is selected and disable/enable buttons accordingly
        if not self.todo.curselection():
            self.menu.entryconfig('Edit', state=tk.DISABLED)
            self.menu.entryconfig('Delete', state=tk.DISABLED)
        else:
            self.menu.entryconfig('Edit', state=tk.NORMAL)
            self.menu.entryconfig('Delete', state=tk.NORMAL)

        self.menu.post(event.x_root, event.y_root)

    def edit(self):
        """Command for the edit button
        """
        if self.todo.curselection():
            item = self.todo.get(self.todo.curselection()[0]).replace(' - ', '')
            newItem = askstring('Enter Item', 'Change item to:', initialvalue=item)

            if newItem:
                self.database.set(table='list', value=newItem, item=item)
                self.reset()

    def add(self):
        """Command for the add button
        """
        item = askstring('Enter Item', 'Item to add:')

        if item:
            self.database.insert(table='list', value=item)
            self.reset()

    def remove(self):
        """Command for the remove button
        """
        if self.todo.curselection():
            self.database.delete('list', self.todo.get(self.todo.curselection()[0]).replace(' - ', ''))    #!Remove the selected item only
            self.reset()

    def clear(self):
        """Command for the clear button
        """
        #*  Ask the user for confirmation
        if messagebox.askyesno('Are you sure?', 'Do you wish to clear the entire list?'):
            self.database.truncate(table='list') #!Clear the entire list
            self.reset()

    def reset(self):
        """Reset the list
        """
        self.todo.delete(0, self.todo.size())
        for i in self.database.select(table='list', columns='item'):
            self.todo.insert(self.todo.size(), ' - ' + str(i[0]))

        #!  Create a blank item at the end of the list box and set it as unselectable to make room for the packed horizontal scrollbar
        self.todo.insert(self.todo.size(), '')
        self.todo.itemconfig(self.todo.size() - 1, fg="gray")
        def no_selection(event, index):
            if len(self.todo.curselection()) != 0:
                if str(self.todo.curselection()[0]) in str(index):
                    self.todo.selection_clear(index)
        self.todo.bind("<<ListboxSelect>>", lambda event, index=self.todo.size() - 1: no_selection(event, self.todo.size() - 1))
        self.todo.config(height=self.todo.size())