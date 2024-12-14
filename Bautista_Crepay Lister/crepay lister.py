import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkcalendar import DateEntry  # Import the DateEntry widget from tkcalendar
from database import register_user, login_user, add_payment_reminder, fetch_reminders
from email_service import send_email  # Assuming this is your email module

# Function to Open the Registration Window
def open_register_window():
    def register():
        username = reg_username_entry.get().strip()
        password = reg_password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty!")
            return
        result = register_user(username, password)
        messagebox.showinfo("Registration", result)
        if "successful" in result:
            register_window.destroy()

    register_window = tk.Toplevel(login_window)
    register_window.title("Register")
    register_window.geometry("500x355")
    register_window.resizable(False, False)  # Disable resizing

    # Create a Canvas for the background image
    canvas = tk.Canvas(register_window, width=400, height=300)
    canvas.pack(fill="both", expand=True)

    # Load the Background Image
    register_window.background_image = PhotoImage(file="\\Users\\shane\\Downloads\\test.png")  # Adjust the path
    canvas.create_image(0, 0, anchor="nw", image=register_window.background_image)

    # Widgets
    tk.Label(register_window, font=('helvetica', 10, 'bold'), text="Username:", bg="white").place(x=50, y=150)
    reg_username_entry = tk.Entry(register_window)
    reg_username_entry.place(x=150, y=150, width=200)

    tk.Label(register_window, font=('helvetica', 10, 'bold'), text="Password:", bg="white").place(x=50, y=200)
    reg_password_entry = tk.Entry(register_window, show="*")
    reg_password_entry.place(x=150, y=200, width=200)
    
    title = tk.Label(register_window, text="Welcome To Crepay Lister", font='helvetica 20 bold', bg="#03fca5")
    title.place(x=70, y=50)
    
    tk.Button(register_window, font=('helvetica', 10, 'bold'), text="Register", command=register).place(x=170, y=250, width=150)

# Login Function
def login():
    username = username_var.get().strip()
    password = password_var.get().strip()
    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return
    user = login_user(username, password)
    if user:
        messagebox.showinfo("Login", "Login successful!")
        login_window.destroy()
        main_panel(user["id"])  # Pass the user ID to the main panel
    else:
        messagebox.showerror("Login", "Invalid username or password.")

# Main Panel
def main_panel(user_id):
    def add_reminder():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        account = account_entry.get().strip()
        amount = amount_entry.get().strip()
        payment_date = payment_date_entry.get()  # Fetch date from DateEntry widget
        if not all([name, email, account,amount , payment_date]):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        result = add_payment_reminder(user_id, name, email, account,amount , payment_date)
        messagebox.showinfo("Reminder", result)
        
        # Send email notification after adding reminder
        try:
            subject = "Payment Reminder Added"
            body = f"Reminder Details:\nName: {name}\nEmail: {email}\nAccount: {account}\nAmount: {amount}\nPayment Date: {payment_date}"
            send_email(email, subject, body)  # Assuming send_email is working as intended
            messagebox.showinfo("Email", "Reminder email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

        refresh_reminders()

    def refresh_reminders():
        reminders = fetch_reminders(user_id)
        reminder_listbox.delete(0, tk.END)
        for reminder in reminders:
            reminder_listbox.insert(tk.END, f"{reminder[0]} | {reminder[1]} | {reminder[2]} | {reminder[3]} | {reminder[4]}")
   
    # Create Main Window
    main_window = tk.Tk()
    main_window.title("Crepay Lister")
    main_window.geometry("900x700")
    main_window.resizable(False, False)  # Disable resizing

    # Create a Canvas for the background image
    canvas = tk.Canvas(main_window, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Load the Background Image
    main_window.background_image = PhotoImage(file="\\Users\\shane\\Downloads\\crepay.png")  # Adjust the path
    canvas.create_image(0, 0, anchor="nw", image=main_window.background_image)

    # Widgets for reminder
    tk.Label(main_window, text="Name:",font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=50)
    name_entry = tk.Entry(main_window)
    name_entry.place(x=350, y=50, width=200)

    tk.Label(main_window, text="Email:",font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=100)
    email_entry = tk.Entry(main_window)
    email_entry.place(x=350, y=100, width=200)

    tk.Label(main_window, text="Credit Account:",font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=150)
    account_entry = tk.Entry(main_window)
    account_entry.place(x=350, y=150, width=200)
    
    tk.Label(main_window, text="Amount:",font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=200)
    amount_entry = tk.Entry(main_window)
    amount_entry.place(x=350, y=200, width=200)

    tk.Label(main_window, text="Payment Date:",font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=250)
    payment_date_entry = DateEntry(main_window, date_pattern="yyyy-MM-dd", width=18)  # Use DateEntry widget
    payment_date_entry.place(x=400, y=250, width=150)

    tk.Button(main_window, text="Add Reminder",font=('helvetica', 10, 'bold'), command=add_reminder).place(x=350, y=300, width=120)

    reminder_listbox = tk.Listbox(main_window, width=50)
    reminder_listbox.place(x=100, y=400, width=700, height=200)

    refresh_reminders()

    # Start the main window loop
    main_window.mainloop()

# Login Window
login_window = tk.Tk()
login_window.title("Crepay Lister")
login_window.geometry("846x600")    
login_window.resizable(False, False)  # Disable resizing

# Load Images
try:
    icon = PhotoImage(file="\\Users\\shane\\Downloads\\Crepay lister.png")  # Ensure correct path
    login_window.background_image = PhotoImage(file="\\Users\\shane\\Downloads\\money.png")  # Ensure correct path
except Exception as e:
    messagebox.showerror("Error", f"Failed to load images: {e}")
    exit()

# Create a Canvas for the background image
canvas = tk.Canvas(login_window, width=800, height=600)
canvas.pack(fill="both", expand=True)  # Make canvas expand to fill the window

# Background Image for Login Window
canvas.create_image(0, 0, anchor="nw", image=login_window.background_image)

# Keep a reference to the image
canvas.image = login_window.background_image

# Icon
login_window.iconphoto(True, icon)

# Widgets
title = tk.Label(login_window, text="Welcome To Crepay Lister", font='Arial 30 bold', bg="white")
title.place(x=150, y=50)

username_var = tk.StringVar()
tk.Label(login_window, text="Username:", font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=150)
username_entry = tk.Entry(login_window, textvariable=username_var)
username_entry.place(x=300, y=150, width=200)

password_var = tk.StringVar()
tk.Label(login_window, text="Password:", font=('helvetica', 10, 'bold'), bg="white").place(x=200, y=200)
password_entry = tk.Entry(login_window, textvariable=password_var, show="*")
password_entry.place(x=300, y=200, width=200)

tk.Button(login_window, text="Login", font=('helvetica', 10, 'bold'), command=login).place(x=300, y=250, width=100)
tk.Button(login_window, text="Register", font=('helvetica', 10, 'bold'), command=open_register_window).place(x=400, y=250, width=100)

login_window.mainloop() 