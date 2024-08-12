import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from functools import partial
from csv import writer
import requests
from API_test import *

root=tk.Tk()

root.geometry("800x600")

root.title("University of Dallas Gym Employee Software")

ud_seal = PhotoImage(file = r'C:\Users\Liam\Desktop\Coding Portfolio\CodingPortfolio\gym_check_in_software\UDallas_seal.png')

listbox_emp = None
listbox_dates = None

employee_api = 'https://api.restpoint.io/api/employee?'
header = 'x-endpoint-key=133bec7420fc43f38dc315e44a51264f'

root.iconphoto(False, ud_seal)

# declaring string variable
# for storing name and password
id_var=tk.StringVar()
passw_var=tk.StringVar()
new_id_var = tk.StringVar()
new_passwrd_var = tk.StringVar()
confirm_passwrd_var = tk.StringVar()
new_name_var = tk.StringVar()

checkout_to_do = [
     "At the beginning of your shift did you dry-mop the entire floor?", 
     "At the end of your shift did you dust the treadmills and ellipticals?",
     "At the end of your shift are all the weight plates back on their racks?",
     "At the end of your shift is the front desk area neat and clean?",
     "Morning shift: did you take the dumbbells off the racks and clean the racks?",
     "Mid-day shift: did you take the kettlebells off the racks and clean the racks?",
     "Afternoon shift: did you clean the treads of the treadmills?",
     "Night shift: did you dust the ellipticals, treadmills, and bicycles, and wipe and vacuum their foot pads?",
     "Late afternoon shift: did you wipe down all of the weight machines?",
     "Evening shift: did you mop the floor?",
     ]
# defining a function that will
# get the name and password and 
# print them on the screen
def submit(frame):

	name=id_var.get()
	password=passw_var.get()
	
	check_credentials(name, password,frame)
	
	id_var.set("")
	passw_var.set("")
	
def create_window(user_role, user, frame):
    for widget in frame.winfo_children():
          widget.destroy()
    
    if user_role == "admin":
        make_admin_page(frame)
    else:
        make_employee_page(frame, user)

def make_admin_page(frame):
     admin_label = tk.Label(frame, text="Administration Window", font=('calibre', 10, 'bold'))
     menubar = tk.Menu(frame, tearoff=0)
     filemenu = tk.Menu(menubar, tearoff=0)
     filemenu.add_command(label="Log Out", command=lambda:logout(frame))
     filemenu.add_separator()
     filemenu.add_command(label="Exit", command=root.quit)
     menubar.add_cascade(label="File", menu=filemenu)
     frame.config(menu=filemenu)
     add_employee_button = tk.Button(frame, text="Add Employee", command = lambda: add_employee(frame))
     remove_employee_button = tk.Button(frame, text="Remove Employee", command= lambda: remove_employee(frame))
     reset_employee_pass = tk.Button(frame, text="Reset Password", command= lambda: reset_passwords(frame))
     time_cards = tk.Button(frame, text="Access Time Cards", command= lambda: time_cards_page(frame))
     admin_label.pack(pady=10)
     add_employee_button.pack(pady=10)
     remove_employee_button.pack(pady=10)
     reset_employee_pass.pack(pady=10)
     time_cards.pack(pady=10)

def make_employee_page(frame, user):
        employee = get_employee_by_id(user)
        employee_name = employee['name']
        worker_label = tk.Label(frame, text="Employee Portal", font=('calibre', 10, 'bold'))
        menubar = tk.Menu(frame, tearoff=0)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Log Out", command=lambda: logout(frame))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        frame.config(menu=filemenu)
        welcome_label = tk.Label(frame, text=f"Welcome to the gym {employee_name}!")
        clock_in_button = tk.Button(frame, text="Clock-In", command = lambda: worker_clock_in(user))
        clock_out_button = tk.Button(frame, text="Clock-Out", command = lambda: worker_clock_out(frame, user))
        worker_label.pack(pady=10)
        welcome_label.pack(pady=10)
        clock_in_button.pack(pady=10)
        clock_out_button.pack(pady=10)

def check_credentials(user, passwrd,frame):
     employees = get_employees()
     for emp in employees:
          if emp['id'] == user and emp['password'] == passwrd:
               if emp['role'] == 'admin':
                    create_window('admin', emp, frame)
                    return
               else:
                    create_window('worker', emp['id'], frame)
                    return
          else:
               continue
     messagebox.showerror("Error", "Invalid Username or Password")

