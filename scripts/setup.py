import os
import tkinter as tk
# Declare data objects (will add setting objects later)
setup_items = { 
    'instrument': None, 
    'meas_foldername': "measurement-files", 
    'meas_folderpath': None,
}
        
def _get_csv_folder_path(folder_name):
    # Create csv folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # Get the relative path to the folder
    rel_path = os.path.join(os.getcwd(), folder_name)
    return rel_path


def _select_instrument_resource(setup_items, rm):
    # Button function to return the chosen resource and close the GUI
    def choose_resource():
        setup_items['instrument'] = listbox.get(tk.ACTIVE)
        print("Selected Instrument Is: " + setup_items['instrument']) 
        root.destroy()  # Close the GUI
    
    # List available resources
    available_resources = rm.list_resources()
    
    # Create a GUI to select the instrument
    root = tk.Tk()
    root.title("Select Instrument")
    root.geometry("640x400")  
    root.resizable(False, False)  
    
    # Create a listbox and add availble resources
    listbox = tk.Listbox(root, font=("Helvetica", 12), selectmode=tk.SINGLE)
    for resource in available_resources:
        listbox.insert(tk.END, resource)
        
    listbox.pack(expand=True, fill=tk.BOTH)
    
    ok_button = tk.Button(root, text="OK", command=choose_resource)
    ok_button.pack()

    root.mainloop()