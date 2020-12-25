import tkinter as tk

class autoscrollbar(tk.Scrollbar):
    """Class to overwrite the scrollbar class, makes the scrollbars auto disappear

    Args:
        tk.Scrollbar (Scrollbar): The scrollbar being customized
    """
    def set(self, low, high):
        """***Overwriten method***

        Args:
            low (float): Lowest scrollable point
            high (float): Highest scrollable point
        """
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