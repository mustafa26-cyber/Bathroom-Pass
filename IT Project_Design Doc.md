  
**Concept:**   
**We are thinking of making a feature where you input your name and reason for a hall pass and it prints it, then you give the printed pass to Dr. Wu to sign, it will already have the date and time from the code we install on it. We need a receipt printer and possibly a touch screen that allows students to input their name and reason and press a button to print.**

**We also want to make a feature like a log that keeps track of who signs out and when. This can be on a device like a touch screen or computer that lets the teacher see the log. Students should also be able to see the log so they know when it’s their turn to leave.** 

We need:

- Receipt Printer  
- Python code to print and keep track  
- A device (preferably touch screen with buttons that will keep track of the log)  
- Connect printer to a computer that has the code  
- Make a website for the UI

Question:  
Should we write the code in VS code or there is a feature in Github to make a code?  
How to make branches in code?  
What’s better to use VS code or Github?

Franco \+ hasan: python code troubleshooting  
Mustafa: github  
Kai: finding receipt and touch screen that you can program the code into

[https://shop.m5stack.com/products/atom-thermal-printer-kit?variant=42135643095297\&country=US\&currency=USD\&utm\_](https://shop.m5stack.com/products/atom-thermal-printer-kit?variant=42135643095297&country=US&currency=USD&utm_) 

[https://www.alibaba.com/product-detail/NETUM-80mm-Usb-thermal-Receipt-Printer\_1601382458059.html?mark=google\_shopping\&seo=1\&utm\_](https://www.alibaba.com/product-detail/NETUM-80mm-Usb-thermal-Receipt-Printer_1601382458059.html?mark=google_shopping&seo=1&utm_) 

can use a microcontroller such as a raspberry pi in order to send commands to the printer

demonstration vids:

[https://www.youtube.com/watch?v=LwKOvT7rCiU](https://www.youtube.com/watch?v=LwKOvT7rCiU)

[https://www.youtube.com/watch?v=xg45b8UXoZI](https://www.youtube.com/watch?v=xg45b8UXoZI)   
^^

This is an excellent project. You are moving from a simple script to a **full-stack IoT (Internet of Things) solution**.

To answer your specific questions before the Design Doc:

* **VS Code vs. GitHub:** You write code in **VS Code** (the "Editor"). **GitHub** is the "Library" where you store and protect that code. You will write the code in VS Code on your computer and "Push" it to GitHub to save it.  
* **How to make branches:** In VS Code, click the branch icon (bottom left) or type git checkout \-b feature-name in the terminal. This allows Franco and Hasan to work on code without breaking Mustafa’s GitHub setup.

---

# **Technical Design Specification: The "SmartPass" System**

## **I. Executive Summary & Problem Scope**

* **The Problem:** Traditional paper hall passes are slow to write, easy to lose, and difficult for teachers to track over time. There is no "live" queue, leading to students constantly asking, "Can I go yet?"  
* **The Solution:** A kiosk-based system where students input their data via a touchscreen. The system instantly prints a physical "receipt" pass for the teacher to sign and updates a digital live-log (web dashboard) for both teachers and students to monitor.  
* **Target User:** High school teachers (like Dr. Wu) who need organized records, and students who need a transparent waiting line.

## **II. Technical Requirements**

* **Functional Requirements:**  
  * The system must capture Name, Reason, Date, and Time.  
  * The system must trigger a physical print command to a thermal printer.  
  * The system must display a "Live Log" table on a web interface.  
* **Non-Functional Requirements:**  
  * **Reliability:** The log must save data to a file/database so it isn't lost if the power goes out.  
  * **Usability:** The touchscreen buttons must be large enough for quick interaction.

## **III. System Architecture & Logic**

### **Logic Flowchart**

Code snippet

```
graph TD
    A[Student enters Name/Reason] --> B[Presses 'Print Pass' Button]
    B --> C[Python Script saves data to Log]
    C --> D[Command sent to Thermal Printer]
    D --> E[Receipt Prints for Signature]
    C --> F[Web Dashboard updates in real-time]
```

### **System Diagram**

* **Frontend:** HTML/JavaScript Website (The UI students see).  
* **Backend:** Python (Flask or FastAPI) running on a Raspberry Pi or Laptop.  
* **Hardware:** USB Thermal Receipt Printer \+ Touchscreen Monitor.

## **IV. Data Schema & Tech Stack**

* **Tech Stack:** \* **Python:** Used for the logic and printer communication (escpos library).  
  * **Flask:** To create the website that shows the log.  
  * **GitHub:** For version control and team collaboration.  
  * **Raspberry Pi (Optional):** To act as the small "brain" hidden behind the screen.  
* Data Model:  
  Entries are stored as a JSON object or CSV row:  
  { "id": 101, "name": "Student Name", "date": "01/22/26", "time": "10:30AM", "reason": "Bathroom", "status": "Active" }

## **V. Open Questions & Potential Problems**

### **1\. Open Questions**

* **Printer Drivers:** Will the Alibaba/NETUM printer work natively with Python libraries, or do we need specific Windows/Linux drivers?  
* **Web Access:** How do we make the "Live Log" accessible to students on their own phones? (Local Wi-Fi hosting vs. Cloud).  
* **Power:** Does the M5Stack printer kit provide enough power to the microcontroller, or do we need two separate plugs?

### **2\. Risk Assessment & Mitigation Table**

| Potential Problem | Impact | Mitigation Plan |
| :---- | :---- | :---- |
| **Paper Jam/Out of Paper** | Medium | Add a "Printer Status" check in the code to alert the teacher. |
| **Duplicate Entries** | Low | Disable the "Print" button for 5 seconds after it is pressed once. |
| **Database Corruption** | High | Use a simple CSV file as a backup that saves every time a pass is issued. |

---

## **AI Appendix**

* **Prompt Log:**  
  * "Create a professional technical design document for a Python hall pass system using thermal printers."  
  * "Explain the difference between VS Code and GitHub for a high school project."  
* **The Vetting Statement:**  
  * I used AI to structure the risk assessment table to ensure I didn't miss "Scope Creep." I kept the Python logic simple (using CSV/JSON) because a full SQL database would be too complex for our 4-person team's timeline.

---

### **Your Next Steps:**

1. **Mustafa:** Create the GitHub Repository and invite Franco, Hasan, and Kai.  
2. **Kai:** Finalize the choice between the **M5Stack** (easier for small DIY) and the **NETUM** (more professional/sturdier).  
3. **Franco & Hasan:** Start testing the "Save to File" logic in your Python code so the data doesn't disappear.

