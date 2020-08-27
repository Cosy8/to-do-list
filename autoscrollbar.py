import tkinter as tk

#!  Class to overwrite the scrollbar class, makes the scrollbars auto disappear
class autoscrollbar(tk.Scrollbar):
    #   Overwriten
    def set(self, low, high):
        #*  If the bar can't be scrolled, drop the component
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.pack_forget()
        else:
            if self.cget('orient') == tk.VERTICAL:
                self.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self.pack(side=tk.BOTTOM, fill=tk.X)
        self.master.update()
        tk.Scrollbar.set(self, low, high)