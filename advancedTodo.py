from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog
import time
from tkinter import ttk
window=Tk()
window.title("Advanced To-Do List")
window.config(bg="#F0F4F8")

# window.resizable(False, False)
window.grid_columnconfigure(0,weight=1)

current_time = time.strftime("%H:%M:%S %p")
current_date = time.strftime("%A, %d %B %Y")


tasks=[]
times=[]

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_reqwidth()) // 2
y = (screen_height - window.winfo_reqheight()) // 2
window.geometry(f"+{x}+{y}")  

frame=Frame(window)
frame.grid(row=2,column=0,columnspan=2)
task=Entry(frame,font="Arial 15", width=60, bg="lightyellow")
task.grid(row=1,column=0,padx=20)
task.insert(0, "You can only enter up to 40 characters")
task.config(fg="grey")

def on_focus_in(event):
    if task.get() == "You can only enter up to 40 characters":
        task.delete(0, END)
        task.config(fg="black")
def on_focus_out(event):
    if task.get() == "":
        task.insert(0,"You can only enter up to 40 characters")
        task.config(fg="grey")      

task.bind("<FocusIn>", on_focus_in)
task.bind("<FocusOut>", on_focus_out)



def generate_time_values():
    for hour in range(24):
        for minute in range(0, 60, 15):  # Example: increments of 15 minutes
            ampm = "AM" if hour < 12 else "PM"
            display_hour = hour % 24
            if display_hour == 0:
                display_hour = 0   # For 12 AM and 12 PM
            
            time_str = f"{display_hour:02d}:{minute:02d} {ampm}"
            times.append(time_str)
            
            
    return times   



time_var = StringVar(frame)
time_values = generate_time_values()
time_var.set(time_values[0])  # Set initial value
time_spinbox1 = Spinbox(frame,text="\n", textvariable=time_var, values=time_values,font="Arial 15")
time_spinbox1.grid(row=1,column=1,sticky="nw",pady=20)



    

def add_task():
    user_input = task.get()
    if user_input != "":
        tasks.append(user_input)
        number = len(tasks)   # next task number
        messagebox.showinfo("Task Added", "Your task has been added successfully!") 
        tasksLabel.insert(END, f"{number}. {user_input:<40}  Set At {time_spinbox1.get()} created on {current_date} {current_time}")  
        times.append(time_spinbox1.get())
        task.delete(0, END)
        
def save_file():
    # Open a file save dialog
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                     filetypes=(("Text files", "*.txt"),
                                                ("All files", "*.*")))
    if file: # Check if a file was selected (user didn't cancel)
        text_content = tasksLabel.get(0, END) 
        joined_text = "\n".join(text_content)
        file.write(joined_text)
        
        file.close()
        messagebox.showinfo("File Saved", "Your to-do list has been saved successfully!")
    else:
        messagebox.showwarning("Save Cancelled", "No file was selected. Save operation cancelled.")
         
def read_file():
    try:
        with open("data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                tasksLabel.insert(END, line.strip())
                tasks.append(line.strip())
    except FileNotFoundError:
        pass  # If the file doesn't exist, we simply start with an empty list        
        
       
    
    
    

def remove_task():
    selected_task_index = tasksLabel.curselection()
    if selected_task_index:
        index=selected_task_index[0]
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected task?"):
            tasksLabel.delete(index)
            number = len(tasks)  # Update task numbers
            for i, num in enumerate(range(1, number + 1), start=0):
                current_task = tasksLabel.get(i)
                if current_task:
                    task_text = current_task.split('. ', 1)[1]  # Get text after the number and dot
                    tasksLabel.delete(i)
                    tasksLabel.insert(i, f"{num}. {task_text}")
        else:
            return    
        tasks.pop(index)
     
def auto_save():
    with open("data.txt", "w") as file:
        text_content = tasksLabel.get(0, END)
        joined_text = "\n".join(text_content)
        file.write(joined_text)
    window.destroy()       
    
    
title_frame=Frame(window)
title_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")            
title=Label(title_frame,text="What's the next task then?😀",font="Arial 20 bold", bg="#34495E",anchor="center",fg="white")
title.place(relwidth=1,relheight=1)




button1=Button(frame,text="Add Task", font="Arial 15", fg="black", command=add_task)
button1.grid(row=1,column=2)
button2=Button(frame,text="Remove task", font="Arial 15", fg="black", command=remove_task)
button2.grid(row=1,column=3)
button3=Button(window,text="Save List", font="Arial 15", fg="black", command=save_file,state=DISABLED)
button3.grid(row=0,sticky="ne",padx=20,pady=10)

tasksLabel=Listbox(window,font="Consolas 15", bg="lightgrey",height=22)
tasksLabel.grid(row=3,column=0,sticky="new",padx=20)



scrollbar=Scrollbar(window,command=tasksLabel.yview,width=30)
scrollbar.grid(row=3,column=0,sticky="nse")
tasksLabel.config(yscrollcommand=scrollbar.set)

current_time_label = Label(title_frame, text=f"{current_date} \n{current_time}", font="Arial 20", bg="#2C3E50",fg="#ECF0F1")
current_time_label.grid(row=0, column=0,sticky="nw",padx=10) 



window_width = 1200
window_height = 680

# Get screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position
x = (screen_width // 2) - (window_width // 2) + 8
y = (screen_height // 2) - (window_height // 2) - 33

# Set geometry with size + position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

read_file()
window.protocol("WM_DELETE_WINDOW", auto_save)
window.mainloop() 