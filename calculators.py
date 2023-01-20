import matplotlib.pyplot as plt

from gui_methods import *

from accumulated_interest_calculator import interest_calculator
from inflation_calculator import inflation_calculator
from loan_calculator import loan_calculator, higher_monthly_payment_calculator
from percentage_calculator import percentage_calculator
from retirement_calculator import retirement_calculator

plt.style.use('dark_background')
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("800x880")
app.title("Accumulated Interest Calculators")

tabview = customtkinter.CTkTabview(master=app, width=700, height=850)
tabview.pack(pady=10, padx=10)
tabview.add("Inflation")
tabview.add("Investment")
tabview.add("Retirement")
tabview.add("Percentage")
tabview.add("Loan")

###########################################################################
###################### Investment Tab #####################################
###########################################################################

investment_frame = customtkinter.CTkFrame(master=tabview.tab("Investment"))
investment_frame.pack(pady=10, padx=10, fill="both", expand=True)

investment_frame.grid_columnconfigure((1, 2), weight=1)
investment_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 11), weight=0)
investment_frame.grid_rowconfigure((0, 7, 9, 10), weight=1)

investment_info = "This tab calculates total amount of money after investing for a number of years."
define_info_frame(investment_frame, investment_info)

investment_graph_frame = customtkinter.CTkFrame(master=investment_frame)
investment_graph_frame.grid(row=9, column=1, rowspan=2, columnspan=2)

###########################################################################
if_initial_amount_entry = define_row(investment_frame, "Initial amount", 1000, 1)
if_interest_rate_entry = define_row(investment_frame, "Interest Rate (%)", 8, 2)
if_period_entry = define_row(investment_frame, "Period (in years)", 20, 3)
if_current_salary_entry = define_row(investment_frame, "Current net monthly salary", 5000, 4)
if_salary_inflation_rate_entry = define_row(investment_frame, "Salary inflation rate (%)", 5, 5)
if_percentage_deposit_entry = define_row(investment_frame, "Percentage of salary invested", 15, 6)

if_principle_res_label, if_accumulated_interest_res_label, if_total_res_label = \
    define_results_frame(investment_frame, 7,
                         ["Amount deposited",
                          "Accumulated interest",
                          "Total"])


def calculate_investment_callback():
    initial_amount = get_entry_value(if_initial_amount_entry, 1000, float)
    interest_rate = get_entry_value(if_interest_rate_entry, 8, float)
    period = get_entry_value(if_period_entry, 20, int)
    inflation_rate = get_entry_value(if_current_salary_entry, 5, float)
    current_salary = get_entry_value(if_salary_inflation_rate_entry, 5000, float)
    percentage_deposit = get_entry_value(if_percentage_deposit_entry, 15, float)

    if initial_amount == IOError or \
            interest_rate == IOError or \
            period == IOError or \
            inflation_rate == IOError or \
            current_salary == IOError or \
            percentage_deposit == IOError:
        return

    deposits, interests, totals = interest_calculator(initial_amount,
                                                      interest_rate,
                                                      period,
                                                      current_salary,
                                                      inflation_rate,
                                                      percentage_deposit)

    write_results(if_principle_res_label, deposits[-1])
    write_results(if_accumulated_interest_res_label, interests[-1])
    write_results(if_total_res_label, totals[-1])

    draw_figure(investment_graph_frame,
                period,
                {"Deposited": deposits,
                 "Accumulated interest": interests,
                 "Total": totals})


calculate_button(investment_frame, 7, calculate_investment_callback)

###########################################################################
###################### Inflation Tab ######################################
###########################################################################


inflation_frame = customtkinter.CTkFrame(master=tabview.tab("Inflation"))
inflation_frame.pack(pady=10, padx=10, fill="both", expand=True)

inflation_frame.grid_columnconfigure((1, 2), weight=1)
inflation_frame.grid_rowconfigure((1, 2, 3, 5, 6, 7, 8, 11), weight=0)
inflation_frame.grid_rowconfigure((0, 4, 9, 10), weight=1)

inflation_info = "This tab calculates the inflated amount after a number of years."
define_info_frame(inflation_frame, inflation_info)

inflation_graph_frame = customtkinter.CTkFrame(master=inflation_frame)
inflation_graph_frame.grid(row=9, column=1, rowspan=2, columnspan=2)

###########################################################################
ff_current_amount_entry = define_row(inflation_frame, "Current amount", 100, 1)
ff_period_entry = define_row(inflation_frame, "Period (in years)", 20, 2)
ff_inflation_rate_entry = define_row(inflation_frame, "Inflation rate (%)", 2, 3)

ff_principle_res_label = define_results_frame(inflation_frame, 4, ["Inflated amount"])[0]


