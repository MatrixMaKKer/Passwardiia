import tkinter as tk
from tkinter import messagebox, ttk
import random

# User data
users = {}
current_user = None
admin_login = "wojtaxmod"
admin_password = "wojtax2011"
active_users = []
notifications = []
messages = {}
notes = {}

# Initialize the main window
root = tk.Tk()
root.title("Passwardia")
root.attributes('-fullscreen', True)
root.configure(bg="black")

# Set default colors
background_color = "black"
particles_color = "green"
text_color = "green"

# Canvas for particles
canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
canvas.pack(fill="both", expand=True)

particles = []
for _ in range(100):
    particles.append({
        "char": random.choice(["$", "@", "#", "!", "%", "^", "&", "*", "(", ")"]),
        "x": random.randint(0, root.winfo_screenwidth()),
        "y": random.randint(-300, root.winfo_screenheight()),
        "speed": random.uniform(1, 3)
    })

notification_bell = None
note_counter = {}

# ---------- Functions ----------

def update_particles():
    canvas.delete("particles")
    for p in particles:
        p["y"] += p["speed"]
        if p["y"] > root.winfo_screenheight():
            p["y"] = random.randint(-300, 0)
            p["x"] = random.randint(0, root.winfo_screenwidth())
        canvas.create_text(p["x"], p["y"], text=p["char"], fill=particles_color, font=("Courier", 14), tags="particles")
    root.after(50, update_particles)

def go_to_main_menu(event=None):
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.pack(fill="both", expand=True)
    show_main_menu()

