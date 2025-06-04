import tkinter as tk
from turtle import color
import weakref
import customtkinter as ctk
from tkinter import messagebox
from registration import Registration
from user import User
from profile_window import ProfileWindow


ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.0)

class RegistrationWindow(ctk.CTkFrame):
    def __init__(self, master, registered):
        super().__init__(master)
        self.configure(fg_color="#E6E4E4", corner_radius=0)
        self.mode = "login"  # or 'register'
        self.font_family = "Inter"
        self.title_font_size = 24
        self.entry_font_size = 14
        self.button_font_size = 16
        self.registered = registered
        
        self.create_header()
        self.create_main_frame()
        self.create_footer_buttons()

    def show(self):
        self.lift()
        self.pack(side="right", expand=True, fill="both")

    def hide(self):
        self.pack_forget()

    def create_header(self):
        if self.registered == 0:
            header_width = 1000
        else:
            header_width = 800
        header_frame = ctk.CTkFrame(self, width=header_width, height=50, fg_color="#58C75C", corner_radius=0)
        header_frame.place(x=0, y=0)

        self.header_label = ctk.CTkLabel(
            master=header_frame,
            text="Registration",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        self.header_label.place(relx=0.5, rely=0.5, anchor="center")

    def create_main_frame(self): 
        self.main_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15, fg_color="white")
        self.main_frame.place(relx=0.5, rely=0.45, anchor="center")
        self.main_frame.pack_propagate(False)

        self.form_title = ctk.CTkLabel(
            self.main_frame, 
            text="Login", 
            font=(self.font_family, self.title_font_size, "bold"), 
            text_color="#333333"
        )
        self.form_title.pack(pady=(20, 10))

        self.email_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Email", 
            width=300, height=40,
            font=(self.font_family, self.entry_font_size)
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Password", 
            width=300, height=40, show="*",
            font=(self.font_family, self.entry_font_size)
        )
        self.password_entry.pack(pady=10)

        self.confirm_password_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Confirm Password", 
            width=300, height=40, show="*",
            font=(self.font_family, self.entry_font_size),
            
        )
        # Спочатку приховуємо confirm_password_entry для режиму Login

        self.confirm_button = ctk.CTkButton(
            self.main_frame, 
            text="Confirm", 
            width=300, 
            command=self.on_confirm,
            font=(self.font_family, self.button_font_size)
        )
        self.confirm_button.pack(pady=(20, 10))
    
    def on_confirm(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get() if self.mode == "register" else None

        if not email or not password or (self.mode == "register" and not confirm_password):
            messagebox.showwarning("⚠️ Warning", "Please fill in all fields.")
            return

        if self.mode == "register" and password != confirm_password:
            messagebox.showerror("❌ Error", "Passwords do not match.")
            return
        
        if self.mode == "login":
            reg = Registration()
            new_user = reg.login_user(email, password) 
            if new_user:
                messagebox.showinfo("✅ Success", "Login successful.")
            else:
                messagebox.showerror("❌ Error", "Incorrect email or password.")
            
        elif self.mode == "register":
            reg = Registration()

            new_user = User(
                name="None",
                email=email,
                password=password,
                sex="None",
                birth_date="2000-11-11",
                weight=40,
                height=100,
                goal="None",
                activity_factor=1.22,
                avatar_image="None",
                bjv_mode="None"
            )
            self.place_forget()
            self.master.sidebar.pack_forget()  

            
            self.profile_window = ProfileWindow(self.master, new_user, 0)
            self.profile_window.place(x=0, y=0, relwidth=1, relheight=1)
        
            


    def create_footer_buttons(self):
        self.registration_button = ctk.CTkButton(
            self, 
            text="Registration",
            fg_color="#58C75C", 
            command=self.toggle_mode, 
            height=40,
            font=(self.font_family, self.button_font_size)
        )
        self.registration_button.place(relx=0.5, rely=0.8, anchor="center")

        self.exit_button = ctk.CTkButton(
            self, 
            text="Exit", 
            fg_color="#9F9F9F", 
            hover_color="#cc0000", 
            command=self.quit_app, 
            height=40,
            width=100,
            font=(self.font_family, self.button_font_size)
        )
        self.exit_button.place(relx=0.5, rely=0.91, anchor="center")

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.form_title.configure(text="Registration")
            self.header_label.configure(text="Login")  # верхня панель при реєстрації -> 'Login'
            self.registration_button.configure(text="Back to Login")
            self.confirm_password_entry.pack(pady=10, before=self.confirm_button)
        else:
            self.mode = "login"
            self.form_title.configure(text="Login")
            self.header_label.configure(text="Registration")  # верхня панель при вході -> 'Registration'
            self.registration_button.configure(text="Registration")
            self.confirm_password_entry.pack_forget()

    def quit_app(self):
        self.master.destroy()
        
    def take_new_data(self, user):
        self.windows = {
                "Profile": ProfileWindow(self, user, 0)
            }


        self.current_window = "Profile"
        self.windows["Profile"].place(x=0, y=0, relwidth=1, relheight=1)
        self.windows["Profile"].show()
        new_user = {}
        return new_user