def calculate_inflation_callback():
    current_amount = get_entry_value(ff_current_amount_entry, 100, float)
    period = get_entry_value(ff_period_entry, 20, int)
    inflation_rate = get_entry_value(ff_inflation_rate_entry, 2, float)

    if current_amount == IOError or \
            period == IOError or \
            inflation_rate == IOError:
        return

    inflated_amounts = inflation_calculator(current_amount,
                                            inflation_rate,
                                            period)

    write_results(ff_principle_res_label, inflated_amounts[-1])

    draw_figure(inflation_graph_frame,
                period,
                {"Inflated amount": inflated_amounts})


calculate_button(inflation_frame, 4, calculate_inflation_callback)

###########################################################################
###################### Retirement Tab #####################################
###########################################################################


retirement_frame = customtkinter.CTkFrame(master=tabview.tab("Retirement"))
retirement_frame.pack(pady=10, padx=10, fill="both", expand=True)

retirement_frame.grid_columnconfigure((1, 2), weight=1)
retirement_frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 11), weight=0)
retirement_frame.grid_rowconfigure((0, 8, 9, 10), weight=1)

retirement_info = "This tab calculates the required investment " \
                  "to live of the interests without draining the investment.\n" \
                  "Accounting for 25% less of the interest rate as a breathing room"
define_info_frame(retirement_frame, retirement_info)

retirement_graph_frame = customtkinter.CTkFrame(master=retirement_frame)
retirement_graph_frame.grid(row=9, column=1, rowspan=2, columnspan=2)

###########################################################################
rf_expected_salary_entry = define_row(retirement_frame,
                                      "Desired monthly salary\nat retirement (in today's values)", 5000, 1)
rf_current_salary_entry = define_row(retirement_frame, "Current net salary", 3000, 2)
rf_period_entry = define_row(retirement_frame, "Years until retirement", 20, 3)
rf_starting_amount_entry = define_row(retirement_frame, "Current saving", 10000, 4)
rf_inflation_rate_entry = define_row(retirement_frame, "Inflation rate (%)", 2, 5)
rf_salary_inflation_rate_entry = define_row(retirement_frame, "Salary inflation rate (%)", 5, 6)
rf_interest_rate_entry = define_row(retirement_frame, "Expected interest rate (%)", 8, 7)

rf_inflated_salary_res_label, rf_investment_res_label, rf_percentage_res_label = \
    define_results_frame(retirement_frame, 8,
                         ["Inflated salary",
                          "Required investment",
                          "Percentage to save"])


def calculate_retirement_callback():
    expected_salary = get_entry_value(rf_expected_salary_entry, 5000, float)
    current_salary = get_entry_value(rf_current_salary_entry, 3000, float)
    period = get_entry_value(rf_period_entry, 20, int)
    starting_amount = get_entry_value(rf_starting_amount_entry, 10000, float)
    inflation_rate = get_entry_value(rf_inflation_rate_entry, 2, float)
    salary_inflation_rate = get_entry_value(rf_salary_inflation_rate_entry, 5, float)
    interest_rate = get_entry_value(rf_interest_rate_entry, 8, float)

    if expected_salary == IOError or \
            current_salary == IOError or \
            period == IOError or \
            starting_amount == IOError or \
            inflation_rate == IOError or \
            salary_inflation_rate == IOError or \
            interest_rate == IOError:
        return

    inflated_salary, accumulated_investments, retirement_investment, percentage = \
        retirement_calculator(expected_salary,
                              current_salary,
                              inflation_rate,
                              salary_inflation_rate,
                              period,
                              starting_amount,
                              interest_rate)

    write_results(rf_inflated_salary_res_label, inflated_salary)
    write_results(rf_investment_res_label, retirement_investment)
    write_results(rf_percentage_res_label, percentage)

    draw_figure(retirement_graph_frame,
                period,
                {"Accumulated investment": accumulated_investments})


calculate_button(retirement_frame, 8, calculate_retirement_callback)

###########################################################################
###################### Percentage Tab ######################################
###########################################################################

percentage_frame = customtkinter.CTkFrame(master=tabview.tab("Percentage"))
percentage_frame.pack(pady=10, padx=10, fill="both", expand=True)

percentage_frame.grid_columnconfigure((1, 2), weight=1)
percentage_frame.grid_rowconfigure((1, 2, 3, 5, 6, 7, 8, 11), weight=0)
percentage_frame.grid_rowconfigure((0, 4, 9, 10), weight=1)

percentage_info = "This tab calculates the average interest that leads from the starting amount\n" \
                  "to the end amount in the given period of years."
define_info_frame(percentage_frame, percentage_info)

percentage_graph_frame = customtkinter.CTkFrame(master=percentage_frame)
percentage_graph_frame.grid(row=9, column=1, rowspan=2, columnspan=2)

###########################################################################
pf_starting_amount_entry = define_row(percentage_frame, "Starting amount", 100, 1)
pf_end_amount_entry = define_row(percentage_frame, "End amount", 1000, 2)
pf_period_entry = define_row(percentage_frame, "Period (in years)", 20, 3)

