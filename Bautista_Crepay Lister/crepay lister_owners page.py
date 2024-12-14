import tkinter as tk
from tkinter import messagebox, PhotoImage
from email_service import send_email  # Assuming this function exists and is implemented properly
from database import register_worker, authenticate_worker, fetch_upcoming_reminders  # Import functions from the database module

# Function to handle worker login
def login_worker():
    """Login worker."""
    username = username_var.get().strip()
    password = password_var.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return

    # Authenticate worker (this is a simple example, ensure to hash the password in real-world use)
    worker = authenticate_worker(username, password)
    if worker:
        messagebox.showinfo("Login", "Login successful!")
        login_window.destroy()
        open_worker_window(worker)  # Open worker window after login with worker info
    else:
        messagebox.showerror("Login", "Invalid username or password.")

def open_worker_window(worker):
    def send_notification():
        """Send email notification about an upcoming payment reminder."""
        selected = reminder_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No reminder selected!")
            return
        
        # Get the selected reminder's details
        reminder = reminder_listbox.get(selected[0])
        name, email, account, amount, payment_date = reminder.split(" | ")

        # Send email to user about their upcoming payment
        try:
            subject = "Upcoming Payment Reminder"
            body = f"Dear {name},\n\nThis is a reminder for your upcoming payment.\n\nAccount: {account}\nAmount: {amount}\nPayment Date: {payment_date}"
            send_email(email, subject, body)  # Assuming send_email is correctly implemented
            messagebox.showinfo("Notification", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def refresh_reminders():
        """Refresh the list of upcoming reminders."""
        reminders = fetch_upcoming_reminders()  # Fetch all upcoming reminders
        reminder_listbox.delete(0, tk.END)
        if reminders:
            for reminder in reminders:
                # Each reminder is added to the listbox in the format: 'Name | Email | Account | Amount | Payment Date'
                reminder_listbox.insert(tk.END, f"{reminder['name']} | {reminder['email']} | {reminder['credit_account']} | {reminder['amount']} | {reminder['next_payment_date']}")
        else:
            messagebox.showinfo("No Reminders", "No upcoming payment reminders found.")

    # Create the worker window
    worker_window = tk.Tk()
    worker_window.title("Worker Panel")
    worker_window.geometry("800x600")
    worker_window.resizable(False, False)

    # Create a Canvas for the background image
    canvas = tk.Canvas(worker_window, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Load the Background Image
    try:
        worker_window.background_image = PhotoImage(file="\\Users\\shane\\Downloads\\money.png")  # Ensure correct path
        canvas.create_image(0, 0, anchor="nw", image=worker_window.background_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        canvas.config(bg="lightblue")  # Fallback background

    # Widgets for reminders
    tk.Label(worker_window, text="Upcoming Payment Reminders:", bg="white").place(x=50, y=50)

    # Listbox for displaying reminders
    reminder_listbox = tk.Listbox(worker_window, width=60, height=15)
    reminder_listbox.place(x=50, y=100, width=700, height=300)

    # Button to send notifications
    send_button = tk.Button(worker_window, text="Send Notification", command=send_notification)
    send_button.place(x=350, y=450)

    # Refresh reminders when the worker panel is opened
    refresh_reminders()

    # Start the main window loop
    worker_window.mainloop()

# Register Window for Worker
def open_register_window():
    def register():
        username = reg_username_var.get().strip()
        password = reg_password_var.get().strip()
        email = reg_email_var.get().strip()

        if not username or not password or not email:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        result = register_worker(username, password, email)
        messagebox.showinfo("Registration", result)
        if "successful" in result:
            register_window.destroy()

    """Open the registration window."""
    register_window = tk.Toplevel(login_window)
    register_window.title("Worker Registration")
    register_window.geometry("400x300")
    register_window.resizable(False, False)

    # Create a Canvas for the background image
    canvas = tk.Canvas(register_window, width=400, height=300)
    canvas.pack(fill="both", expand=True)

    # Load the Background Image
    try:
        register_window.background_image = PhotoImage(file="\\Users\\shane\\Downloads\\test.png")  # Adjust the path
        canvas.create_image(0, 0, anchor="nw", image=register_window.background_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        canvas.config(bg="lightgray")  # This will be used if image is not loaded

    # Directly place widgets on the canvas
    tk.Label(register_window, text="Register New Worker", font=("Helvetica", 14), bg="white").place(x=140, y=20)

    tk.Label(register_window, text="Username:", bg="white").place(x=50, y=70)
    reg_username_var = tk.StringVar()
    reg_username_entry = tk.Entry(register_window, textvariable=reg_username_var)
    reg_username_entry.place(x=150, y=70)

    tk.Label(register_window, text="Password:", bg="white").place(x=50, y=110)
    reg_password_var = tk.StringVar()
    reg_password_entry = tk.Entry(register_window, textvariable=reg_password_var, show="*")
    reg_password_entry.place(x=150, y=110)

    tk.Label(register_window, text="Email:", bg="white").place(x=50, y=150)
    reg_email_var = tk.StringVar()
    reg_email_entry = tk.Entry(register_window, textvariable=reg_email_var)
    reg_email_entry.place(x=150, y=150)

    tk.Button(register_window, text="Register", command=register).place(x=180, y=200)

# Login Window for Worker
def open_login_window():
    global username_var, password_var, login_window

    login_window = tk.Tk()
    login_window.title("Worker Login")
    login_window.geometry("800x600")
    login_window.resizable(False, False)

    try:
        # Load background image
        background_image = PhotoImage(file="\\Users\\shane\\Downloads\\money.png")  # Update with your image path
        login_window.iconphoto(False, PhotoImage(file="\\Users\\shane\\Downloads\\Crepay lister.png"))  # Update with your icon path
        canvas = tk.Canvas(login_window, width=400, height=300)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=background_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        login_window.destroy()
        return

    # Widgets for login
    tk.Label(login_window, text="Username:", font=('helvetica', 10, 'bold')).place(x=250, y=150)
    username_var = tk.StringVar()
    username_entry = tk.Entry(login_window, textvariable=username_var)
    username_entry.place(x=350, y=150)
    
    # Widgets
    title = tk.Label(login_window, text="Welcome To Crepay Lister for Admin", font='Arial 30 bold', bg="white")
    title.place(x=50, y=50)

    tk.Label(login_window, text="Password:", font=('helvetica', 10, 'bold')).place(x=250, y=200)
    password_var = tk.StringVar()
    password_entry = tk.Entry(login_window, textvariable=password_var, show="*")
    password_entry.place(x=350, y=200)

    tk.Button(login_window, text="Login", font=('helvetica', 10, 'bold'), command=login_worker).place(x=310, y=300)
    tk.Button(login_window, text="Register", font=('helvetica', 10, 'bold'), command=open_register_window).place(x=360, y=300)

    login_window.mainloop()

# Start the Login Window
open_login_window() 