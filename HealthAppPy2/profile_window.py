import tkinter as tk
from tkinter import ttk
from turtle import width
from xml.dom.domreg import registered
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw 
import tkinter.messagebox as messagebox
from tkinter import filedialog
import os
import sys
from DB_control import DBControl
import io
import sqlite3
import json

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.0)

# -------------------- User Profile Window --------------------
class ProfileWindow(ctk.CTkFrame):
    def __init__(self, master, user, registered): 
        super().__init__(master)
        self.user = user
        self.configure(fg_color="#E6E4E4", corner_radius=0)
        self.registered = registered
        self.statistic_frame = ctk.CTkFrame(self.master, width=800, height=600, fg_color="#E6E4E4")
        if self.registered == 0:
            max_width = 1000
        else:
            max_width = 800
        self.change_frame = ctk.CTkFrame(self.master, width=max_width, height=600, fg_color="#E6E4E4")
        
        self.create_statistic_ui()
        self.create_change_ui()
        self.create_activity_ui()
        if registered == 0:
            self.show_change()
        else:
            self.show_statistic()
        
    def show_statistic(self):
        self.change_frame.place_forget()
        self.statistic_frame.place(x=0, y=0) 

    def show_change(self):
        self.statistic_frame.place_forget()
        self.change_frame.place(x=0, y=0)
        
    def show_change2(self):
        self.activity_frame.place_forget()
        self.change_frame.place(x=0, y=0)
        
    def show_choose(self):
        self.change_frame.place_forget()
        self.activity_frame.place(x=0, y=0)
        
    def set_avatar_image(self, ax, ay, master): 
        if self.user.avatar_image:
            try:
                image = Image.open(io.BytesIO(self.user.avatar_image))
            except:
                image = Image.open("icons/profile.png")
        else:
            image = Image.open("icons/profile.png")

        # Зміна розміру
        size = (166, 166)
        image = image.resize(size)

        # Створюємо маску — біле коло на чорному фоні
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Применяем маску до альфа-каналу (для прозорості)
        image.putalpha(mask)

        # Створюємо CTkImage з альфа-каналом
        ctk_image = ctk.CTkImage(light_image=image, size=size)

        # Виводимо лейбл з аватаром
        self.avatar_label = ctk.CTkLabel(master=master, image=ctk_image, text="")
        self.avatar_label.image = ctk_image
        self.avatar_label.place(x=ax, y=ay)
    
    def create_statistic_ui(self):
        

        self.statistic_frame = ctk.CTkFrame(self , width=800, height=600, fg_color="#E6E4E4") 
        self.sex_button_map = {}
        self.goal_button_map = {}
        # Header
        header_frame = ctk.CTkFrame(self.statistic_frame, width=800, height=50, fg_color="#58C75C", corner_radius=0)
        header_frame.place(x=0, y=0)

        header_label = ctk.CTkLabel(
            master=header_frame,
            text=f"Welcome {self.user.name}!",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        header_label.place(x=143 + (700 - 143) // 2, rely=0.5, anchor="center")

         # --------- ПЕРШИЙ Content Frame (Recorded + BMI) ---------
        content_frame_1 = ctk.CTkFrame(self.statistic_frame, width=770, height=63 * 1.33, fg_color="#FFFFFF", corner_radius=7)
        content_frame_1.place(x=15, y=57)

        ctk.CTkLabel(
            master=content_frame_1,
            text="Recorded:",
            text_color="black",
            font=("Inter", 16)
        ).place(x=10, y=10)
        
        ctk.CTkLabel(
            master=content_frame_1,
            text="0 day(s)",
            text_color="black",
            font=("Inter", 16, "bold")
        ).place(x=100, y=10)
        
        ctk.CTkLabel(
            master=content_frame_1,
            text="BMI:",
            text_color="black",
            font=("Inter", 16)
        ).place(x=210, y=10)
        
        # Розрахунок BMI
        weight = self.user.weight
        height_cm = self.user.height
        bmi = weight / ((height_cm / 100) ** 2)

        # Виведення BMI з точністю до 1 знака після коми
        ctk.CTkLabel(
            master=content_frame_1,
            text=f"{bmi:.1f}",
            text_color="black",
            font=("Inter", 16, "bold")
        ).place(x=260, y=10)  

        # --------- ДРУГИЙ Content Frame (User Info) ---------
        content_frame_2 = ctk.CTkFrame(self.statistic_frame, width=500, height=350, fg_color="#FFFFFF", corner_radius=7)
        content_frame_2.place(x=15, y=150)

        info_font_normal = ("Inter", 16)
        info_font_bold = ("Inter", 16, "bold")

        user_info_labels = ["Email:", "Birth date:", "Weight:", "Height:", "Sex:", "Goal:", "Activity:"]
        if self.user.sex == "F":
            user_sex_text = "Female"
        else: 
            user_sex_text = "Male"
            
        if self.user.goal == "L":
            user_goal_text = "Lose"
        elif self.user.goal == "G":
            user_goal_text = "Gain"
        else:
            user_goal_text = "Maintain"
            
        if self.user.activity_factor == 1.2:
            activity_text = "Low"
        elif self.user.activity_factor == 1.375:
            activity_text = "Under medium"
        elif self.user.activity_factor == 1.55:
            activity_text = "Medium"
        elif self.user.activity_factor == 1.725:
            activity_text = "Above medium"
        elif self.user.activity_factor == 1.9:
            activity_text = "High"
        user_info_values = [self.user.email, self.user.birth_date, self.user.weight, self.user.height, user_sex_text, user_goal_text, activity_text]

        for idx, (label, value) in enumerate(zip(user_info_labels, user_info_values)):
            ctk.CTkLabel(
                master=content_frame_2,
                text=label,
                text_color="black",
                font=info_font_normal
            ).place(x=10, y=int(10 + idx * 48))

            ctk.CTkLabel(
                master=content_frame_2,
                text=value,
                text_color="black",
                font=info_font_bold
            ).place(x=130, y=int(10 + idx * 48))  # зсунув праві значення трохи правіше

        # --------- АВАТАР ---------
        
        ax=565
        ay=152
        self.set_avatar_image(ax, ay, self.statistic_frame)

        
        # --------- КНОПКА "Change" ---------
        change_button = ctk.CTkButton(
            master=self.statistic_frame,
            width=int(146 * 1.364),
            height=int(44 * 1.33),
            corner_radius=7,
            fg_color="#58C75C",
            hover_color="#7F7F7F",
            text="Change",
            text_color="white",
            font=("Inter", 18, "bold"),
            command=self.show_change
        )
        change_button.place(x=550, y=350)

        # --------- КНОПКА Log out ---------
        logout_image = ctk.CTkImage(
            light_image=Image.open(r"icons\logout.png"),  
            size=(19, 19)
        )

        logout_button = ctk.CTkButton(
            master=self.statistic_frame,
            width=int(150),
            height=int(45),
            corner_radius=7,
            fg_color="#9F9F9F",
            hover_color="#8F8F8F",
            text="Log out",
            image=logout_image,
            compound="left",
            text_color="black",
            font=("Inter", 16),
            command=self.logout_user
        )
        logout_button.place(x=15, y=520)
    
    

    def logout_user(self):
        confirm = messagebox.askyesno("Confirmation", "Do you really want to log out?")
        if not confirm:
            return
        
        current_user_path = "current_user.json"

        try:
            if os.path.exists(current_user_path):
                os.remove(current_user_path)
                print("Файл current_user.json видалено.")

            # --- Перезапуск програми ---
            python = sys.executable
            os.execl(python, python, *sys.argv)

        except Exception as e:
            print(f"Помилка при Log Out: {e}")

    def show(self):
        self.lift()
        self.pack(side="right", expand=True, fill="both")

    def hide(self):
        self.pack_forget()
    
    def create_change_ui(self):
         
        
        if self.registered == 0:
            max_width = 1000
            text_label = "Enter your data"
        else:
            max_width = 800
            text_label = "Change Profile"
        self.change_frame = ctk.CTkFrame(self, width=max_width, height=int(600), fg_color="#E6E4E4")

        # --------- ХЕДЕР ---------
        header_frame = ctk.CTkFrame(self.change_frame, width=max_width, height=int(50), fg_color="#58C75C", corner_radius=0)
        header_frame.place(x=0, y=0)

        header_label = ctk.CTkLabel(
            master=header_frame,
            text=text_label,
            text_color="white",
            font=("Inter", 20, "bold")
        )
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # --------- КОНТЕНТ ФРЕЙМ ---------
        content_frame = ctk.CTkFrame(self.change_frame, width=int(500), height=int(470), fg_color="#FFFFFF", corner_radius=7)
        content_frame.place(x=25, y=70)

        # --------- АВАТАР ---------
        if self.registered == 0:
            ax = 670
            ay = 100
        else:
            ax = 575
            ay = 152
            
        self.set_avatar_image(ax, ay, self.change_frame)
        
            
        # ---------- КНОПКИ ПІД АВАТАРКОЮ ----------
        def create_icon_button(master, text, image_path, x, y, width, height, font_size, icon_size, btn_color, hover_color, command):
            image = Image.open(image_path).resize(icon_size, Image.Resampling.LANCZOS)
            icon = ctk.CTkImage(light_image=image, dark_image=image, size=icon_size)

            btn = ctk.CTkButton(
                master,
                text=text,
                image=icon,
                compound="left",
                anchor="w",
                width=int(width * 1.364),
                height=int(height * 1.33),
                corner_radius=7,
                font=("Arial", font_size),
                fg_color=btn_color,
                hover_color=hover_color,
                text_color="white",
                command = command
            )
            btn.place(x=x, y=y)
            return btn

        if self.registered == 0:
            buttons_x = 655
            buttons_start_y = 280
        else:
            buttons_x = 560
            buttons_start_y = 340
            
        button_spacing = 13

        create_icon_button(
            master=self.change_frame,
            text="     Add Photo",
            image_path=r"icons/add.png",
            x=buttons_x,
            y=buttons_start_y,
            width=146,
            height=31,
            font_size=18,
            icon_size=(18, 18),
            btn_color="#58C75C",
            hover_color="#46A34C",
            command=self.add_photo
        )

        create_icon_button(
            master=self.change_frame,
            text="      Remove",
            image_path=r"icons/cancel.png",
            x=buttons_x,
            y=buttons_start_y + 1 * (int(31 * 1.33) + button_spacing),
            width=146,
            height=31,
            font_size=18,
            icon_size=(21, 21),
            btn_color="#58C75C",
            hover_color="#46A34C",
            command=lambda: print("Remove")
        )
        if self.registered == 0:
            plus = 37
        else:
            plus = 31
            
        create_icon_button(
            master=self.change_frame,
            text="       Confirm",
            image_path=r"icons/confirmation.png",
            x=buttons_x,
            y=buttons_start_y + 2 * (int(plus * 1.33) + button_spacing),
            width=146,
            height=31,
            font_size=18,
            icon_size=(19, 19),
            btn_color="#58C75C",
            hover_color="#46A34C",
            command=self.confirm_profile_change
        )
        
            

        if self.registered == 0:
            pass
        else:
            cancel_btn = ctk.CTkButton(
                master=self.change_frame,
                text="Cancel",
                width=110,
                height=36,
                corner_radius=7,
                font=("Arial", 14),
                fg_color="#9F9F9F",
                hover_color="#8A8A8A",
                text_color="white",
                command=self.show_statistic 
            )
            cancel_btn.place(x=buttons_x + 45, y=buttons_start_y + 3 * (41 + button_spacing))

        # ---------- КОНТРОЛІ ----------

        frame_width = 470
        frame_height = 40
        spacing = 24
        start_y = 10
        field_labels = ["Name:", "Date of Birth:", "Weight:", "Height:", "Sex:", "Goal:", "Activity factor:"]

        radio_vars = {}

        for i, label_text in enumerate(field_labels):
            bg_color = "#FFFFFF" if label_text == "Activity factor:" else "#E9E9E9"
            inner_frame = ctk.CTkFrame(content_frame, width=frame_width, height=frame_height, fg_color=bg_color, corner_radius=4)
            inner_frame.place(x=15, y=start_y + i * (frame_height + spacing))

            label = ctk.CTkLabel(inner_frame, text=label_text, text_color="#000000", anchor="w", font=("Arial", 14))
            label.place(x=10, rely=0.5, anchor="w")

            # Додаткові елементи керування
            if label_text == "Name:":
                entry = ctk.CTkEntry(inner_frame, width=340, height=30, fg_color="white", text_color="black")
                entry.place(x=100, rely=0.5, anchor="w")

            elif label_text == "Date of Birth:":
                year_entry = ctk.CTkEntry(inner_frame, width=60, height=30, fg_color="white", text_color="black", placeholder_text="YYYY")
                year_entry.place(x=130, rely=0.5, anchor="center")

                month_entry = ctk.CTkEntry(inner_frame, width=60, height=30, fg_color="white", text_color="black", placeholder_text="MM")
                month_entry.place(x=220, rely=0.5, anchor="center")

                day_entry = ctk.CTkEntry(inner_frame, width=60, height=30, fg_color="white", text_color="black", placeholder_text="DD")
                day_entry.place(x=310, rely=0.5, anchor="center")
            
            elif label_text == "Weight:":
                weight_slider = TrackSlider(inner_frame, x=80, y=0, min_val=40, max_val=200, initial=self.user.weight, label_text="Weight")
            elif label_text == "Height:":
                height_slider = TrackSlider(inner_frame, x=80, y=0, min_val=100, max_val=210, initial=self.user.height, label_text="Height")

            elif label_text == "Sex:":
                var = tk.StringVar(value="")

                def make_radio(parent, text, value, x_offset):
                    def on_click():
                        var.set(value)
                        for btn in radio_vars["Sex:"]:
                            btn.configure(fg_color="#E9E9E9")
                        radio_btn.configure(fg_color="#58C75C")

                    radio_btn = ctk.CTkButton(
                        master=parent,
                        width=25,
                        height=25,
                        text="",
                        fg_color="#E9E9E9",
                        hover_color="#D0D0D0",
                        command=on_click,
                        corner_radius=12.5,
                        border_width=2,
                        border_color="#4A4A4A"
                    )
                    radio_btn.place(x=x_offset, rely=0.5, anchor="w")
                    label = ctk.CTkLabel(master=parent, text=text, text_color="black")
                    label.place(x=x_offset + 25, rely=0.5, anchor="w")
                    self.sex_button_map[radio_btn] = value
                    
                    return radio_btn

                radio_vars["Sex:"] = [
                    make_radio(inner_frame, "  Male", "M", 100),
                    make_radio(inner_frame, "  Female", "F", 240)
                ]

            elif label_text == "Goal:":
                var = tk.StringVar(value="")

                def make_goal(parent, text, value, x_offset):
                    def on_click():
                        var.set(value)
                        for btn in radio_vars["Goal:"]:
                            btn.configure(fg_color="#E9E9E9")
                        radio_btn.configure(fg_color="#58C75C")

                    radio_btn = ctk.CTkButton(
                        master=parent,
                        width=25,
                        height=25,
                        text="",
                        fg_color="#E9E9E9",
                        hover_color="#D0D0D0",
                        command=on_click,
                        corner_radius=12.5,
                        border_width=2,
                        border_color="#4A4A4A"
                    )
                    radio_btn.place(x=x_offset, rely=0.5, anchor="w")
                    label = ctk.CTkLabel(master=parent, text=text, text_color="black")
                    label.place(x=x_offset + 25, rely=0.5, anchor="w")
                    self.goal_button_map[radio_btn] = value
                    return radio_btn

                radio_vars["Goal:"] = [
                    make_goal(inner_frame, "  Lose", "L", 100),
                    make_goal(inner_frame, "  Gain", "G", 200),
                    make_goal(inner_frame, "  Maintain", "M", 300)
                ]
            elif label_text == "Activity factor:":
                choose_button = ctk.CTkButton(
                    master=inner_frame,
                    text="Choose",
                    width=200,
                    height=40,
                    font=("Arial", 18),
                    text_color="white",
                    fg_color="#58C75C",
                    hover_color="#4CAF50",
                    corner_radius=7,
                    command=self.show_choose  
                )
                choose_button.place(x=140, rely=0.5, anchor="w")
                
        self.name_entry = entry
        self.year_entry = year_entry
        self.month_entry = month_entry
        self.day_entry = day_entry
        self.weight_slider = weight_slider
        self.height_slider = height_slider
        self.radio_vars = radio_vars

    def add_photo(self):
        file_path = filedialog.askopenfilename(
            title="Choose Profile Image",
            filetypes=[("Image files", "*.jpg *.png")]
        )
    
        if not file_path:
            return  # Користувач скасував

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.jpg', '.png']:
            messagebox.showerror(" Error", "Please select a .jpg or .png file.")
            return

        try:
            # Збереження байтів зображення
            with open(file_path, 'rb') as file:
                self.avatar_image_blob = file.read()

            # Відображення у UI
            image = Image.open(io.BytesIO(self.avatar_image_blob))
            image = image.resize((166, 166))
            self.avatar_ctk_image = ctk.CTkImage(light_image=image, size=(166, 166))
            self.avatar_label.configure(image=self.avatar_ctk_image)

        except Exception as e:
            messagebox.showerror(" Error", f"Failed to load image: {e}")

    def confirm_profile_change(self):
        print("confirmation")

        # --- Ім'я ---
        name = self.name_entry.get() or self.user.name

        try:
            original_birth_year, original_birth_month, original_birth_day = map(int, self.user.birth_date.split("-"))
        except Exception:
            original_birth_year, original_birth_month, original_birth_day = 2000, 1, 1

        try:
            birth_year = int(self.year_entry.get())
        except ValueError:
            birth_year = original_birth_year

        try:
            birth_month = int(self.month_entry.get())
        except ValueError:
            birth_month = original_birth_month

        try:
            birth_day = int(self.day_entry.get())
        except ValueError:
            birth_day = original_birth_day

        weight = self.weight_slider.value or self.user.weight
        height = self.height_slider.value or self.user.height

        avatar_blob = getattr(self, 'avatar_image_blob', self.user.avatar_image)

        # --- Стать ---
        sex = ""
        for btn in self.radio_vars["Sex:"]:
            if btn.cget("fg_color") == "#58C75C":
                sex = self.sex_button_map[btn]
                break
        if not sex:
            sex = self.user.sex

        # --- Ціль ---
        goal = ""
        for btn in self.radio_vars["Goal:"]:
            if btn.cget("fg_color") == "#58C75C":
                goal = self.goal_button_map[btn]
                break
        if not goal:
            goal = self.user.goal

        # Інші параметри:
        activity_factor = self.user.activity_factor
        
        bjv_mode = self.user.bjv_mode
        email = self.user.email
        password = self.user.password 

        birth_date_str = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"

        try:
            if self.registered == 0:
                # --- Реєстрація нового користувача ---
                insert_query = f"""
                    INSERT INTO USERS (
                        EMAIL, PASSWORD, NAME, AVATAR_IMAGE, BIRTH_DATE, WEIGHT, HEIGHT, SEX, GOAL, BJV_MODE, ACTIVITY_FACTOR
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """
                values = (
                    email, password, name, avatar_blob, birth_date_str,
                    int(weight), int(height), sex, goal, bjv_mode, float(activity_factor)
                )

                conn = sqlite3.connect("Health_database.db")
                cursor = conn.cursor()
                cursor.execute(insert_query, values)
                conn.commit()
                conn.close()
                print("User inserted successfully.")
                self.update_current_user_email(email)

            else:
                # --- Оновлення профілю ---
                columns = ["NAME", "BIRTH_DATE", "WEIGHT", "HEIGHT", "SEX", "GOAL", "AVATAR_IMAGE", "ACTIVITY_FACTOR"]
                values = [
                    f"'{name}'",
                    f"'{birth_date_str}'",
                    weight,
                    height,
                    f"'{sex}'",
                    f"'{goal}'",
                    "?",
                    activity_factor
                ]
                condition = f"EMAIL = '{email}'"

                DBControl.update_data(
                    file_name="Health_database.db",
                    table_name="USERS",
                    columns_array=columns,
                    values_array=values,
                    is_image=True,
                    data_tuple=(avatar_blob,),
                    object_condition=condition
                )
                print("User updated successfully.")

        except Exception as e:
            print(f"Error saving user data: {e}")
            return

        # Перезапуск програми
        python = sys.executable
        os.execl(python, python, *sys.argv)
            
            
    
    def update_current_user_email(self, new_email):
        current_user_path = "current_user.json"  
        data = {"email": new_email}

        try:
            with open(current_user_path, "w") as f:
                json.dump(data, f)
            print("current_user.json updated.")
        except Exception as e:
            print(f"Failed to update current_user.json: {e}")

    def create_activity_ui(self):
        self.activity_frame = ctk.CTkFrame(self, width=800, height=600, fg_color="#E6E4E4")
        
        # Хедер
        header_frame = ctk.CTkFrame(self.activity_frame, width=800, height=50, fg_color="#58C75C", corner_radius=0)
        header_frame.place(x=0, y=0)

        header_label = ctk.CTkLabel(
            master=header_frame,
            text="Choose Activity",
            text_color="white",
            font=("Inter", 20, "bold")
        )
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Змінні для радіокнопок
        self.work_var = tk.StringVar(value="")
        self.sports_var = tk.StringVar(value="")

        # Функція для створення групи радіокнопок
        def create_radio_group(parent, y_position, label_text, options, variable):
            label_frame = ctk.CTkFrame(parent, width=260, height=40, fg_color="white")
            label_frame.place(relx=0.5, y=y_position, anchor="n")

            label = ctk.CTkLabel(
                master=label_frame,
                text=label_text,
                font=("Inter", 16, "bold")
            )
            label.place(relx=0.5, rely=0.5, anchor="center")

            radio_buttons = []
            for i, (text, value, icon_path) in enumerate(options):
                def on_click(val=value, idx=i):
                    variable.set(val)
                    for btn in radio_buttons:
                        btn.configure(fg_color="#E9E9E9")
                    radio_buttons[idx].configure(fg_color="#58C75C")

                frame = ctk.CTkFrame(parent, width=200, height=150, fg_color="white")
                frame.place(x=70 + i * 220, y=y_position + 57)

                icon_img = ctk.CTkImage(light_image=Image.open(icon_path), size=(80, 80))
                icon_label = ctk.CTkLabel(master=frame, image=icon_img, text="")
                icon_label.place(relx=0.5, y=15, anchor="n")

                radio_btn = ctk.CTkButton(
                    master=frame,
                    width=25,
                    height=25,
                    text="",
                    fg_color="#E9E9E9",
                    hover_color="#D0D0D0",
                    command=on_click,
                    corner_radius=12.5,
                    border_width=2,
                    border_color="#4A4A4A"
                )
                radio_btn.place(x=20, y=115)

                label = ctk.CTkLabel(master=frame, text=text, text_color="black", font=("Inter", 16, "bold"))
                label.place(x=50, y=115)

                radio_buttons.append(radio_btn)

        # Опції для "Type of Work"
        work_options = [
            ("Sedentary", "Sedentary", "icons/sedentary.png"),
            ("Standing", "Standing", "icons/teacher.png"),
            ("Active", "Active", "icons/mechanic.png")
        ]
        create_radio_group(self.activity_frame, 70, "Type of work", work_options, self.work_var)

        # Опції для "Doing Sports"
        sports_options = [
            ("No sport", "No sport", "icons/no-sport.png"),
            ("Light", "Light", "icons/sports.png"),
            ("Heavy", "Heavy", "icons/sport.png")
        ]
        create_radio_group(self.activity_frame, 290, "Doing sports", sports_options, self.sports_var)

        # Кнопка Cancel
        def on_cancel():
            if messagebox.askyesno("Cancel editing?", "Cancel editing?"):
                self.show_change2()

        cancel_button = ctk.CTkButton(
            master=self.activity_frame,
            text="Cancel",
            width=120,
            height=40,
            corner_radius=7,
            font=("Inter", 16, "bold"),
            text_color="white",
            fg_color="#9F9F9F",
            hover_color="#8A8A8A",
            command=on_cancel
        )
        cancel_button.place(x=110, y=520)

        # Кнопка Confirm
        confirm_icon = ctk.CTkImage(
            light_image=Image.open("icons/confirmation.png"),
            size=(19, 19)
        )

        def get_activity_factor():
            work = self.work_var.get()
            sports = self.sports_var.get()

            if work == "Sedentary":
                if sports == "No sport":
                    return 1.2
                elif sports == "Light":
                    return 1.375
                elif sports == "Heavy":
                    return 1.55
            elif work == "Standing":
                if sports == "No sport":
                    return 1.375
                elif sports == "Light":
                    return 1.55
                elif sports == "Heavy":
                    return 1.725
            elif work == "Active":
                if sports == "No sport":
                    return 1.55
                elif sports == "Light":
                    return 1.725
                elif sports == "Heavy":
                    return 1.9

            return 1.2  # Значення за замовчуванням

        def on_confirm():
            if messagebox.askyesno("Confirm", "Confirm the changes?"):
                activity_factor = get_activity_factor()
                print(f"Selected activity factor: {activity_factor}")
                
                self.user.activity_factor = activity_factor
                
                

                self.show_change2()

        confirm_button = ctk.CTkButton(
            master=self.activity_frame,
            text="         Confirm",
            image=confirm_icon,
            compound="left",
            anchor="w",
            width=200,
            height=40,
            corner_radius=7,
            font=("Inter", 16, "bold"),
            text_color="white",
            fg_color="#58C75C",
            hover_color="#45B24B",
            command=on_confirm
        )
        confirm_button.place(x=510, y=520)
       
    
class TrackSlider:
    def __init__(self, parent, x, y, min_val, max_val, initial, label_text):
        self.min_val = min_val
        self.max_val = max_val
        self.track_start = 10
        self.track_end = 340
        self.track_y = 25
        self.knob_radius = 5
        self.knob_color = "#3EDD43"

        # Створюємо Canvas
        self.canvas = tk.Canvas(parent, width=350, height=50, bg="#E9E9E9", highlightthickness=0)
        self.canvas.place(x=x, y=y)

        # Створюємо label для значення всередині canvas
        self.value_label = tk.Label(self.canvas, text=str(initial), font=("Arial", 10), bg="#E9E9E9")
        self.label_id = self.canvas.create_window(0, 0, window=self.value_label)  # Координати оновлюються пізніше

        # Малюємо лінію
        self.canvas.create_line(
            self.track_start, self.track_y, self.track_end, self.track_y,
            fill="black", width=4, capstyle=tk.ROUND
        )

        # Створюємо кружок
        self.value = initial
        self.knob = self.canvas.create_oval(0, 0, 0, 0, fill=self.knob_color, outline="#000")

        self.update_knob_position()

        # Обробка подій миші
        self.canvas.tag_bind(self.knob, "<B1-Motion>", self.move_knob)
        self.canvas.tag_bind(self.knob, "<Button-1>", self.move_knob)

    def update_knob_position(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        x_pos = self.track_start + ratio * (self.track_end - self.track_start)
        y = self.track_y

        # Оновлюємо координати кружка
        self.canvas.coords(
            self.knob,
            x_pos - self.knob_radius,
            y - self.knob_radius,
            x_pos + self.knob_radius,
            y + self.knob_radius
        )

        # Оновлюємо значення та позицію підпису
        self.value_label.config(text=str(int(self.value)))
        self.canvas.coords(self.label_id, x_pos, y - 15) 

    def move_knob(self, event):
        x = min(max(event.x, self.track_start), self.track_end)
        ratio = (x - self.track_start) / (self.track_end - self.track_start)
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        self.update_knob_position()

    def get_value(self):
        return self.value
    
    