def worker_clock_in(user_id):
     employees = get_employees()
     for emp in employees:
          if emp['id'] == user_id:
               if emp['log_status'] == False:
                    update_employee_log(emp['id'], True)
                    dates = emp['dates_logged']
                    loaded_dates = json.loads(dates)
                    log_date = datetime.now().replace(microsecond=0)
                    log_date_str = log_date.isoformat()
                    loaded_dates[log_date_str] = -1
                    push_dates = json.dumps(loaded_dates)
                    update_employee_dates_logged(emp['id'], push_dates)
                    messagebox.showinfo("Success", "You have clocked in!")
               else:
                    messagebox.showerror("Error", "You are already clocked in!")

def worker_clock_out(frame, user_id):
     employees = get_employees()
     for emp in employees:
          if emp['id'] == user_id:
               if emp['log_status'] == True:
                    update_employee_log(emp['id'], False)
                    date_list = emp['dates_logged']
                    date_accessed = json.loads(date_list)
                    latest_date_str = date_accessed.popitem()
                    latest_date = latest_date_str[0]
                    latest_date_formatted = datetime.strptime(latest_date, "%Y-%m-%dT%H:%M:%S")
                    clock_out_date = datetime.now().replace(microsecond=0)
                    difference = clock_out_date - latest_date_formatted
                    difference_in_hours = "{:.2f}".format(difference.total_seconds() / 3600.0)
                    date_accessed[latest_date] = difference_in_hours
                    push_dates = json.dumps(date_accessed)
                    update_employee_dates_logged(emp['id'], push_dates)
                    messagebox.showinfo("Success", "You have clocked out!")
               else:
                    messagebox.showerror("Error", "You must clock in first!")

def worker_out_checklist(frame, current_time):
     for widget in frame.winfo_children():
          widget.destroy()

     check_out_label = tk.Label(frame, text="Check Out Checklist", font=('calibre', 10, 'bold'))
     dry_mop_q = tk.Label(frame, text="At the beginning of your shift did you dry-mop the entire floor?", font=('calibre', 10, 'bold'))
     dusting_q = tk.Label(frame, text="At the end of your shift did you dust the treadmills and ellipticals?", font=('calibre',10,'bold'))

     check_out_label.pack(pady=10)
     dry_mop_q.pack(pady=10)
     dusting_q.pack(pady=10)
          
def add_employee(frame):
     for widget in frame.winfo_children():
          widget.destroy()
     new_label = tk.Label(frame, text = "Add New Employee", font=('calibre',10,'bold'))
     menubar = tk.Menu(frame, tearoff=0)
     filemenu = tk.Menu(menubar, tearoff=0)
     filemenu.add_command(label="Return to Admin Home", command= lambda: return_to_admin(frame))
     filemenu.add_command(label="Log Out", command=lambda:logout(frame))
     filemenu.add_separator()
     filemenu.add_command(label="Exit", command=root.quit)
     menubar.add_cascade(label="File", menu=filemenu)
     frame.config(menu=filemenu)
     new_id = tk.Entry(frame, textvariable= new_id_var, font=('calibre',10,'normal'))
     new_id_label = tk.Label(frame, text = "Employee/Student ID", font=('calibre',10,'bold'))
     new_passwrd = tk.Entry(frame, textvariable= new_passwrd_var, font=('calibre',10, 'normal'), show = '*')
     new_passwrd_label = tk.Label(frame, text = "New Password", font=('calibre',10,'bold'))
     confirm_passwrd = tk.Entry(frame, textvariable=confirm_passwrd_var, font=('calibre',10,'normal'), show = '*')
     confirm_passwrd_label = tk.Label(frame, text = "Confirm Password", font=('calibre',10,'bold'))
     new_name = tk.Entry(frame, textvariable=new_name_var, font=('calibre',10))
     new_name_label = tk.Label(frame, text = "Employee/Student Name", font=('calbrie',10,'bold'))
     submit_new_employee = tk.Button(frame, text = "Submit", command = lambda: check_and_add())
     new_label.pack(pady=10)
     new_id_label.pack(pady=10)
     new_id.pack(pady=10)
     new_name_label.pack(pady=10)
     new_name.pack(pady=10)
     new_passwrd_label.pack(pady=10)
     new_passwrd.pack(pady=10)
     confirm_passwrd_label.pack(pady=10)
     confirm_passwrd.pack(pady=10)
     submit_new_employee.pack(pady=10)

