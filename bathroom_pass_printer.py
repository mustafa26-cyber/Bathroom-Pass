import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import json
import os
import subprocess
import tempfile


# ---------------- CONFIG ----------------
PRINTER_NAME = "ZTC-ZD421"
ROOM_NUMBER = "1311B"


BG_COLOR = "#f4f6f9"
PRIMARY_BLUE = "#1f4ed8"


NAMES_FILE = "names.json"
LOG_FILE = "logs.json"
OTHER_REASONS_FILE = "other_reasons.json"


window = tk.Tk()
window.title("Bathroom Pass System")
window.attributes("-fullscreen", True)
window.configure(bg=BG_COLOR)


selected_student = None
selected_period = None


logs = []
active_passes = {}


# ---------------- FILE FUNCTIONS ----------------
def load_names(period):
   if not os.path.exists(NAMES_FILE):
       return []
   with open(NAMES_FILE, "r") as f:
       data = json.load(f)
   return data.get(period, [])


def save_name(period, name):
   data = {}
   if os.path.exists(NAMES_FILE):
       with open(NAMES_FILE, "r") as f:
           data = json.load(f)
   data.setdefault(period, []).append(name)
   with open(NAMES_FILE, "w") as f:
       json.dump(data, f)


def delete_name(period, student):
   data = {}
   if os.path.exists(NAMES_FILE):
       with open(NAMES_FILE, "r") as f:
           data = json.load(f)
   if period in data and student in data[period]:
       data[period].remove(student)
   with open(NAMES_FILE, "w") as f:
       json.dump(data, f)
   student_screen(period)


def load_logs():
   global logs
   if os.path.exists(LOG_FILE):
       with open(LOG_FILE, "r") as f:
           logs = json.load(f)


def save_logs():
   with open(LOG_FILE, "w") as f:
       json.dump(logs, f)


def load_other_reasons():
   if not os.path.exists(OTHER_REASONS_FILE):
       return []
   with open(OTHER_REASONS_FILE, "r") as f:
       return json.load(f)


def save_other_reason(reason):
   reasons = load_other_reasons()
   if reason not in reasons:
       reasons.append(reason)
       with open(OTHER_REASONS_FILE, "w") as f:
           json.dump(reasons, f)


# ---------------- PRINTER ----------------
def send_zpl(zpl):
   try:
       with tempfile.NamedTemporaryFile(delete=False, suffix=".zpl") as temp:
           temp.write(zpl.encode("utf-8"))
           temp.flush()
           temp_path = temp.name
       subprocess.run(
           ["lp", "-d", PRINTER_NAME, "-o", "raw", temp_path],
           check=True
       )
       os.remove(temp_path)
   except Exception as e:
       messagebox.showerror("Printer Error", f"Printing failed:\n{e}")


def print_to_printer(student, reason, date, time):
   zpl = f"""
^XA
^PW406
^LL203
^CF0,30
^FO120,20^FDHall Pass^FS
^CF0,22
^FO10,60^FDName: {student}^FS
^FO10,90^FDReason: {reason}^FS
^FO10,120^FDDate: {date}^FS
^FO210,120^FDTime: {time}^FS
^FO10,150^FDRoom: {ROOM_NUMBER}^FS
^CF0,20
^FO120,180^FDTeacher Signature:^FS
^FO300,190^GB120,2,2^FS
^XZ
"""
   send_zpl(zpl)


# ---------------- AUTO TIME CHECK ----------------
def check_overdue_passes():
   now = datetime.datetime.now()
   for student in list(active_passes.keys()):
       start_time = active_passes[student]
       diff = (now - start_time).total_seconds() / 60
       if diff >= 10:
           for entry in reversed(logs):
               if entry["Name"] == student and entry["Time In"] == "":
                   entry["Time In"] = "OVERDUE"
                   break
           del active_passes[student]
   save_logs()
   window.after(60000, check_overdue_passes)


# ---------------- UI HELPERS ----------------
def clear_window():
   for widget in window.winfo_children():
       widget.destroy()


def add_back_button(command):
   tk.Button(
       window,
       text="⬅ Back",
       font=("Segoe UI",18),
       command=command
   ).pack(anchor="nw", padx=20, pady=20)


