import tkinter as tk # I import tkinter so it makes a graphic window
import datetime #  Makes a set date and time

# Data Storage
logs = [] # This list works as a log that keeps track of every bathroom pass that gets printed

# Functions
def issue_pass(): # This function runs when someone presses the button to print a bathroom pass.
    name = name_entry.get() # The program gets text directly from the GUI text boxes instead of using input()
    reason = reason_entry.get()

    if name == "" or reason == "": # This prevents blank passes from being printed and wasting paper.
        output_label.config(text="Please fill in all fields!")
        return

    now = datetime.datetime.now() # The program puts automated times so it cant be a fake date or time.
    current_date = now.strftime("%m/%d/%Y")
    current_time = now.strftime("%I:%M %p")

    entry = { # Each pass is saved as a dictionary, making it easier to keep track of.
        "Name": name,
        "Time": current_time,
        "Date": current_date,
        "Reason": reason
    }
    logs.append(entry)

    pass_text = ( # This makes the format of the pass look like a real printed receipt.
        "==============================\n"
        "        HALL PASS\n"
        "==============================\n"
        f"NAME:   {name}\n"
        f"TIME:   {current_time}\n"
        f"DATE:   {current_date}\n"
        f"REASON: {reason}\n\n"
        "SIGNATURE: _______________\n"
        "==============================\n"
        "Valid for 10 minutes\n"
    )

    output_label.config(text=pass_text) # The pass appears in a window.

    name_entry.delete(0, tk.END)
    reason_entry.delete(0, tk.END)

# GUI Setup
window = tk.Tk() # This is the title and structure of the window and text.
window.title("Bathroom Pass Printer")
window.geometry("600x500")

title = tk.Label(window, text="Bathroom Pass Printer", font=("Comic Sans MS", 24))
title.pack(pady=10)

tk.Label(window, text="Student Name:").pack() # Makes boxes for name and reason,this lets the user input their name and reason.
name_entry = tk.Entry(window, width=40)
name_entry.pack()

tk.Label(window, text="Reason:").pack()
reason_entry = tk.Entry(window, width=40)
reason_entry.pack()

print_button = tk.Button(window, text="Print Pass", command=issue_pass) # Function runs once this button is clicked.
print_button.pack(pady=10)

output_label = tk.Label(window, text="", font=("Courier", 12), justify="left") # Shows that the bathroom printed pass was completed.
output_label.pack(pady=10)

window.mainloop() # Lets the program run and wait for actions from the user.
