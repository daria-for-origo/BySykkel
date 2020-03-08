import tkinter as tk
import tkinter.ttk 

import BySykkelModel
import BySykkelView
import BySykkelParams

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

'''
Main
'''

args = BySykkelParams.parser.parse_args()

window = tk.Tk()
w1 = tk.PanedWindow(window)
w1.pack(fill=tk.BOTH, expand=1)

'''
See fixed_map above for the explanation
'''
style = tk.ttk.Style()
style.map('Treeview', foreground=fixed_map(style, 'foreground'), background=fixed_map(style, 'background'))

'''
Prepare data model
'''
model = BySykkelModel.Source(args.gbfs, args.client_id)

'''
Update window with system information 
'''
window.title(model.system.format("Operert av {0}.\tSpørsmål? Ring {1} eller send epost to {2}"))

'''
Create TreeView 
'''
view = BySykkelView.TreeView(window, model, "Treeview")
current_location = tk.StringVar()
current_location.set(args.location)
current_location_label = tk.Label(w1, textvariable=current_location)
w1.add(current_location_label)

def get_current_position():
    '''
    This is only a placeholder
    '''
    return BySykkelModel.GPSLocation.parse(current_location.get())

def demo():
    current_location.set(str(test.location()))
    view.update(test.bikes(), test.docks(), test.location())
  

def update():
    view.update(args.bikes, args.docks, get_current_position())
    window.after(args.interval*1000, update)


if args.demo:
    w2 = tk.PanedWindow(window) 
    w2.pack(fill=tk.X, expand=1)
    run_demo_button = tk.Button(w2, text="Interaktiv Demo\n(trykk her)", command=demo)
    w2.add(run_demo_button)
    w3 = tk.PanedWindow(w2)
    w2.add(w3)
    test = BySykkelView.InteractiveDemo(w3, args.bikes, args.docks, 
                                        BySykkelModel.GPSLocation.parse(args.location))

    window.after(0, demo)

else:
    
    window.after(0, update)

window.mainloop()