def remove_employee(frame):
     for widget in frame.winfo_children():
          widget.destroy()
     remove_label = tk.Label(frame, text = "Remove Employee", font=('calibre',10,'bold'))
     menubar = tk.Menu(frame, tearoff=0)
     filemenu = tk.Menu(menubar, tearoff=0)
     filemenu.add_command(label="Return to Admin Home", command= lambda: return_to_admin(frame))
     filemenu.add_command(label="Log Out", command=lambda:logout(frame))
     filemenu.add_separator()
     filemenu.add_command(label="Exit", command=root.quit)
     menubar.add_cascade(label="File", menu=filemenu)
     frame.config(menu=filemenu)
     new_id = tk.Entry(frame, textvariable= new_id_var, font=('calibre',10,'normal'))
     new_id_label = tk.Label(frame, text = "Employee/Student ID", font=('calibre',10,'bold'))
     
     submit_new_employee = tk.Button(frame, text = "Submit", command= lambda: check_and_remove())
     remove_label.pack(pady=10)
     new_id_label.pack(pady=10)
     new_id.pack(pady=10)
     submit_new_employee.pack(pady=10)

def check_and_add():
     employees = get_employees() 
     new_id = new_id_var.get()
     new_pass = new_passwrd_var.get()
     confirm = confirm_passwrd_var.get()
     new_name = new_name_var.get()

     for emp in employees:
          if emp['id'] == new_id:
               messagebox.showerror("Error", "That ID is already in use")
          else:
               if new_pass == confirm:
                    enter_new_employee(new_id, new_name, new_pass)
               else:
                    messagebox.showerror("Error", "Passwords do not match")
     new_id_var.set("")
     new_passwrd_var.set("")
     confirm_passwrd_var.set("")

def check_and_remove():
     employees = get_employees()
     remove_id = new_id_var.get()

     for emp in employees:
          if emp['id'] == remove_id:
               delete_employee(remove_id)
     else:
          messagebox.showerror("Error", "That ID is not in use")
     new_id_var.set("")

def make_login_page(frame):
     for widget in frame.winfo_children():
          widget.destroy()
     # creating a label for name using widget Label
     id_label = tk.Label(root, text = 'Student ID', font=('calibre',10, 'bold'))

     # creating a entry for input name using widget Entry
     id_entry = tk.Entry(root,textvariable = id_var, font=('calibre',10,'normal'))

     # creating a label for password
     passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))

     # creating a entry for password
     passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')

     # creating a button using the widget Button that will call the submit function 
     sub_btn=tk.Button(root,text = 'Submit', command = lambda: submit(root))

     # placing the label and entry in the required position using grid method
     id_label.grid(row=0,column=0)
     id_entry.grid(row=0,column=1)
     passw_label.grid(row=1,column=0)
     passw_entry.grid(row=1,column=1)
     sub_btn.grid(row=2,column=1)

def logout(frame):
     make_login_page(frame)

