Bathroom Pass System for CRLS

Created by:

Mustafa Paktiawal
Syed Hasan
Franco Mendoza
Kai Ademi
Bathroom Pass Printer (High School)

A Python-based bathroom pass system with a full-screen graphical interface designed for classroom use.
It allows teachers and students to quickly generate, track, and analyze bathroom passes.

We did use AI for our proejct as a tool, we only used chatgpt whenever we were stuck on a certain part of our project and couldn't figure out a way around it. We worked on the hardware parts and troubleshooting the code and testing it over and over again to make sure to work as well as go in to do any fixes that AI could've broke

What this program does
Select a class period
Choose or add a student name
Select a reason for leaving
Automatically records:
Date
Time Out
Time In
Prints a physical hall pass (Zebra printer supported)
Tracks:
Active students out of class
Pass history (logs)
Includes analytics dashboard (password protected):
Average time out
Median time
Most-used reasons
Student usage counts

Requirements (What you need)
1. Install Python

Make sure Python 3.9+ is installed.

2. Required Python Libraries

All required libraries are built into Python:

tkinter (GUI)
datetime
json
os
subprocess
tempfile
statistics

⚠️ SideNote:

On Windows/macOS, tkinter usually comes preinstalled
On Linux, you may need to install it manually:

This program is designed for a Zebra printer using ZPL (Zebra Programming Language).

You Must:
Make sure your printer is installed on your system
Ensure the printer name matches EXACTLY
On Mac/Linux: lpstat -p
On Windows: PRINTER_NAME = "Your_Printer_Name_Here"

File Setup (IMPORTANT)

When you first run the program, it will automatically create:

names.json → student names per period
logs.json → pass history
other_reasons.json → custom reasons
analytics.json → usage statistics

Make sure the program has permission to write files in its folder.

How to Run the Program
1. Download or clone this repository
2. Make sure the file is named something like: bathroom_pass.py
3. Open a terminal in the folder
4. Run: python bathroom_pass.py

How to Use
1. Select a period
2. Select or add a student
3. Choose a reason
4. The pass will:
  -Print automatically
  -Be logged in the system
5. When the student returns:
  -Click "Done" next to their name

Analytics Access:
Click the hidden "Franco" text at the bottom left
Enter password: Ilovethisclass123

You can easily customize the room number, background color, fonts and such on your own.
Enjoy!