# ---------------- PERIOD SCREEN ----------------
def period_screen():
   clear_window()


   screen_width = window.winfo_screenwidth()


   main_frame = tk.Frame(window, bg=BG_COLOR)
   main_frame.pack(fill="both", expand=True)


   left_frame = tk.Frame(main_frame, bg=BG_COLOR, width=int(screen_width*0.75))
   left_frame.pack(side="left", fill="both", expand=True)
   left_frame.pack_propagate(False)


   line_frame = tk.Frame(main_frame, bg="gray", width=2)
   line_frame.pack(side="left", fill="y")


   right_frame = tk.Frame(main_frame, bg=BG_COLOR, width=int(screen_width*0.25))
   right_frame.pack(side="left", fill="both", expand=True)
   right_frame.pack_propagate(False)


   tk.Label(
       left_frame,
       text="Select Period",
       font=("Segoe UI",48,"bold"),
       bg=BG_COLOR
   ).pack(pady=40)


   def select_period(p):
       global selected_period
       selected_period = p
       student_screen(p)


   periods = [
       "Period 1",
       "Period 2",
       "Period 3",
       "Period 4",
       "Falcon Block / Other"
   ]


   for p in periods:
       tk.Button(
           left_frame,
           text=p,
           font=("Segoe UI",26,"bold"),
           width=22,
           height=3,
           bg="white",
           bd=0,
           relief="flat",
           highlightthickness=2,
           highlightbackground="#d0d0d0",
           command=lambda period=p: select_period(period)
       ).pack(pady=12)


   tk.Label(
       right_frame,
       text="Students Out",
       font=("Segoe UI",32,"bold"),
       bg=BG_COLOR
   ).pack(pady=20)


   if not active_passes:
       tk.Label(
           right_frame,
           text="No students currently out",
           font=("Segoe UI",18),
           bg=BG_COLOR
       ).pack()
   else:
       for student in active_passes:


           box = tk.Frame(
               right_frame,
               bg="white",
               highlightbackground="#cfcfcf",
               highlightthickness=2,
               padx=10,
               pady=10
           )
           box.pack(pady=10, padx=10, fill="x")


           time_out = active_passes[student].strftime("%I:%M %p")


           tk.Label(
               box,
               text=f"{student} - {time_out}",
               font=("Segoe UI",20),
               bg="white"
           ).pack(side="left")


           tk.Button(
               box,
               text="Done",
               font=("Segoe UI",18),
               bg="#16a34a",
               fg="white",
               bd=0,
               padx=20,
               pady=8,
               command=lambda s=student: mark_back_home(s)
           ).pack(side="right")


   view_log_button = tk.Button(
       right_frame,
       text="View Log",
       font=("Segoe UI",22),
       bg=PRIMARY_BLUE,
       fg="white",
       padx=30,
       pady=10,
       bd=0,
       command=view_logs
   )
   view_log_button.pack(side="bottom", pady=20)


def open_student_screen(period):
   global selected_period
   selected_period = period
   student_screen(period)


# ---------------- STUDENT SCREEN ----------------
def student_screen(period):


   clear_window()
   add_back_button(period_screen)


   tk.Label(
       window,
       text=f"{period} - Room {ROOM_NUMBER}",
       font=("Segoe UI",32,"bold"),
       bg=BG_COLOR
   ).pack(pady=10)


   container = tk.Frame(window)
   container.pack(fill="both", expand=True)


   canvas = tk.Canvas(container, bg=BG_COLOR)


   v_scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
   h_scroll = tk.Scrollbar(window, orient="horizontal", command=canvas.xview)


   scroll_frame = tk.Frame(canvas, bg=BG_COLOR)


   scroll_frame.bind(
       "<Configure>",
       lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
   )


   canvas.create_window((0,0), window=scroll_frame, anchor="nw")


   canvas.configure(
       yscrollcommand=v_scroll.set,
       xscrollcommand=h_scroll.set
   )


   canvas.pack(side="left", fill="both", expand=True)
   v_scroll.pack(side="right", fill="y")
   h_scroll.pack(side="bottom", fill="x")


   student_names = load_names(period)
   student_names.sort()


   max_rows = 6


   for i, student in enumerate(student_names):


       row = i % max_rows
       column = i // max_rows


       box = tk.Frame(scroll_frame, bg=BG_COLOR)
       box.grid(row=row, column=column, padx=30, pady=30)


       tk.Button(
           box,
           text=student,
           font=("Segoe UI",20),
           width=16,
           height=2,
           command=lambda s=student: select_student(s)
       ).pack()


       tk.Button(
           box,
           text="❌",
           font=("Segoe UI",14),
           fg="red",
           bd=0,
           command=lambda s=student: delete_name(period,s)
       ).place(relx=1,rely=0,anchor="ne")


   entry_frame = tk.Frame(window, bg=BG_COLOR)
   entry_frame.pack(pady=20)


   name_entry = tk.Entry(entry_frame,font=("Segoe UI",20),width=20)
   name_entry.pack(side="left",padx=20)


   def add_name():


       global selected_student


       name = name_entry.get().strip()


       if not name:
           return


       name = name.title()


       save_name(period,name)


       selected_student = name


       reason_screen()


   tk.Button(
       entry_frame,
       text="Add Name",
       font=("Segoe UI",20),
       command=add_name
   ).pack(side="left")


   name_entry.bind("<Return>", lambda event: add_name())


