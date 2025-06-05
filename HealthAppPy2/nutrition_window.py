from tkinter import ttk, messagebox

import customtkinter as ctk
from nutrition import Nutrition
from PIL import Image
import io
import tkinter as tk

class Func_Button(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master = master,
            width = 100,
            height = 40,
            font = ("Inter", 15, "bold"),
            text_color = "white",
            **kwargs
        )

class Enter(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(
            master = master,
            width = 150,
            height = 40,
            font = ("Inter", 14),
            text_color = "black",
            fg_color = "#FFFFFF",
            placeholder_text_color = "#AAAAAA",
            border_color = "#FFFFFF",
            border_width = 0,
            **kwargs
        )

class NutritionWindow(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user.email
        self.catalog_path = "activity_catalog.json"
        self.user_email = user.email
        self.nutrition_functions = Nutrition(user)

        self.image_frame = None
        self.tree = None
        self.combo = None
        self.mass_enter = None
        self.remove_enter = None
        self.add_button = None
        self.remove_button = None

        self.configure(fg_color="#E6E4E4", corner_radius = 0)

        # Already creating interface:
        self.create_header()
        self.create_main_content()
        self.create_image_frame()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#C75858", corner_radius=0, height=50)
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(
            master = header_frame,
            text = "Calculate consumed products",
            text_color = "white",
            font = ("Inter", 20, "bold")
        )
        header_label.pack(pady=10)

    def create_main_content(self):
        self.content_frame = ctk.CTkFrame(self, fg_color="#E6E4E4", corner_radius=0)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)
        self.content_frame.grid_rowconfigure(3, weight=1)

        style = ttk.Style()
        style.configure("Custom.TCombobox",
                        padding=(10, 12, 10, 12),  # (left, top, right, bottom)
                        font=("Inter", 15))

        table_values = self.nutrition_functions.get_all_products_list()

        self.combo = ttk.Combobox(self.content_frame, values=table_values, height=4, font = ("Inter", 15), style="Custom.TCombobox")
        self.combo.set("Select product")
        self.combo.bind("<<ComboboxSelected>>", self.on_product_selected)
        self.combo.grid(row=0, column=0, sticky="ew", columnspan=2, pady=(0, 10))

        add_frame = ctk.CTkFrame(self.content_frame, fg_color="#E6E4E4")
        add_frame.grid(row=1, column=0, sticky="w", pady=(0, 30))

        self.mass_enter = Enter(add_frame, placeholder_text="Enter grams", corner_radius=7)
        self.mass_enter.pack(side="left", padx=(0, 10))

        self.add_button = Func_Button(add_frame, text="Add", fg_color="#58C75C", hover_color="#3CAE40", corner_radius=7, command=self.add_product)
        self.add_button.pack(side="left")

        remove_frame = ctk.CTkFrame(self.content_frame, fg_color="#E6E4E4")
        remove_frame.grid(row=1, column=1, sticky="e", pady=(0, 30))

        self.remove_button = Func_Button(remove_frame, text="Remove", fg_color="#C75858", hover_color="#A34848", corner_radius=7, command = self.remove_product)
        self.remove_button.pack(side="left", padx=(0, 10))

        self.remove_enter = Enter(remove_frame, placeholder_text="Enter id", corner_radius=7)
        self.remove_enter.pack(side="left")

        self.create_table()

    # ------------------   Making table in the Content Frame   ------------------
    def create_table(self):
        table_frame = tk.Frame(self.content_frame, background="#E6E4E4")
        table_frame.grid(row=3, column=0, sticky="nsew", columnspan=3)

        nutrition_columns_names = [
            ("id", "ID", 17, "center"),
            ("product", "Product", 300, "w"),
            ("mass", "Mass", 80, "center"),
            ("proteins", "Proteins", 80, "center"),
            ("fats", "Fats", 80, "center"),
            ("carbohydrates", "Carbohydrates", 85, "center"),
            ("kcal", "Kcal", 80, "center")
        ]

        self.tree = ttk.Treeview(table_frame, height=17, columns=[array[0] for array in nutrition_columns_names], show="headings")

        for col_var, col_name, col_width, col_anchor in nutrition_columns_names:
            self.tree.heading(col_var, text=col_name)
            self.tree.column(col_var, width=col_width, anchor=col_anchor)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        start_rows = self.nutrition_functions.show_today_consumption()
        for row in start_rows:
            self.insert_row_to_table(list(row))

    # ------------------   Making image holder for chosen product   ------------------
    def create_image_frame(self):
        self.image_frame = ctk.CTkFrame(self.content_frame, width=100, height=100, fg_color="#E6E4E4", corner_radius=7)
        # self.image_frame.place(x=640, y=0)
        self.image_frame.grid(row=0, column=2, sticky="ne", padx=(30, 0), rowspan=2, pady=(0, 30))

        image_blob = self.nutrition_functions.get_product_image("Select product")
        self.set_image(image_blob)
         
    # ------------------   Functional methods   ------------------
    def on_product_selected(self, event):
        product = self.combo.get()

        for widget in self.image_frame.winfo_children():
            widget.destroy()

        image_blob = self.nutrition_functions.get_product_image(product)

        if not image_blob:
            image_blob = self.nutrition_functions.get_product_image("Select product")
        
        self.set_image(image_blob)
        
    def set_image(self, image_blob):
        image = Image.open(io.BytesIO(image_blob))
        image = image.resize((100, 100))

        ctk_image = ctk.CTkImage(light_image=image, size=(100, 100))

        image_label = ctk.CTkLabel(self.image_frame, image=ctk_image, text="")
        image_label.image = ctk_image
        image_label.pack(expand=True)
        
    def is_number(self, value):
        try:
            return float(value) != 0
        except ValueError:
            return False

    def show_recorded_rows(self):
        start_rows = self.nutrition_functions.show_today_consumption()
        for row in start_rows:
            self.insert_row_to_table(list(row))
        
    def insert_row_to_table(self, values_list):
        row_number = len(self.tree.get_children()) + 1
        values_list.insert(0, row_number)
        new_row = self.tree.insert("", "end", values = (values_list[:1] + values_list[3:]))
        self.tree.see(new_row)

    def add_product(self):
        product = self.combo.get()
        mass = self.mass_enter.get()

        if not self.nutrition_functions.check_product(product):
            messagebox.showerror("Error", "Choose product from the list!")
        elif not self.is_number(mass):
            messagebox.showerror("Error", "Enter valid amount of grams of product!")
        else:
            product_values = self.nutrition_functions.add_consumed_product(product, mass)
            self.insert_row_to_table(product_values)

        self.mass_enter.delete(0, 'end')

    def remove_product(self):
        id_to_remove = self.remove_enter.get()

        if not id_to_remove.isdigit():
            messagebox.showerror("Error", "Enter valid row ID to remove the product!")
            return

        id_to_remove = int(id_to_remove)
        all_items = self.tree.get_children()

        if id_to_remove < 1 or id_to_remove > len(all_items):
            messagebox.showerror("Error", "No such ID in the table!")
            return

        item_to_remove = all_items[id_to_remove - 1]
        values = self.tree.item(item_to_remove)['values']

        self.nutrition_functions.remove_consumed_product(values[1], float(values[2]))

        self.tree.delete(item_to_remove)

        for new_id, item in enumerate(self.tree.get_children(), start = 1):
            current_values = self.tree.item(item)['values']
            self.tree.item(item, values = (new_id, *current_values[1:]))

        self.remove_enter.delete(0, 'end')

    def show(self):
        self.lift()
        self.pack(side="right", expand=True, fill="both")

    def hide(self):
        self.pack_forget()