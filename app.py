import os
import json
import pathlib

import tkinter as tk

from expert import ExpertSystem


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.__expert = ExpertSystem()
        self._listbox_data_dir = pathlib.Path('./list_box_data').resolve()
        self.__listbox_list = list()
        self.__listbox_match_dict = dict()
        tk.Frame.__init__(self, *args, **kwargs)
        root.title("ЭС")
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GListBox_220 = tk.Listbox(root, exportselection=0)
        GListBox_220.place(x=100, y=130, width=142, height=30)
        self.__listbox_list.append(GListBox_220)

        GListBox_983 = tk.Listbox(root, exportselection=0)
        GListBox_983.place(x=350, y=130, width=144, height=31)
        self.__listbox_list.append(GListBox_983)

        GListBox_458 = tk.Listbox(root, exportselection=0)
        GListBox_458.place(x=100, y=210, width=141, height=30)
        self.__listbox_list.append(GListBox_458)

        GListBox_624 = tk.Listbox(root, exportselection=0)
        GListBox_624.place(x=350, y=210, width=147, height=30)
        self.__listbox_list.append(GListBox_624)

        GListBox_62 = tk.Listbox(root, exportselection=0)
        GListBox_62.place(x=100, y=290, width=141, height=30)
        self.__listbox_list.append(GListBox_62)

        GListBox_57 = tk.Listbox(root, exportselection=0)
        GListBox_57.place(x=350, y=290, width=146, height=30)
        self.__listbox_list.append(GListBox_57)

        GLabel_234 = tk.Label(root)
        GLabel_234["text"] = "Выбери нужные параметры"
        GLabel_234.place(x=200, y=30, width=180, height=30)

        GButton_351 = tk.Button(root)
        GButton_351["text"] = "Подобрать"
        GButton_351.place(x=200, y=390, width=158, height=35)
        GButton_351["command"] = self.button_click_command
        self._append_listbox_data()

    def _append_listbox_data(self):
        data_list = list()

        for file_name in os.listdir(self._listbox_data_dir):
            with open(self._listbox_data_dir / file_name) as file:
                data_list.append(json.load(file))

        for listbox, listbox_dict in zip(self.__listbox_list, data_list):
            self.__listbox_match_dict[listbox] = listbox_dict
            for name, value in listbox_dict.items():
                listbox.insert(value, name)

    def _execute(self, phasifired_list: list) -> list:
        fuzzy_logical_list = self.__expert.fuzzy_logical_output(phasifired_list)
        aggregate_list = self.__expert.aggregate(fuzzy_logical_list)
        result = self.__expert.dephasifier(aggregate_list)
        return result

    def button_click_command(self):
        phasifired_list = list()
        for box in self.__listbox_list:
            value = self.__listbox_match_dict[box][box.get(box.curselection())]
            phasifired_list.append(value)

        expert_output = self._execute(phasifired_list)
        expert_output = '\n'.join(expert_output)

        window = tk.Toplevel(self)
        window.wm_title("Подобравнные авто")
        lable = tk.Label(window, text=expert_output)
        lable.pack(side="top", fill="both", expand=True, padx=100, pady=100)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()
