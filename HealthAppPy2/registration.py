from user import User
from DB_control import DBControl
import base64
import tkinter.messagebox as messagebox
import os
import json
import sys
from profile_window import ProfileWindow



# user_table_sql = """CREATE TABLE IF NOT EXISTS USERS (
#                             EMAIL TEXT PRIMARY KEY,
#                             PASSWORD TEXT NOT NULL,
#                             NAME TEXT NOT NULL,
#                             AVATAR_IMAGE BLOB NOT NULL,
#                             BIRTH_DATE DATE NOT NULL,
#                             WEIGHT INTEGER NOT NULL,
#                             HEIGHT INT NOT NULL,
#                             SEX TEXT NOT NULL,
#                             GOAL TEXT NOT NULL,
#                             BJV_MODE TEXT NOT NULL,
#                             ACTIVITY_FACTOR REAL NOT NULL
#                             );"""

class Registration:
    def __init__(self, db_name="Health_database.db"):
        self.db_name = db_name
        self.db = DBControl()
        
    

    def login_user(self, email, password):
        user_data = self.db.receive_data(
            self.db_name,
            "USERS",
            "*",
            f"EMAIL = '{email}'"
        )

        if not user_data:
            messagebox.showerror("Login Error", "User not found. Please register first.")
            return None
        
        row = user_data[0]

        stored_password = row[1]

        if password != stored_password:
            messagebox.showerror("Login Error", "Incorrect password.")
            return None

        user = User(
            name=row[2],
            email=row[0],
            password=row[1],
            avatar_image=row[3],
            birth_date=row[4],
            weight=row[5],
            height=row[6],
            sex=row[7],
            goal=row[8],
            activity_factor=row[10],
            bjv_mode=row[9]
        )

        with open("current_user.json", "w") as file:
            json.dump({"email": user.email}, file, indent=4)

        
        python = sys.executable
        os.execl(python, python, * sys.argv)

        return user
    
    def load_or_register_user(self):
        current_user_path = "current_user.json"

        if os.path.exists(current_user_path):
            with open(current_user_path, "r") as file:
                data = json.load(file)
                user_email = data.get("email")

                result = DBControl.receive_data(
                    "Health_database.db", "USERS",
                    "*", f"EMAIL = '{user_email}'"
                )

                if result:
                    row = result[0]
                    # EMAIL, PASSWORD, NAME, AVATAR_IMAGE, BIRTH_DATE, WEIGHT, HEIGHT, SEX, GOAL, BJV_MODE, ACTIVITY_FACTOR
                    return User(
                        name=row[2],
                        email=row[0],
                        password=row[1],
                        avatar_image=row[3],
                        birth_date=row[4],
                        weight=row[5],
                        height=row[6],
                        sex=row[7],
                        goal=row[8],
                        activity_factor=row[10],
                        bjv_mode=row[9]
                    )
                else:
                    print("No User with such email in DataBase")
                    os.remove(current_user_path)

        return 0

        
    
    
        
        