import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from tkinter import *
from tkinter.ttk import *
import datetime
from csv import writer

root=tk.Tk()

root.geometry("800x600")

root.title("University of Dallas Gym Employee Software")

ud_seal = PhotoImage(file = r'C:\Users\Liam\Desktop\Coding Portfolio\CodingPortfolio\gym_check_in_software\UDallas_seal.png')

root.iconphoto(False, ud_seal)

# declaring string variable
# for storing name and password
id_var=tk.StringVar()
passw_var=tk.StringVar()
new_id_var = tk.StringVar()
new_passwrd_var = tk.StringVar()
confirm_passwrd_var = tk.StringVar()

user_map = {
	"admin":"admin",
	"900897702":"loser",
	"900":"winner",

}

worker_clock_status = {
    "900897702": False,
    "900": False,
}

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
        worker_label = tk.Label(frame, text="Employee Portal", font=('calibre', 10, 'bold'))
        menubar = tk.Menu(frame, tearoff=0)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Log Out", command=lambda: logout(frame))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        frame.config(menu=filemenu)
        clock_in_button = tk.Button(frame, text="Clock-In", command = lambda: worker_clock_in(user))
        clock_out_button = tk.Button(frame, text="Clock-Out", command = lambda: worker_clock_out(frame, user))
        worker_label.pack(pady=10)
        clock_in_button.pack(pady=10)
        clock_out_button.pack(pady=10)

def check_credentials(user, passwrd,frame):
    if user in user_map and user_map[user] == passwrd:
        user_role = "admin" if user == "admin" else "worker"
        create_window(user_role, user,frame)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def worker_clock_in(user_id):
     if not worker_clock_status[user_id]:
         current_time = datetime.datetime.now()
         info_list = [user_id, True, datetime.datetime.now(), None]
         with open(r'C:\Users\Liam\Desktop\Coding Portfolio\CodingPortfolio\gym_check_in_software\worker_log.csv', 'a', newline ='') as file:
             writer_object = writer(file)
             writer_object.writerow(info_list)
             file.close()
         worker_clock_status[user_id] = True
     else:
          messagebox.showerror("Error", "You are already clocked in")

def worker_clock_out(frame, user_id):
     if worker_clock_status[user_id]:
         current_time = datetime.datetime.now()
         info_list = [user_id, False, None, datetime.datetime.now()]
         with open(r'C:\Users\Liam\Desktop\Coding Portfolio\CodingPortfolio\gym_check_in_software\worker_log.csv', 'a', newline='') as file:
             writer_object = writer(file)
             writer_object.writerow(info_list)
             file.close()
         worker_clock_status[user_id] = False
         worker_out_checklist(frame, current_time)
     else:
          messagebox.showerror("Error", "You are already clocked out")

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
     submit_new_employee = tk.Button(frame, text = "Submit", command = lambda: check_and_add())
     new_label.pack(pady=10)
     new_id_label.pack(pady=10)
     new_id.pack(pady=10)
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
     global user_map
     global worker_clock_map
     
     new_id = new_id_var.get()
     new_pass = new_passwrd_var.get()
     confirm = confirm_passwrd_var.get()
     if new_id not in user_map:
          if new_pass == confirm:
               user_map[new_id] = new_pass
          else:
               messagebox.showerror("Error", "Passwords do not match")
     else:
          messagebox.showerror("Error", "That ID is already in use")
     new_id_var.set("")
     new_passwrd_var.set("")
     confirm_passwrd_var.set("")

def check_and_remove():
     global user_map
     global worker_clock_map

     remove_id = new_id_var.get()

     if remove_id in user_map:
          del user_map[remove_id]
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

     if new_passwrd == confirmed_passwrd:
          if exiting_id in user_map:
               user_map[exiting_id] = new_passwrd
     else:
          tk.messagebox.showerror("Error", "Passwords do not match")
     
     new_passwrd_var.set("")
     confirm_passwrd_var.set("")
     id_var.set("")


make_login_page(root)
# performing an infinite loop for the window to display
root.mainloop()