pf_principle_res_label = define_results_frame(percentage_frame, 4, ["Interest average rate"])[0]


def calculate_percentage_callback():
    starting_amount = get_entry_value(pf_starting_amount_entry, 100, float)
    end_amount = get_entry_value(pf_end_amount_entry, 1000, float)
    period = get_entry_value(pf_period_entry, 20, int)

    if starting_amount == IOError or \
            end_amount == IOError or \
            period == IOError:
        return

    inflation_rate, inflated_amounts = percentage_calculator(end_amount,
                                                             starting_amount,
                                                             period)

    write_results(pf_principle_res_label, inflation_rate)

    draw_figure(percentage_graph_frame,
                period,
                {"Inflated amount": inflated_amounts})


calculate_button(percentage_frame, 4, calculate_percentage_callback)

###########################################################################
###################### Loan Tab ###########################################
###########################################################################

loan_frame = customtkinter.CTkFrame(master=tabview.tab("Loan"))
loan_frame.pack(pady=10, padx=10, fill="both", expand=True)

loan_frame.grid_columnconfigure((1, 2), weight=1)
loan_frame.grid_rowconfigure((1, 2, 3, 5, 8, 11), weight=0)
loan_frame.grid_rowconfigure((0, 4, 6, 7, 9, 10), weight=1)

loan_info = "This tab calculates the monthly payment and the total payment of a loan."
define_info_frame(loan_frame, loan_info)

loan_graph_frame = customtkinter.CTkFrame(master=loan_frame)
loan_graph_frame.grid(row=9, column=1, rowspan=2, columnspan=2)

###########################################################################
lf_loan_amount_entry = define_row(loan_frame, "Loan amount", 100_000, 1)
lf_interest_rate_entry = define_row(loan_frame, "Interest rate (%)", 5, 2)
lf_period_entry = define_row(loan_frame, "Period (in years)", 30, 3)
lf_monthly_payment_entry = define_row(loan_frame, "Monthly payment", "", 5)

# Minimum Monthly Payment Results Frame
lf_min_monthly_payment_results_frame = customtkinter.CTkFrame(master=loan_frame)
lf_min_monthly_payment_results_frame.grid(row=4, column=2)
lf_min_monthly_payment_results_frame.grid_columnconfigure(1, weight=1)
lf_min_monthly_payment_results = customtkinter.CTkLabel(master=lf_min_monthly_payment_results_frame,
                                                        justify=tkinter.LEFT, text="\t")
lf_min_monthly_payment_results.grid(row=2, column=2)
#######################################

lf_total_amount_res_label = define_results_frame(loan_frame, 6, ["Original total"])[0]

lf_reduced_total_res_label, lf_reduced_period_res_label = define_results_frame(loan_frame, 7,
                                                                               ["Actual total", "Actual Period"])


def calculate_loan_monthly_payment_callback():
    loan_amount = get_entry_value(lf_loan_amount_entry, 100_000, float)
    interest_rate = get_entry_value(lf_interest_rate_entry, 5, float)
    period = get_entry_value(lf_period_entry, 30, int)

    if loan_amount == IOError or \
            interest_rate == IOError or \
            period == IOError:
        return

    total_amount, min_monthly_payment, _, _, _ = loan_calculator(loan_amount,
                                                                 interest_rate,
                                                                 period)
    rounded_payment = round(min_monthly_payment, 2)
    lf_min_monthly_payment_results.configure(text=f"  {rounded_payment}  ")
    lf_monthly_payment_entry.delete(0, 'end')
    lf_monthly_payment_entry.insert(0, f"{rounded_payment}")
    write_results(lf_total_amount_res_label, total_amount)


lf_get_monthly_payment_button = customtkinter.CTkButton(master=loan_frame,
                                                        command=calculate_loan_monthly_payment_callback,
                                                        text="Minimum monthly payment")
lf_get_monthly_payment_button.grid(row=4, column=1)


def calculate_loan_callback():
    loan_amount = get_entry_value(lf_loan_amount_entry, 100_000, float)
    interest_rate = get_entry_value(lf_interest_rate_entry, 5, float)
    monthly_payment = get_entry_value(lf_monthly_payment_entry,
                                      float(lf_min_monthly_payment_results.cget("text")),
                                      float)

    if loan_amount == IOError or \
            interest_rate == IOError or \
            monthly_payment == IOError:
        return

    red_amount, years, months, principles, interests, totals = higher_monthly_payment_calculator(loan_amount,
                                                                                                 interest_rate,
                                                                                                 monthly_payment)

    write_results(lf_reduced_total_res_label, red_amount)
    lf_reduced_period_res_label.configure(text=f"=  {years} years + {months} months  ")
    draw_figure(loan_graph_frame,
                len(principles) - 1,
                {"Principle": principles,
                 "Paid interest": interests,
                 "Total paid": totals},
                True)


calculate_button(loan_frame, 6, calculate_loan_callback)

app.mainloop()
