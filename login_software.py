# Program to make a simple 
# login screen 


import tkinter as tk

root=tk.Tk()

# setting the windows size
root.geometry("800x600")

# declaring string variable
# for storing name and password
id_var=tk.StringVar()
passw_var=tk.StringVar()


# defining a function that will
# get the name and password and 
# print them on the screen
def submit():

	name=id_var.get()
	password=passw_var.get()
	
	checkAdmin(name, password)
	
	id_var.set("")
	passw_var.set("")
	
def checkAdmin(user, passwrd):
	if user == "admin" and passwrd == "admin":
		create_window()
	else:
		print("Welcome Worker")
		
def create_window():
	tk.Toplevel(root)
	
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
