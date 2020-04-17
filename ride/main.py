import tkinter as tk
import tkinter.ttk 

import BySykkelConfig
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
Enjoy the ride
'''

args = BySykkelParams.parser.parse_args()

if args.silent:
    BySykkelConfig.SilentRun = True

mainWindow = tk.Tk()


currentPositionPane = tk.PanedWindow(mainWindow)
currentPositionPane.pack(fill=tk.BOTH, expand=1)

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
mainWindow.title(model.system.format("Operert av {0}.\tSpørsmål? Ring {1} eller send epost to {2}"))

'''
Create TreeView 
'''
view = BySykkelView.TreeView(mainWindow, model, "Treeview")

'''
Current Location Label
'''
current_location = tk.StringVar()
current_location_label = tk.Label(currentPositionPane, textvariable=current_location)
current_location.set(args.location)
currentPositionPane.add(current_location_label)

def get_current_position():
    '''
    This is only a placeholder
    Alas
    '''
    return BySykkelModel.GPSLocation.parse(current_location.get())

def demo():
    '''
    Update by request using interactive demo settings
    (+)Update also current_location so it will look nice
    '''
    current_location.set(test.location())
    view.update(test.bikes(), test.docks(), get_current_position())
  

def update():
    '''
    Constant update using setup parameters and current location
    '''
    view.update(args.bikes, args.docks, get_current_position())
    mainWindow.after(args.interval*1000, update)


if args.demo:
    '''
    Create Interactive Demo section (--demo option)
    Ugly code to separate button from the rest of the settings
    '''
    demoPane = tk.PanedWindow(mainWindow) 
    demoPane.pack(fill=tk.X, expand=1)
    demo_label = tk.Label(demoPane, text="Interaktiv Demo")
    demoPane.add(demo_label)
    
    demoSettingsPane = tk.PanedWindow(demoPane)
    demoPane.add(demoSettingsPane)
    test = BySykkelView.InteractiveDemo(demoSettingsPane, 
                                        args.bikes, args.docks, 
                                        get_current_position())

    demo_button = tk.Button(demoPane, text="Trykk Her", command=demo)
    demoPane.add(demo_button)

    mainWindow.after(0, demo)

else:
    '''
    Start constant update
    '''
    mainWindow.after(0, update)

mainWindow.mainloop()
