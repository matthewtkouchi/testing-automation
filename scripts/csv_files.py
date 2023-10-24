import os
import pandas as pd
import numpy as np
import tkinter as tk
# import user defined functions
from setup import _get_csv_folder_path
# import user defined data structures
from setup import setup_items

def get_filenames(dir):     # Get all csv filenames in a directory
    return [fname for fname in os.listdir(dir) if fname.endswith(".csv")]


def create_filename_text_widgets(root, filenames):      # Create rename GUI widgets
    text_widgets = []
    for i, filename in enumerate(filenames):
        # Create labels (col 1)
        label = tk.Label(root, text=f"File {i + 1}:")
        label.grid(row=i, column=0)
        # Remove the file extension
        filename = os.path.splitext(filename)[0]   # its okay to remove .csv since filenames only contain .csv files from the get_filenames call
        # Create text entry (col 2)
        entry = tk.Entry(root)
        entry.insert(0, filename)
        entry.grid(row=i, column=1)
        text_widgets.append(entry)
    return text_widgets


def save_changes(filenames, text_widgets, root):        # Handle Button Presses
    meas_path = setup_items['meas_folderpath']
    for i, entry in enumerate(text_widgets):
        new_name = entry.get()
        if new_name:
            old_name = filenames[i]
            old_path = os.path.join(meas_path, old_name)
            new_path = os.path.join(meas_path, new_name + ".csv")
            os.rename(old_path, new_path)
            filenames[i] = new_name  # update filenames array
    print(filenames)
    root.destroy()
    
    
def cancel_changes(root):       # Handle Button Presses
    root.destroy()
    

def rename_csv_files(dir):      # Rename CSV files in a directory
    # Get file names
    filenames = get_filenames(dir)  # filenames are only files that contain .csv
    print(filenames)
    # Render GUI
    root = tk.Tk()
    root.title("Rename CSV Files")
    root.geometry("640x400")
    root.resizable(False, False)
    # Render widgets for text entry
    text_widgets = create_filename_text_widgets(root, filenames)
    # Buttons to save changes or cancel changes
    ok_button = tk.Button(root, text="OK", command=lambda: save_changes(filenames, text_widgets, root))
    ok_button.grid(row=len(filenames), column=0)
    cancel_button = tk.Button(root, text="Cancel", command=lambda: cancel_changes(root))
    cancel_button.grid(row=len(filenames), column=1)
    # Run until button is pressed and GUI is destroyed
    root.mainloop()

def process_csv_files(dir):
    # Create a directory named 'watts' inside the measurement-files directory
    output_folder = os.path.join(dir, 'watts')
    os.makedirs(output_folder, exist_ok=True)   # Only make if it doesn't already exist
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame()
    # Get all CSV files in measurment-files
    csv_files = get_filenames(dir)
    # Extract the angles from the first CSV file (assuming angles are the same for all)
    temp_path = os.path.join(dir, csv_files[0])
    temp_df = pd.read_csv(temp_path)
    angles = temp_df['angle']
    # Add the "angle" column as the first column in result_df
    result_df['angle'] = angles
    for csv_file in csv_files:
        file_path = os.path.join(dir, csv_file)
        df = pd.read_csv(file_path)
        # Check if 'power(dBm)' column exists in the DataFrame
        if 'power(dBm)' not in df.columns:
            print(f"Ignored file: {csv_file} (No 'power(dBm)' column)")
            continue
        # Convert "power(dBm)" to Watts using the reference value of 1 mW = 0 dBm and store in new df
        df['Watts'] = 10 ** ((df['power(dBm)'] - 30) / 10)
        column_name = os.path.splitext(csv_file)[0]
        result_df[column_name] = df['Watts']
    # Save the result DataFrame to a CSV file in the 'output' folder
    output_file = os.path.join(output_folder, "combined-linear.csv")
    result_df.to_csv(output_file, index=False)
    print(f"Conversion completed. Output saved to {output_file}")
    
# Example usage:
csv_dir = _get_csv_folder_path(setup_items['meas_foldername'])
setup_items['meas_folderpath'] = csv_dir
process_csv_files(csv_dir)
