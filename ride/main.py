import tkinter as tk
import tkinter.ttk 

import BySykkelModel
import BySykkelView


import sys, getopt

def fixed_map(style, option):
    '''
    This bit of code was copied here to resolve specific problem with 
    python/tkinter versions 
    '''
    # Fix for setting text colour for tk 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
      elm[:2] != ('!disabled', '!selected')]


def main():
    window = tk.Tk()
    
    w1 = tk.PanedWindow(window)
    w2 = tk.PanedWindow(window)

    w1.pack(fill=tk.X, expand=1)
    w2.pack(fill=tk.X, expand=1)

    style = tk.ttk.Style()
    style.map('Treeview', foreground=fixed_map(style, 'foreground'), background=fixed_map(style, 'background'))

    '''
    <Offline Test>
    model = BySykkelModel.Source("offline/gbfs.json", "")
    '''
    model = BySykkelModel.Source("https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json", "Daria-Klukin-for-Origo")
    
    
    window.title(str(model.system.format("{0} {1} {2}")))

    view = BySykkelView.TreeView(w1, model, "Treeview")
    view.pack(side=tk.TOP,fill=tk.X)

    test = BySykkelView.InteractiveInput(w2)


    def update():
        view.update(int(test.bikes.get()), 
                    int(test.docks.get()), 
                    float(test.lat.get()), 
                    float(test.lon.get()))

        window.after(10000, update)
        print(model.system)

    window.after(0, update)
    window.mainloop()


if __name__ == "__main__":
    main()