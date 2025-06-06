import customtkinter as ctk
from DB_control import DBControl
from sidebar import Sidebar
from bmi_calculator import BMICalculator
from nutrition_window import NutritionWindow
from user import User
from calorie_counting import CalorieCounting
from profile_window import ProfileWindow
from registration import Registration
from reg_window import RegistrationWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calorie Tracker")
        self.geometry("1000x600")
        self.resizable(True, True)

        self.sidebar = Sidebar(self, self.switch_window)
        self.sidebar.pack(side="left", fill="y")
        self.reg = Registration()
        user = self.reg.load_or_register_user()
        
        if user == 0:
            
            self.windows = {
                "Registration": RegistrationWindow(self, 0)
            }

            
            self.sidebar.pack_forget()

            self.current_window = "Registration"
            self.windows["Registration"].place(x=0, y=0, relwidth=1, relheight=1)
            self.windows["Registration"].show()
            return
        

        self.calorie_counter = CalorieCounting(user)

        self.windows = {
            "BMI": BMICalculator(self, user),
            "Nutrition": NutritionWindow(self, user),
            "Profile": ProfileWindow(self, user, 1),
            "Registration": RegistrationWindow(self, 1)
        }

        for window in self.windows.values():
            window.place(x=200, y=0, relwidth=1, relheight=1)
            window.hide()

        self.current_window = None
        self.switch_window("Profile")
        

    def switch_window(self, name):
        if self.current_window:
            self.windows[self.current_window].hide()

        # Updating norm in db
        if name == "BMI":
            self.calorie_counter.update_norm_if_needed("Health_database.db")
            

        self.current_window = name
        self.windows[name].show()