# ---------------- SELECT STUDENT ----------------
def select_student(student):
   global selected_student
   selected_student = student
   reason_screen()


# ---------------- REASON SCREEN ----------------
def reason_screen():


   clear_window()
   add_back_button(lambda: student_screen(selected_period))


   tk.Label(
       window,
       text=f"{selected_student} - Select Reason",
       font=("Segoe UI",34,"bold"),
       bg=BG_COLOR
   ).pack(pady=60)


   for reason in ["Bathroom","Water","Other"]:


       tk.Button(
           window,
           text=reason,
           font=("Segoe UI",24),
           width=18,
           height=2,
           command=lambda r=reason: handle_reason(r)
       ).pack(pady=20)


# ---------------- HANDLE OTHER REASON ----------------
def handle_reason(reason):


   if reason != "Other":
       finalize_pass(reason)
   else:
       show_other_reason_dropdown()


def show_other_reason_dropdown():


   clear_window()


   add_back_button(lambda: reason_screen())


   tk.Label(
       window,
       text=f"{selected_student} - Select or Add Reason",
       font=("Segoe UI",28,"bold"),
       bg=BG_COLOR
   ).pack(pady=30)


   reasons = load_other_reasons()


   if not reasons:
       reasons = ["Other"]


   selected = tk.StringVar(value=reasons[0])


   dropdown = ttk.Combobox(
       window,
       textvariable=selected,
       state="readonly",
       values=reasons,
       font=("Segoe UI",20)
   )


   dropdown.pack(pady=20)


   entry = tk.Entry(window,font=("Segoe UI",20))
   entry.pack(pady=20)


   def confirm_other():


       r = entry.get().strip()


       if r:
           save_other_reason(r)
           finalize_pass(r)
       else:
           finalize_pass(selected.get())


   tk.Button(
       window,
       text="Confirm",
       font=("Segoe UI",22),
       bg=PRIMARY_BLUE,
       fg="white",
       command=confirm_other
   ).pack(pady=20)


# ---------------- PRINT ----------------
def finalize_pass(reason):


   now=datetime.datetime.now()
   date=now.strftime("%m/%d/%Y")
   time=now.strftime("%I:%M %p")


   print_to_printer(selected_student,reason,date,time)


   logs.append({
       "Name":selected_student,
       "Date":date,
       "Time Out":time,
       "Time In":"",
       "Reason":reason
   })


   active_passes[selected_student]=datetime.datetime.now()


   save_logs()


   clear_window()


   tk.Label(
       window,
       text="Your pass is being printed,\nmake sure you get it signed!\nMake sure you sign back in",
       font=("Segoe UI",28,"bold"),
       bg=BG_COLOR,
       fg="red"
   ).pack(expand=True)


   window.after(5000,period_screen)


# ---------------- SIGN BACK IN ----------------
def mark_back_home(student):


   now=datetime.datetime.now().strftime("%I:%M %p")


   for entry in reversed(logs):
       if entry["Name"]==student and entry["Time In"]=="":
           entry["Time In"]=now
           break


   save_logs()


   if student in active_passes:
       del active_passes[student]


   period_screen()


# ---------------- LOGS ----------------
def view_logs():


   win=tk.Toplevel(window)
   win.title("Logs")
   win.geometry("900x600")


   cols=("Name","Date","Time Out","Time In","Reason")


   tree=ttk.Treeview(win,columns=cols,show="headings")


   for c in cols:
       tree.heading(c,text=c)
       tree.column(c,width=150)


   tree.pack(fill="both",expand=True)


   for entry in logs:


       tag=""


       if entry["Time In"]=="OVERDUE":
           tag="overdue"


       tree.insert(
           "",
           "end",
           values=(
               entry["Name"],
               entry["Date"],
               entry["Time Out"],
               entry["Time In"],
               entry["Reason"]
           ),
           tags=(tag,)
       )


   tree.tag_configure("overdue",foreground="red")


# ---------------- START ----------------
load_logs()
period_screen()
check_overdue_passes()
window.mainloop()





