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
        cols = ['Stasjon', 'KM', 'Sykkler', 'Ledige Plasser', 'Adresse']
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
          
    def update(self, bikes, docks, lat, lon):        
        '''
        Triggers full treeview re-load
        If model can not be reloaded, the view will remain unchanged
        '''
        if self.model.update(BySykkelModel.GPSLocation(lat, lon)):
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
                    values=("{:.3f}".format(row.distance), row.bikes, row.docks, row.address))


class InteractiveInput:
   def  __init__(self, w):
        tk.Label(w, text="Min bikes").grid(row=0)
        tk.Label(w, text="Min docks").grid(row=1)
        tk.Label(w, text="Latitude").grid(row=2)
        tk.Label(w, text="Longitude").grid(row=3)

        self.bikes = tk.Entry(w)
        self.bikes.insert(tk.END, "1")
        self.docks = tk.Entry(w)
        self.docks.insert(tk.END, "1")
        self.lat = tk.Entry(w)
        self.lat.insert(tk.END, "59.915096")
        self.lon = tk.Entry(w)
        self.lon.insert(tk.END, "10.7312715")

        self.bikes.grid(row=0, column=1)
        self.docks.grid(row=1, column=1)
        self.lat.grid(row=2, column=1)
        self.lon.grid(row=3, column=1)
