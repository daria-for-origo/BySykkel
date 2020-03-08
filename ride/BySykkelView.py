import tkinter as tk
import tkinter.ttk 

import BySykkelModel

class TreeView(tk.ttk.Treeview):
    '''
    Unfortunetely, this is not a smart piece of a program
    Using only basic functions of tk, it provides minimalistic design
    for demostrating BySykkelModel (which is better than that)
    '''
    def __init__(self, window, model, style):
        self.model = model
        cols = [model.system.name + " Stasjoner", 'Avstand', 'Sykkler', 'Ledige Plasser', 'Adresse']
        super().__init__(window, columns=cols[1:], style=style, show='tree')
        vsb = tkinter.ttk.Scrollbar(window, orient="vertical", command=self.yview)
        vsb.pack(side='right', fill='y')
        self.configure(yscrollcommand=vsb.set)

        '''
        This is a dirty trick to make first level of a tree to look like a header
        Root element of tree view can not be removed, so it is usefull to keep
        all other rows under root level - than they are easy to replace 
        '''
        self.root = self.insert("", 1, text=cols[0], values=cols[1:], open=True)

        self.tag_configure('filter', foreground='gray')

        self.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

          
    def update(self, bikes, docks, gps_location):        
        '''
        Triggers full treeview re-load
        If model can not be reloaded, the view will remain unchanged
        '''
        if self.model.update(gps_location):
            self.delete(*self.get_children(self.root))
            for row in self.model.status:
                row_tags = list()
                if row.bikes < bikes or row.docks < docks:
                    '''
                    Matter of choice, should be left to the gui of course
                    Here, all entries that are not-relevant to the user
                    will be shown in gray - for testing purposes
                    '''
                    row_tags.append('filter')
                self.insert(self.root, "end", text=row.name, tags = row_tags, \
                    values=("{:.3f} km".format(row.distance), row.bikes, row.docks, row.address))


class InteractiveDemo:
    '''
    Module for interactive test of BySykkelModel/BySykkelView
    '''
    def  __init__(self, w, bikes, docks, gps_location):
        tk.Label(w, text="Sykkler").grid(row=0, column=0)
        tk.Label(w, text="Plasser").grid(row=1, column=0)
        tk.Label(w, text="GPS Lokasjon").grid(row=0, column=2)

        self._bikes = tk.Entry(w)
        self._bikes.insert(tk.END, bikes)
        self._docks = tk.Entry(w)
        self._docks.insert(tk.END, docks)
        self._gps = tk.Entry(w)
        self._gps.insert(tk.END, str(gps_location))
       
        self._bikes.grid(row=0, column=1)
        self._docks.grid(row=1, column=1)
        self._gps.grid(row=0, column=3)

    def bikes(self):
        return int(self._bikes.get())

    def docks(self):
        return int(self._docks.get())

    def location(self):
        return self._gps.get()
