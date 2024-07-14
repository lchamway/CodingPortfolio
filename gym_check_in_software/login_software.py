import tkinter as tk
from tkinter import messagebox
import datetime
from csv import writer

root=tk.Tk()

root.geometry("800x600")

# declaring string variable
# for storing name and password
id_var=tk.StringVar()
passw_var=tk.StringVar()

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
     ]
# defining a function that will
# get the name and password and 
# print them on the screen
def submit():

	name=id_var.get()
	password=passw_var.get()
	
	check_credentials(name, password)
	
	id_var.set("")
	passw_var.set("")
	
def create_window(user_role, user):
    new_window = tk.Toplevel(root)
    new_window.geometry("400x300")
    new_window.title("Main Window")
    
    if user_role == "admin":
        admin_label = tk.Label(new_window, text="Admin", font=('calibre', 10, 'bold'))
        admin_label.pack(pady=10)
    else:
        worker_label = tk.Label(new_window, text="Employee Portal", font=('calibre', 10, 'bold'))
        clock_in_button = tk.Button(new_window, text="Clock-In", command = lambda: worker_clock_in(user))
        clock_out_button = tk.Button(new_window, text="Clock-Out", command = lambda: worker_clock_out(user))
        worker_label.pack(pady=10)
        clock_in_button.pack(pady=10)
        clock_out_button.pack(pady=10)
	
def check_credentials(user, passwrd):
    if user in user_map and user_map[user] == passwrd:
        user_role = "admin" if user == "admin" else "worker"
        create_window(user_role, user)
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

def worker_clock_out(user_id):
     if worker_clock_status[user_id]:
         current_time = datetime.datetime.now()
         info_list = [user_id, False, None, datetime.datetime.now()]
         with open(r'C:\Users\Liam\Desktop\Coding Portfolio\CodingPortfolio\gym_check_in_software\worker_log.csv', 'a', newline='') as file:
             writer_object = writer(file)
             writer_object.writerow(info_list)
             file.close()
         worker_clock_status[user_id] = False
         worker_out_checklist(current_time)
     else:
          messagebox.showerror("Error", "You are already clocked out")

def worker_out_checklist(current_time):
     check_out_window = tk.Toplevel(root)
     check_out_window.geometry("400x300")
     check_out_window.title("Check Out Checklist")

     check_out_label = tk.Label(check_out_window, text="Check Out Checklist", font=('calibre', 10, 'bold'))
     dry_mop_q = tk.Label(check_out_window, text="At the beginning of your shift did you dry-mop the entire floor?", font=('calibre', 10, 'bold'))
     dusting_q = tk.Label(check_out_window, text="At the end of your shift did you dust the treadmills and ellipticals?", font=('calibre',10,'bold'))

     check_out_label.pack(pady=10)
     dry_mop_q.pack(pady=10)
     dusting_q.pack(pady=10)
          
# creating a label for name using widget Label
id_label = tk.Label(root, text = 'Student ID', font=('calibre',10, 'bold'))

# creating a entry for input name using widget Entry
id_entry = tk.Entry(root,textvariable = id_var, font=('calibre',10,'normal'))

# creating a label for password
passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))

# creating a entry for password
passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')

# creating a button using the widget Button that will call the submit function 
sub_btn=tk.Button(root,text = 'Submit', command = submit)

# placing the label and entry in the required position using grid method
id_label.grid(row=0,column=0)
id_entry.grid(row=0,column=1)
passw_label.grid(row=1,column=0)
passw_entry.grid(row=1,column=1)
sub_btn.grid(row=2,column=1)

# performing an infinite loop for the window to display
root.mainloop()
