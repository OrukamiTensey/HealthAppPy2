import datetime
from nutrition import Nutrition

class User:
    def __init__(self, name, email, password, avatar_image, birth_date, weight, height, sex, goal, activity_factor, bjv_mode):
        self.name = name
        self.email = email
        self.password = password
        self.avatar_image = avatar_image
        self.birth_date = birth_date  # у форматі YYYY-MM-DD
        self.weight = weight
        self.height = height
        self.sex = sex  # 'M' або 'F'
        self.goal = goal  
        self.activity_factor = float(activity_factor) # 1.2  1.55  1.9
        self.bjv_mode = bjv_mode
        
    def get_age(self):
        today = datetime.date.today()
        birth = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "avatar_image": self.avatar_image,
            "birth_date": self.birth_date,
            "weight": self.weight,
            "height": self.height,
            "sex": self.sex,
            "goal": self.goal,
            "activity_factor": self.activity_factor,
            "bjv_mode": self.bjv_mode
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["name"], data["email"], data["password"], data["avatar_image"], data["birth_date"],
            data["weight"], data["height"], data["sex"], data["goal"],
            data["activity_factor"], data["bjv_mode"]
        )

    def display_profile(self):
        print("\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.get_age()} years")
        print(f"Weight: {self.weight} kg")
        print(f"Height: {self.height} cm")
        print(f"Sex: {self.sex}")
        print(f"Goal: {self.goal}\n")
        print(f"Activity factor: {self.activity_factor}\n")
        
