import os
import json
import pathlib

import tkinter as tk

from expert import ExpertSystem


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.__expert = ExpertSystem()
        self._listbox_data_dir = pathlib.Path('./list_box_data').resolve()

        with open('./source/compare.json', 'r') as file:
            self.__compare = json.load(file)

        self.__listbox_dict = dict()
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
        GListBox_220.place(x=100, y=130, width=140, height=30)
        self.__listbox_dict['body_work'] = GListBox_220
        self.__listbox_dict['body_work'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('body_work')
        )

        GListBox_983 = tk.Listbox(root, exportselection=0)
        GListBox_983.place(x=350, y=130, width=140, height=30)
        self.__listbox_dict['budget'] = GListBox_983
        self.__listbox_dict['budget'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('budget')
        )

        GListBox_458 = tk.Listbox(root, exportselection=0)
        GListBox_458.place(x=100, y=210, width=140, height=30)
        self.__listbox_dict['condition'] = GListBox_458
        self.__listbox_dict['condition'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('condition')
        )

        GListBox_624 = tk.Listbox(root, exportselection=0)
        GListBox_624.place(x=350, y=210, width=140, height=30)
        self.__listbox_dict['gear_box'] = GListBox_624
        self.__listbox_dict['gear_box'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('gear_box')
        )

        GListBox_62 = tk.Listbox(root, exportselection=0)
        GListBox_62.place(x=100, y=290, width=140, height=30)
        self.__listbox_dict['nsumber_of_passengers'] = GListBox_62
        self.__listbox_dict['nsumber_of_passengers'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('nsumber_of_passengers')
        )

        GListBox_57 = tk.Listbox(root, exportselection=0)
        GListBox_57.place(x=350, y=290, width=140, height=30)
        self.__listbox_dict['purpose'] = GListBox_57
        self.__listbox_dict['purpose'].bind(
            "<<ListboxSelect>>",
            lambda x: self._select_listbox_callback('purpose')
        )

        GLabel_234 = tk.Label(root)
        GLabel_234["text"] = "Выбери нужные параметры"
        GLabel_234.place(x=200, y=30, width=180, height=30)

        GButton_351 = tk.Button(root)
        GButton_351["text"] = "Подобрать"
        GButton_351.place(x=200, y=390, width=158, height=35)
        GButton_351["command"] = self.button_click_command
        self._append_listbox_data()

    def _append_listbox_data(self):
        for file_name in os.listdir(self._listbox_data_dir):
            with open(self._listbox_data_dir / file_name) as file:
                listbox_dict = json.load(file)
                _file = self._listbox_data_dir / file_name
                self.__listbox_match_dict[_file.stem] = listbox_dict
                for name, value in listbox_dict.items():
                    self.__listbox_dict[_file.stem].insert(value, name)

    def _execute(self, phasifired_list: list) -> list:
        fuzzy_logical_list = self.__expert.fuzzy_logical_output(phasifired_list)
        aggregate_list = self.__expert.aggregate(fuzzy_logical_list)
        result = self.__expert.dephasifier(aggregate_list)
        return result

    def _select_listbox_callback(self, name):
        box = self.__listbox_dict[name]

        selected = box.get(
            box.curselection()
        )

        if name not in self.__compare:
            return

        if selected not in self.__compare[name]:
            return

        for listbox_name, values_dict in self.__compare[name][selected].items():
            selected_temp = self.__listbox_dict[listbox_name].curselection()
            self.__listbox_dict[listbox_name].delete(0, tk.END)
            for key, value in values_dict.items():
                self.__listbox_dict[listbox_name].insert(value, key)
            if selected_temp:
                self.__listbox_dict[listbox_name].selection_set(*selected_temp)

    def button_click_command(self):
        phasifired_list = list()
        for checkbox_name in self.__listbox_dict.keys():

            value = self.__listbox_dict[checkbox_name].get(
                self.__listbox_dict[checkbox_name].curselection()
            )
            value = self.__listbox_match_dict[checkbox_name][value]
            print(value)
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
