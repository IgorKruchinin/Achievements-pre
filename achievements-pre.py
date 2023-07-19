import pandas as pd
import tkinter as tk
from tkinter import ttk
import os.path
from tkcalendar import DateEntry

import matplotlib.pyplot as plt

class Storage:
	def __init__(self):
		if os.path.exists("data.csv"):
			self.df = pd.read_csv("data.csv")
		else:
			self.df = pd.DataFrame({"Дата":[], "Предмет":[], "Тип достижения":[], "Достижение":[]})
	def append(self, elem={"Дата":"", "Предмет":"", "Тип достижения":"", "Достижение":0}):
		self.df = pd.concat([self.df, pd.DataFrame([elem])], ignore_index=True)
		self.df.to_csv("data.csv", index=False)

class App(Storage):
	def __init__(self):
		super().__init__()
		self.main_win = tk.Tk()
		self.main_win.geometry("800x500")
		self.main_win.title("Достижения")
		frame = tk.Frame(self.main_win)
		frame.pack(fill="both", expand=1)
		scrollx = tk.Scrollbar(frame, orient="horizontal")
		scrolly = tk.Scrollbar(frame, orient="vertical")
		self.table = ttk.Treeview(frame, xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
		self.table['columns'] = list(self.df.columns)
		self.table.column("#0", width=0, stretch='NO')
		self.table.heading("#0", text="", anchor='center')
		for colname in list(self.df.columns.values):
			self.table.column(colname, width=80, anchor='center')
			self.table.heading(colname, text=colname, anchor='center')
		for index, row in self.df.iterrows():
			self.table.insert(parent='', index='end', iid=index, text='', values=row.to_list())
		scrollx.config(command=self.table.xview)
		scrollx.pack(side="bottom", fill="x")
		scrolly.config(command=self.table.yview)
		scrolly.pack(side="right", fill="y")
		self.table.pack(fill="both", expand=1)
		fr0 = tk.Frame(self.main_win)
		date_lbl = tk.Label(fr0, text="Дата: ")
		self.date_i = DateEntry(fr0, locale="ru_RU", date_pattern="dd.MM.yyyy", width=10)
		object_lbl = tk.Label(fr0, text="Предмет:")
		self.object_i = tk.Entry(fr0, width=10)
		fr1 = tk.Frame(self.main_win)
		type_lbl = tk.Label(fr1, text="Тип достижения: ")
		self.type_i = tk.Entry(fr1, width=20)
		fr2 = tk.Frame(self.main_win)
		achivement_lbl = tk.Label(fr2, text="Достижение: ")
		self.achivement_i = tk.Entry(fr2, width=20)
		fr3 = tk.Frame(self.main_win)
		append_btn = tk.Button(fr3, text="Добавить достижение", command=self.apply)
		show_plot_btn = tk.Button(fr3, text="Смотреть график", command=self.show_plot)
		date_lbl.pack(side="left")
		self.date_i.pack(side="left")
		object_lbl.pack(side="left")
		self.object_i.pack(side="left")
		type_lbl.pack(side="left")
		self.type_i.pack(side="left")
		achivement_lbl.pack(side="left")
		self.achivement_i.pack(side="left")
		append_btn.pack(side="left")
		show_plot_btn.pack(side="left")
		fr0.pack(side="top")
		fr1.pack(side="top")
		fr2.pack(side="top")
		fr3.pack(side="top")
	def reset_table(self):
			self.table.delete(*self.table.get_children())
			#table.column("#0", width=0, stretch='NO')
			#table.heading("#0", text="", anchor='center')
			for colname in list(self.df.columns.values):
				self.table.column(colname, width=80, anchor='center')
				self.table.heading(colname, text=colname, anchor='center')
			for index, row in self.df.iterrows():
				self.table.insert(parent='', index='end', iid=index, text='', values=row.to_list())
	def apply(self):
		self.append({"Дата":pd.to_datetime(pd.Timestamp(self.date_i.get_date()), format="%d.%m.%Y"), "Предмет":self.object_i.get(), "Тип достижения":self.type_i.get(), "Достижение":int(self.achivement_i.get())})
		self.reset_table()
		self.date_i.delete(0, "end")
		self.object_i.delete(0, "end")
		self.type_i.delete(0, "end")
		self.achivement_i.delete(0, "end")
	def show_plot(self):
                df_tmp = self.df[self.df["Предмет"] == self.object_i.get()]
                df_tmp = df_tmp[df_tmp["Тип достижения"] == self.type_i.get()]
                plt.plot(df_tmp["Дата"], df_tmp["Достижение"])
                plt.xlabel("Дата")
                plt.ylabel("Достижение")
                plt.show()
                self.date_i.delete(0, "end")
                self.object_i.delete(0, "end")
                self.type_i.delete(0, "end")
                self.achivement_i.delete(0, "end")
	def run(self):
		self.main_win.mainloop()
		


App().run()
