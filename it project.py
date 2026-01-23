import datetime

# This list acts as our 'Database' to keep track of everyone
logs = []  # 'an empty notebook, keeps track of time when the student leaves and writes in the notebook'


def issue_pass():
    print("\n--- NEW BATHROOM PASS ENTRY ---")
    name = input("Student Name: ")
    reason = input("Reason for leaving: ")
    now = datetime.datetime.now()
    current_date = now.strftime("%m/%d/%Y")
    current_time = now.strftime("%I:%M %p")

    # 1. Add to the Tracking Chart
    entry = {
        "Name": name,
        "Time": current_time,
        "Date": current_date,
        "Reason": reason  # this is for the log to keep track of name time and reason
    }
    logs.append(entry)

    # 2. Generate the "Receipt" Style Pass
    print("\n" + "="*30)
    print("       HALL PASS       ")
    print("="*30)
    print(f"NAME:   {name}")
    print(f"TIME:   {current_time}")
    print(f"DATE:   {current_date}")
    print(f"REASON: {reason}")
    print("\nSIGNATURE: _________________")
    print("="*30)
    print("   Valid for 10 minutes   ")
    print("="*30 + "\n")
    # 'works by using string multiplication, SM is when the computer uses a shortcut to not have to retype out the
    # same thing over and over again. Works for the bathroom pass since it's the same pass that needs to be printed


def show_logs():
    print("\n--- DAILY LOG CHART ---")
    print(f"{'Name':<15} | {'Time':<10} | {'Date':<12} | {'Reason':<15}")
    print("-" * 45)
    for log in logs:
        print(f"{log['Name']:<12} | {log['Time']:<15} | {log['Date']:<10} | {log['Reason']:<15}")
        # the code here is to give it enough space for names without it looking messy and making it look neat

# Simple Menu Loop


while True:
    action = input("Type 'p' for New Pass, 'l' for Log, or 'q' to quit: ").lower()
    if action == 'p':
        issue_pass()
    elif action == 'l':
        show_logs()
    elif action == 'q':
        break
