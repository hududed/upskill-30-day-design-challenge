import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import pandas as pd
from app import process_data


class Model:
    def __init__(self) -> None:
        self.__data: pd.DataFrame = pd.DataFrame()
        self.__processed_data: pd.DataFrame = pd.DataFrame()

    @property
    def data(self) -> pd.DataFrame:
        return self.__data
    
    @data.setter
    def data(self, value: pd.DataFrame) -> None:
        self.__data = value

    @property
    def processed_data(self) -> pd.DataFrame:
        return self.__processed_data
    
    @processed_data.setter
    def processed_data(self, value: pd.DataFrame) -> None:
        self.__processed_data = value


class View:
    def __init__(self) -> None:
        self.presenter = Presenter
        self.master = tk.Tk()
        self.master.title("Data Analysis Tool")

        self.load_button = tk.Button(
            self.master, text="Load CSV", command=self.on_load_csv_button_click
        )
        self.show_input_data_button = tk.Button(
            self.master,
            text="Show Input Data",
            command=self.on_show_input_data_button_click,
            state="disabled",
        )
        self.analyze_button = tk.Button(
            self.master,
            text="Analyze Data",
            command=self.on_analyze_button_click,
            state="disabled",
        )
        self.selected_option = tk.StringVar(self.master)
        self.options = ["All", "Temperature", "Humidity", "CO2"]
        self.selected_option.set(self.options[0])
        self.option_menu = tk.OptionMenu(
            self.master, self.selected_option, *self.options
        )
        self.export_button = tk.Button(
            self.master,
            text="Export Data",
            command=self.on_export_button_click,
            state="disabled",
        )
        self.text_widget = tk.Text(self.master)

        self.text_widget.pack(side=tk.BOTTOM)
        self.load_button.pack(side=tk.LEFT)
        self.show_input_data_button.pack(side=tk.LEFT)
        self.analyze_button.pack(side=tk.LEFT)
        self.option_menu.pack(side=tk.LEFT)
        self.export_button.pack(side=tk.LEFT)

    def set_data(self, data: pd.DataFrame) -> None:
        self.text_widget.delete("1.0", tk.END)
        
        try:
            self.text_widget.insert(tk.END, str(data))
        except NameError:
            mb.showinfo("Error", "No data to show")

    def on_load_csv_button_click(self) -> None:
        file_path = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.presenter.load_csv(file_path)
            mb.showinfo("Success", "CSV file loaded successfully")
            self.show_input_data_button["state"] = "normal"
            self.analyze_button["state"] = "normal"
            self.export_button["state"] = "normal"

    def on_show_input_data_button_click(self) -> None:
        self.presenter.show_input_data()

    def on_analyze_button_click(self) -> None:
        self.presenter.analyze_data(self.selected_option.get())

    def on_export_button_click(self) -> None:
        file_path = fd.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.presenter.export_data(file_path)
            mb.showinfo("Success", "CSV file exported successfully")
    
class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
    def load_csv(self, file_path: str) -> None:
        self.model.data = pd.read_csv(file_path)
    
    def show_input_data(self) -> None:
        self.view.set_data(self.model.data)
    
    def analyze_data(self, selected_option: str) -> None:
        self.model.processed_data = process_data(self.model.data, selected_option)
        self.view.set_data(self.model.processed_data)

    def export_data(self, file_path: str) -> None:
        self.model.processed_data.to_csv(file_path)

def main() -> None:
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    view.presenter = presenter
    view.master.mainloop()

if __name__ == "__main__":
    main()            

