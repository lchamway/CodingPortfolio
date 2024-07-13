import tkinter as tk
from tkinter import messagebox
import datetime as dt
import csv

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



# defining a function that will
# get the name and password and 
# print them on the screen
def submit():

	name=id_var.get()
	password=passw_var.get()
	
	check_credentials(name, password)
	
	id_var.set("")
	passw_var.set("")
	
		
def create_window(user_role):
    new_window = tk.Toplevel(root)
    new_window.geometry("400x300")
    new_window.title("Main Window")
    
    if user_role == "admin":
        admin_label = tk.Label(new_window, text="Admin", font=('calibre', 10, 'bold'))
        admin_label.pack(pady=10)
    else:
        worker_label = tk.Label(new_window, text="Employee Portal", font=('calibre', 10, 'bold'))
        clock_in_button = tk.Button(new_window, text="Clock-In", command = worker_clock_in)
        clock_out_button = tk.Button(new_window, text="Clock-Out")
        worker_label.pack(pady=10)
        clock_in_button.pack(pady=10)
        clock_out_button.pack(pady=10)
	
def check_credentials(user, passwrd):
    if user in user_map and user_map[user] == passwrd:
        user_role = "admin" if user == "admin" else "worker"
        create_window(user_role)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def worker_clock_in():
     ...
# creating a label for 
# name using widget Label
id_label = tk.Label(root, text = 'Student ID', font=('calibre',10, 'bold'))

# creating a entry for input
# name using widget Entry
id_entry = tk.Entry(root,textvariable = id_var, font=('calibre',10,'normal'))

# creating a label for password
passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))

# creating a entry for password
passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')

# creating a button using the widget 
# Button that will call the submit function 
sub_btn=tk.Button(root,text = 'Submit', command = submit)

# placing the label and entry in
# the required position using grid
# method
id_label.grid(row=0,column=0)
id_entry.grid(row=0,column=1)
passw_label.grid(row=1,column=0)
passw_entry.grid(row=1,column=1)
sub_btn.grid(row=2,column=1)

# performing an infinite loop 
# for the window to display
root.mainloop()
