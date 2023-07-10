import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import pandas as pd
from app import process_data


def main() -> None:
    data: pd.DataFrame
    processed_data: pd.DataFrame

    def load_csv():
        nonlocal data
        # Code to load the CSV file
        file_path = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        data = pd.read_csv(file_path)
        mb.showinfo("Import", "Data successfully loaded!")

    def show_input_data():
        nonlocal data
        # Clear widget from previous data
        text_widget.delete("1.0", tk.END)
        try:
            # Set the text of the widget to the data
            text_widget.insert(tk.END, str(data))
        except NameError:
            mb.showinfo("Error", "No data to show!")

    def analyze_data():
        nonlocal data
        nonlocal processed_data
        nonlocal selected_option
        if data is None:
            mb.showerror("Error", "Please load data first!")
            return
        processed_data = process_data(data, selected_option.get())
        # Clear widget from previous data
        text_widget.delete("1.0", tk.END)
        # set the text of the widget to the data
        text_widget.insert(tk.END, str(processed_data))

    def export_data():
        nonlocal processed_data
        file_path = fd.asksaveasfile(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if file_path is not None:
            processed_data.to_csv(file_path, index=False)
            mb.showinfo("Export", "Data exported successfully!")

    # Create the main window
    root = tk.Tk()
    root.title("Data Processing GUI")

    # Create the widgets for the GUI
    load_button = tk.Button(root, text="Load CSV", command=load_csv)
    show_input_data_button = tk.Button(
        root, text="Show input data", command=show_input_data
    )
    analyze_button = tk.Button(root, text="Analyze Data", command=analyze_data)
    # Create a variable to store the selected option
    selected_option = tk.StringVar(root)
    # Create a list of options
    options = ["All", "Temperature", "Humidity", "CO2"]
    # Set the default selected option
    selected_option.set(options[0])
    # Create an OptionMenu widget
    option_menu = tk.OptionMenu(root, selected_option, *options)

    export_button = tk.Button(root, text="Export Data", command=export_data)
    # Create a Text widget to display the data
    text_widget = tk.Text(root)

    # Arrange the widgets in the main window
    text_widget.pack(side=tk.BOTTOM)
    load_button.pack(side=tk.LEFT)
    show_input_data_button.pack(side=tk.LEFT)
    analyze_button.pack(side=tk.LEFT)
    option_menu.pack(side=tk.LEFT)
    export_button.pack(side=tk.LEFT)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
