import os
import json
from pathlib import Path

import tkinter as tk

from expert import ExpertSystem


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.__expert = ExpertSystem()

        self.__question_path = Path('questions').resolve()
        self.__questions = os.listdir(self.__question_path)
        self.__questions_data = [{}] * len(self.__questions)
        self.__current_question_inx = 0
        self.__selected_list = list()

        self.__answers = [0.0] * len(self.__questions)

        self.__responses = Path('responses').resolve()

        with open('./source/compare.json', 'r', encoding='cp1251') as file:
            self.__compare = json.load(file)

        self.__listbox_dict = dict()
        self.__listbox_match_dict = dict()

        tk.Frame.__init__(self, *args, **kwargs)
        root.title("ЭКСПЕРТНАЯ СИСТЕМА")

        width = 600
        height = 500

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.__lable = tk.Label(root)
        self.__lable["text"] = "Это экспертная система, которая поможет Вам выбрать авто"
        self.__lable.place(x=50, y=30, width=500, height=50)

        back_btn = tk.Button(root)
        back_btn["text"] = "Back"
        back_btn.place(x=100, y=390, width=158, height=35)
        back_btn["command"] = self.__previous_question

        self.__next_btn = tk.Button(root)
        self.__next_btn["text"] = "Next"
        self.__next_btn.place(x=300, y=390, width=158, height=35)
        self.__next_btn["command"] = self.__next_question

        self.__listbox = tk.Listbox(root)
        self.__listbox.place(x=220, y=100, width=180, height=215)
        self.__listbox["exportselection"] = "0"
        self.__listbox["selectmode"] = "single"
        self.__listbox.place_forget()

    def __next_question(self):
        new_listbox_data = dict()
        is_selected = bool(self.__current_question_inx != 0)

        if not self.__listbox.curselection() and 0 != self.__current_question_inx:
            return

        if is_selected:
            cursor = self.__listbox.get(self.__listbox.curselection())
            self.__selected_list.append(cursor)
            answer = self.__questions_data[self.__current_question_inx - 1][cursor]
            self.__answers[self.__current_question_inx - 1] = answer
            if len(self.__questions) > self.__current_question_inx:
                name = self.__questions[self.__current_question_inx].split('.')[0]
                for selected in self.__selected_list:
                    if selected in self.__compare and name in self.__compare[selected]:
                        new_listbox_data = self.__compare[selected][name]

        if len(self.__questions) <= self.__current_question_inx:
            self.__listbox.place_forget()
            self.__lable['text'] = "Спасибо за то что используете нашу программу!"
            self.__next_btn["text"] = 'Exit'
            self.__show_result()
            self.__next_btn["command"] = exit
            return

        self.__answers[self.__current_question_inx] = self.__listbox.curselection()

        self.__listbox.delete(0, tk.END)

        with open(self.__question_path / self.__questions[self.__current_question_inx], 'r', encoding='utf-8') as file:
            question_data = json.load(file)

        self.__lable['text'] = question_data['title']

        if not new_listbox_data:
            new_listbox_data = question_data['data']

        self.__questions_data[self.__current_question_inx] = new_listbox_data

        for key, value in new_listbox_data.items():
            self.__listbox.insert(value, key)

        self.__listbox.place(x=220, y=100, width=180, height=215)
        self.__current_question_inx += 1

    def __previous_question(self):
        if 1 == self.__current_question_inx:
            return

        self.__listbox.delete(0, tk.END)

        self.__current_question_inx -= 1

        for key, value in self.__questions_data[self.__current_question_inx - 1].items():
            self.__listbox.insert(value, key)

    def __call_expert(self) -> list:
        fuzzy_logical_list = self.__expert.fuzzy_logical_output(self.__answers)
        aggregate_list = self.__expert.aggregate(fuzzy_logical_list)
        result = self.__expert.dephasifier(aggregate_list)
        return result

    def __show_result(self):
        output = list()
        expert_output = self.__call_expert()

        for subset in expert_output:
            if f'{subset["number"]}.json' in os.listdir(self.__responses):
                with open(self.__responses / f'{subset["number"]}.json', 'r') as responses:
                    response = json.load(responses)
                    response = ';'.join(response)
                    output.append(f'{response} with {subset["weight"]}')
            else:
                output.append(f'car list №{subset["number"]} with {subset["weight"]}')

        window = tk.Toplevel(self)

        window.wm_title("Подобравнные авто")
        lable = tk.Label(window, text='\n'.join(output))
        lable.pack(side="top", fill="both", expand=True, padx=100, pady=100)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()