def show_main_menu():
    canvas.delete("all")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    canvas.create_text(w//2, h//4, text="Welcome to PASSWARDIA", fill=text_color, font=("Courier", 40, "bold"))
    tk.Button(root, text="LOGIN / REGISTER", font=("Courier", 18), bg=background_color, fg=text_color, command=show_auth_menu).place(x=w//2 - 150, y=h//2)
    tk.Button(root, text="CHANGE COLORS", font=("Courier", 18), bg=background_color, fg=text_color, command=change_colors).place(x=w//2 - 150, y=h//2 + 50)

def show_auth_menu():
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.delete("all")

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    canvas.create_text(w//2, 100, text="Login or Register", fill=text_color, font=("Courier", 24))

    login_var = tk.StringVar()
    pass_var = tk.StringVar()
    show_password = tk.BooleanVar()

    tk.Label(root, text="Username", fg=text_color, bg=background_color, font=("Courier", 14)).place(x=w//2 - 100, y=150)
    login_entry = tk.Entry(root, textvariable=login_var, font=("Courier", 14))
    login_entry.place(x=w//2, y=150)

    tk.Label(root, text="Password", fg=text_color, bg=background_color, font=("Courier", 14)).place(x=w//2 - 100, y=200)
    pass_entry = tk.Entry(root, textvariable=pass_var, show="*", font=("Courier", 14))
    pass_entry.place(x=w//2, y=200)

    def toggle_password():
        pass_entry.config(show="" if show_password.get() else "*")

    tk.Checkbutton(root, text="👁", variable=show_password, command=toggle_password, bg=background_color, fg=text_color, selectcolor=background_color).place(x=w//2 + 200, y=200)

    def login():
        user = login_var.get()
        pwd = pass_var.get()
        global current_user
        if user == admin_login and pwd == admin_password:
            current_user = user
            show_admin_dashboard()
        elif user in users and users[user] == pwd:
            current_user = user
            show_user_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect username or password")

    def register():
        user = login_var.get()
        pwd = pass_var.get()
        if user and pwd:
            users[user] = pwd
            messagebox.showinfo("Success", "User registered successfully")
        else:
            messagebox.showwarning("Error", "Enter a username and password")

    tk.Button(root, text="Login", command=login, font=("Courier", 12), bg=background_color, fg=text_color).place(x=w//2, y=250)
    tk.Button(root, text="Register", command=register, font=("Courier", 12), bg=background_color, fg=text_color).place(x=w//2 + 100, y=250)

def show_user_dashboard():
    global current_user
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.delete("all")
    canvas.pack(fill="both", expand=True)

    w = root.winfo_screenwidth()

    tk.Label(root, text=f"Welcome {current_user}", fg=text_color, bg=background_color, font=("Courier", 20)).place(x=50, y=20)

    if current_user not in messages:
        messages[current_user] = []

    chat_listbox = tk.Listbox(root, height=15, width=60, font=("Courier", 12), bg="black", fg="green")
    chat_listbox.place(x=50, y=70)
    for msg in messages[current_user]:
        chat_listbox.insert(tk.END, msg)

    recipient_var = tk.StringVar()
    message_var = tk.StringVar()

    tk.Label(root, text="To:", fg=text_color, bg=background_color, font=("Courier", 12)).place(x=50, y=370)
    recipient_menu = ttk.Combobox(root, textvariable=recipient_var, values=list(users.keys()) + ["ADMIN"], font=("Courier", 12))
    recipient_menu.place(x=100, y=370)

    tk.Label(root, text="Message:", fg=text_color, bg=background_color, font=("Courier", 12)).place(x=50, y=410)
    message_entry = tk.Entry(root, textvariable=message_var, font=("Courier", 12), width=40)
    message_entry.place(x=150, y=410)

    def send_message():
        recipient = recipient_var.get()
        msg = message_var.get()
        if recipient in users or recipient == "ADMIN":
            formatted_name = "ADMIN" if recipient == "ADMIN" else recipient
            display_name = f"To {formatted_name}: {msg}"
            messages.setdefault(current_user, []).append(display_name)
            chat_listbox.insert(tk.END, display_name)
            messages.setdefault(recipient, []).append(f"From {current_user}: {msg}")
        else:
            messagebox.showerror("Error", "User not found")

    def close_sms_window():
        # Close the SMS window only for admin and return to the admin panel
        if current_user == admin_login:
            show_admin_dashboard()
        else:
            show_user_dashboard()

    tk.Button(root, text="Send", command=send_message, font=("Courier", 12), bg=background_color, fg=text_color).place(x=100, y=450)
    tk.Button(root, text="Close", command=close_sms_window, font=("Courier", 12), bg=background_color, fg=text_color).place(x=200, y=450)

    tk.Button(root, text="Logout", command=go_to_main_menu, font=("Courier", 12), bg=background_color, fg=text_color).place(x=50, y=520)

def show_admin_dashboard():
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.pack(fill="both", expand=True)
    canvas.delete("all")

    w = root.winfo_screenwidth()

    tk.Label(root, text="Welcome Admin", fg=text_color, bg=background_color, font=("Courier", 20)).place(x=50, y=20)

    tk.Button(root, text="Show Users", font=("Courier", 12), bg=background_color, fg=text_color, command=show_users_admin).place(x=50, y=80)
    tk.Button(root, text="Reset Users", font=("Courier", 12), bg=background_color, fg=text_color, command=reset_users).place(x=50, y=120)
    tk.Button(root, text="Logout", command=go_to_main_menu, font=("Courier", 12), bg=background_color, fg=text_color).place(x=50, y=160)

    tk.Button(root, text="View Messages", command=show_messages_admin, font=("Courier", 12), bg=background_color, fg=text_color).place(x=50, y=200)

def show_users_admin():
    # Create a new window for admin to view logins and passwords
    user_window = tk.Toplevel(root)
    user_window.title("User List - Logins and Passwords")
    user_window.geometry("600x400")
    user_window.configure(bg=background_color)

    login_list = "\n".join(users.keys())
    pass_list = "\n".join(users.values())

    tk.Label(user_window, text="LOGINS:", fg="green", bg=background_color, font=("Courier", 14)).pack(pady=10)
    tk.Label(user_window, text=login_list, fg="green", bg=background_color, font=("Courier", 12)).pack(pady=10)
    tk.Label(user_window, text="PASSWORDS:", fg="green", bg=background_color, font=("Courier", 14)).pack(pady=10)
    tk.Label(user_window, text=pass_list, fg="green", bg=background_color, font=("Courier", 12)).pack(pady=10)

    tk.Button(user_window, text="Close", command=user_window.destroy, font=("Courier", 12), bg=background_color, fg=text_color).pack(pady=20)

def show_messages_admin():
    global current_user
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    canvas.delete("all")
    canvas.pack(fill="both", expand=True)

    w = root.winfo_screenwidth()

    tk.Label(root, text=f"Admin Messages", fg=text_color, bg=background_color, font=("Courier", 20)).place(x=50, y=20)

    chat_listbox = tk.Listbox(root, height=15, width=60, font=("Courier", 12), bg="black", fg="green")
    chat_listbox.place(x=50, y=70)
    for msg in messages.get("ADMIN", []):
        chat_listbox.insert(tk.END, msg)

    recipient_var = tk.StringVar()
    message_var = tk.StringVar()

    tk.Label(root, text="To:", fg=text_color, bg=background_color, font=("Courier", 12)).place(x=50, y=370)
    recipient_menu = ttk.Combobox(root, textvariable=recipient_var, values=list(users.keys()) + ["ADMIN"], font=("Courier", 12))
    recipient_menu.place(x=100, y=370)

    tk.Label(root, text="Message:", fg=text_color, bg=background_color, font=("Courier", 12)).place(x=50, y=410)
    message_entry = tk.Entry(root, textvariable=message_var, font=("Courier", 12), width=40)
    message_entry.place(x=150, y=410)

    def send_message():
        recipient = recipient_var.get()
        msg = message_var.get()
        if recipient in users or recipient == "ADMIN":
            formatted_name = "ADMIN" if recipient == "ADMIN" else recipient
            display_name = f"To {formatted_name}: {msg}"
            messages.setdefault("ADMIN", []).append(display_name)
            chat_listbox.insert(tk.END, display_name)
            messages.setdefault(recipient, []).append(f"From ADMIN: {msg}")
        else:
            messagebox.showerror("Error", "User not found")

    tk.Button(root, text="Send", command=send_message, font=("Courier", 12), bg=background_color, fg=text_color).place(x=100, y=450)
    tk.Button(root, text="Close", command=go_to_main_menu, font=("Courier", 12), bg=background_color, fg=text_color).place(x=200, y=450)

def reset_users():
    to_delete = [u for u in users if u != admin_login]
    for user in to_delete:
        del users[user]
    messagebox.showinfo("Reset", "All users (except admin) have been removed.")

def show_notifications(event=None):
    if notifications:
        messagebox.showinfo("Notifications", "\n".join(notifications))
    else:
        messagebox.showinfo("No Notifications", "No new notifications.")

def change_colors():
    global background_color, particles_color, text_color
    colors_window = tk.Toplevel(root)
    colors_window.title("Change Colors")

    def update_colors():
        global background_color, particles_color, text_color
        background_color = bg_color_var.get()
        particles_color = pt_color_var.get()
        text_color = text_color_var.get()
        colors_window.destroy()
        go_to_main_menu()

    color_list = ["black", "red", "green", "blue", "yellow", "pink", "purple", "orange", "brown", "gray", "white"]

    bg_color_var = tk.StringVar(value=background_color)
    pt_color_var = tk.StringVar(value=particles_color)
    text_color_var = tk.StringVar(value=text_color)

    tk.Label(colors_window, text="Background Color", font=("Courier", 12)).pack(pady=5)
    bg_menu = ttk.Combobox(colors_window, textvariable=bg_color_var, values=color_list, font=("Courier", 12))
    bg_menu.pack(pady=5)

    tk.Label(colors_window, text="Particles Color", font=("Courier", 12)).pack(pady=5)
    pt_menu = ttk.Combobox(colors_window, textvariable=pt_color_var, values=color_list, font=("Courier", 12))
    pt_menu.pack(pady=5)

    tk.Label(colors_window, text="Text Color", font=("Courier", 12)).pack(pady=5)
    text_menu = ttk.Combobox(colors_window, textvariable=text_color_var, values=color_list, font=("Courier", 12))
    text_menu.pack(pady=5)

    tk.Button(colors_window, text="Update Colors", command=update_colors, font=("Courier", 12), bg=background_color, fg=text_color).pack(pady=20)

update_particles()  # Start the particle update loop
show_main_menu()  # Display main menu
root.mainloop()
