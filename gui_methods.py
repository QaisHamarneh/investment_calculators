import tkinter
import customtkinter
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mplcursors import cursor


def define_info_frame(frame, message):
    info_frame = customtkinter.CTkFrame(master=frame)
    info_frame.grid(row=11, column=1, columnspan=2)

    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_rowconfigure(1, weight=1)

    info_label = customtkinter.CTkLabel(master=info_frame, justify=tkinter.CENTER,
                                        text=f"  {message}  ")
    info_label.grid(row=1, column=1)


def define_row(frame, label, default, row):
    label = customtkinter.CTkLabel(master=frame,
                                   justify=tkinter.CENTER,
                                   text=f"{label}: ")
    label.grid(row=row, column=1)
    entry = customtkinter.CTkEntry(master=frame, placeholder_text=str(default))
    entry.grid(row=row, column=2)
    return entry


def define_results_frame(frame, row, labels):
    results_frame = customtkinter.CTkFrame(master=frame)
    results_frame.grid(row=row, column=2)
    results_frame.grid_columnconfigure((1, 2), weight=1)
    entries = []
    for i, label in enumerate(labels):
        tk_label = customtkinter.CTkLabel(master=results_frame, justify=tkinter.CENTER,
                                          text=f"  {label}  ")
        tk_label.grid(row=2 + i, column=1)
        result = customtkinter.CTkLabel(master=results_frame, justify=tkinter.LEFT, text="")
        result.grid(row=2 + i, column=2)
        entries.append(result)
    return entries


def get_entry_value(entry: customtkinter.CTkEntry, default, num):
    entry_input = entry.get()
    if entry_input == '':
        return default
    else:
        try:
            return num(entry_input)
        except ValueError:
            entry.configure(fg_color="red")
            return IOError


def draw_figure(frame, period, money_lists: dict, years: bool = False):
    fig = Figure(figsize=(6, 4), dpi=100)
    t = np.arange(period + 1)
    plot = fig.add_subplot(111)
    max_money = np.max(list(money_lists.values()))
    for label, money_list in money_lists.items():
        plot.plot(t, money_list / 1000 if max_money > 100_000 else money_list,
                  label=label)
    plot.set_xlabel("Years")
    plot.set_ylabel("Money (in 1000)" if max_money > 100_000 else "Money")
    plot.legend(loc=2)
    if not years:
        plot.set_xticks([x for x in t if x % 2 == 0] if len(t) > 10 else t)
    else:
        plot.set_xticks([x for x in t if x % 24 == 0] if len(t) > 120 else
                        [x for x in t if x % 12 == 0])
        plot.set_xticklabels([x // 12 for x in t if x % 24 == 0] if len(t) > 120 else
                             [x // 12 for x in t if x % 12 == 0])

    cursor(fig, hover=True)
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def calculate_button(frame, row, calculate_callback):
    lf_calculate_loan_button = customtkinter.CTkButton(master=frame, command=calculate_callback,
                                                       text="Calculate")
    lf_calculate_loan_button.grid(row=row, column=1)


def write_results(label, results):
    label.configure(text=f"=  {round(results):,}  ")