def time_cards_page(frame):
     global listbox_emp
     employees = get_employees()
     for widget in frame.winfo_children():
          widget.destroy()
     time_card_label = tk.Label(frame, text="Time Cards", font=('calibre', 10, 'bold'))
     menubar = tk.Menu(frame, tearoff=0)
     filemenu = tk.Menu(menubar, tearoff=0)
     filemenu.add_command(label="Return to Admin Home", command= lambda: return_to_admin(frame))
     filemenu.add_command(label="Log Out", command=lambda:logout(frame))
     filemenu.add_separator()
     filemenu.add_command(label="Exit", command=root.quit)
     menubar.add_cascade(label="File", menu=filemenu)
     frame.config(menu=filemenu)
     time_card_label.pack()
     scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
     listbox_emp = tk.Listbox(frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
     scrollbar.config(command=listbox_emp.yview)
     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
     listbox_emp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

     for emp in employees:
          listbox_emp.insert(tk.END, emp['name'])
     
     listbox_emp.bind('<Double-Button-1>', access_employee_timecard)

def return_to_admin(frame):
     for widget in frame.winfo_children():
          widget.destroy()
     make_admin_page(frame)
     
def reset_passwords(frame):
     for widget in frame.winfo_children():
          widget.destroy()
     new_label = tk.Label(frame, text = "Reset Employee Password", font=('calibre',10,'bold'))
     menubar = tk.Menu(frame, tearoff=0)
     filemenu = tk.Menu(menubar, tearoff=0)
     filemenu.add_command(label="Return to Admin Home", command= lambda: return_to_admin(frame))
     filemenu.add_command(label="Log Out", command=lambda:logout(frame))
     filemenu.add_separator()
     filemenu.add_command(label="Exit", command=root.quit)
     menubar.add_cascade(label="File", menu=filemenu)
     frame.config(menu=filemenu)
     new_id = tk.Entry(frame, textvariable= id_var, font=('calibre',10,'normal'))
     new_id_label = tk.Label(frame, text = "Employee/Student ID", font=('calibre',10,'bold'))
     new_passwrd = tk.Entry(frame, textvariable= new_passwrd_var, font=('calibre',10, 'normal'), show = '*')
     new_passwrd_label = tk.Label(frame, text = "New Password", font=('calibre',10,'bold'))
     confirm_passwrd = tk.Entry(frame, textvariable=confirm_passwrd_var, font=('calibre',10,'normal'), show = '*')
     confirm_passwrd_label = tk.Label(frame, text = "Confirm Password", font=('calibre',10,'bold'))
     submit_new_employee = tk.Button(frame, text = "Submit", command = lambda: check_and_reset())
     new_label.pack(pady=10)
     new_id_label.pack(pady=10)
     new_id.pack(pady=10)
     new_passwrd_label.pack(pady=10)
     new_passwrd.pack(pady=10)
     confirm_passwrd_label.pack(pady=10)
     confirm_passwrd.pack(pady=10)
     submit_new_employee.pack(pady=10)
     
def check_and_reset():
     global user_map
     new_passwrd = new_passwrd_var.get()
     confirmed_passwrd = confirm_passwrd_var.get()
     exiting_id = id_var.get()
     employees = get_employees()

     if new_passwrd == confirmed_passwrd:
          for emp in employees:
               if emp['id'] == exiting_id:
                    update_employee_password(emp['id'], new_passwrd)
     else:
          tk.messagebox.showerror("Error", "Passwords do not match")
     
     new_passwrd_var.set("")
     confirm_passwrd_var.set("")
     id_var.set("")

def access_employee_timecard(event):
     global listbox_emp
     global listbox_dates
     employees = get_employees()
     selected_employee_index = listbox_emp.curselection()
     selected_employee = listbox_emp.get(selected_employee_index)

     for emp in employees:
          if emp['name'] == selected_employee:
               employee_dates = emp['dates_logged']
               employee_logged_dates = json.loads(employee_dates)
     employees = get_employees()
     top = Toplevel(root)
     top.geometry("400x300")
     top.iconphoto(False, ud_seal)
     top.title("Employee Timecard")
     label = tk.Label(top, text=f"{selected_employee}'s Clock-in Sheet")
     label.pack(pady=20)
     scrollbar = tk.Scrollbar(top, orient=tk.VERTICAL)
     listbox_dates = tk.Listbox(top, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
     scrollbar.config(command=listbox_dates.yview)
     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
     listbox_dates.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

     for date in employee_logged_dates:
          listbox_dates.insert(tk.END, date)
     
     listbox_dates.bind('<Double-Button-1>', partial(access_employee_date, listbox=listbox_dates, employee=selected_employee))
     listbox_dates.bind('<BackSpace>', partial(delete_employee_date, listbox = listbox_dates, employee=selected_employee))

def access_employee_date(event, listbox, employee):
     employees = get_employees()
     selected_date_index = listbox.curselection()
     if selected_date_index:
        selected_date = listbox.get(selected_date_index)
        for emp in employees:
          if emp['name'] == employee:
               date = emp['dates_logged']
               date_map = json.loads(date)
               hours = date_map[selected_date]
        messagebox.showinfo("Timecard Information", f"Employee: {employee}\nDate: {selected_date}\nHours on date: {hours}")

def delete_employee_date(event, listbox, employee):
     employees = get_employees()
     selected_date_index = listbox.curselection()
     if selected_date_index:
          selected_date = listbox.get(selected_date_index)
          for emp in employees:
               if emp['name'] == employee:
                    date = emp['dates_logged']
                    date_map = json.loads(date)
                    del date_map[selected_date]
                    updated_dates = json.dumps(date_map)
                    update_employee_dates_logged(emp['id'], updated_dates)
          messagebox.showinfo("Successful Removal", "Work Date and Hours Deleted")

make_login_page(root)
# performing an infinite loop for the window to display
root.mainloop()
