import customtkinter
from PIL import Image
from path import app_path


# icons downloaded from https://icons8.com


# class NavbarFrame creates a frame that functions as a navbar
class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=("gray65", "gray40"), corner_radius=0)
        self.master = master
        self.icon_path = app_path + "/icons/neutral_100.png"
        self.karma_message = "Consistency is everything. Keep going."
        self.karma_icon_neutral = customtkinter.CTkImage(
            Image.open(app_path + "/icons/neutral_100.png"), size=(32, 32)
        )
        self.karma_icon_bad_3 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/bad_3_100.png"), size=(32, 32)
        )
        self.karma_icon_bad_2 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/bad_2_100.png"), size=(32, 32)
        )
        self.karma_icon_bad_1 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/bad_1_100.png"), size=(32, 32)
        )
        self.karma_icon_good_1 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/good_1_100.png"), size=(32, 32)
        )
        self.karma_icon_good_2 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/good_2_100.png"), size=(32, 32)
        )
        self.karma_icon_good_3 = customtkinter.CTkImage(
            Image.open(app_path + "/icons/good_3_100.png"), size=(32, 32)
        )
        self.karma_counter = 0
        self.karma_label = customtkinter.CTkLabel(
            self,
            text="Karma: ",
            font=master.app_font,
            text_color=("white"),
        )
        self.karma_label.grid(row=0, column=4, padx=(10, 100), pady=10, sticky="e")
        self.karma_counter_label = customtkinter.CTkLabel(
            self,
            text=f"{self.karma_counter} | ",
            font=master.app_font,
            text_color=("white"),
            image=self.karma_icon_neutral,
            compound="right",
        )
        self.karma_counter_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.switch_icon_light = customtkinter.CTkImage(
            Image.open(app_path + "/icons/light_78.png"), size=(32, 32)
        )

        self.mode_switch_var = customtkinter.StringVar(value="off")
        self.mode_switch = customtkinter.CTkSwitch(
            self,
            text="",
            command=self.change_mode,
            variable=self.mode_switch_var,
            onvalue="on",
            offvalue="off",
            font=master.app_font,
        )
        self.mode_switch.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.switch_label = customtkinter.CTkLabel(
            self,
            text="",
            image=self.switch_icon_light,
        )
        self.switch_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")
        self.save_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/save_96.png"), size=(28, 28)
        )

        self.end_of_day_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/dusk_96.png"), size=(30, 30)
        )
        self.end_of_day_label = customtkinter.CTkLabel(
            self,
            text="",
            image=self.end_of_day_icon,
        )
        self.end_of_day_label.grid(
            row=0, column=2, padx=(0, 10), pady=(5, 0), sticky="e"
        )
        self.end_of_day_var = customtkinter.StringVar(value="00:00")
        self.end_of_day = customtkinter.CTkOptionMenu(
            self,
            values=[
                "12:00",
                "13:00",
                "14:00",
                "15:00",
                "16:00",
                "17:00",
                "18:00",
                "19:00",
                "20:00",
                "21:00",
                "22:00",
                "23:00",
            ],
            variable=self.end_of_day_var,
            dynamic_resizing=True,
            width=100,
            font=("Century Gothic", 15),
        )
        self.end_of_day.grid(row=0, column=3, sticky="w", padx=(0, 10), pady=10)
        self.grid_columnconfigure((2), weight=1)

    def change_mode(self):
        if self.mode_switch_var.get() == "off":
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def update_karma(self, karma):
        self.karma_counter += karma
        self.karma_counter_label.configure(text=f"{self.karma_counter} | ")
        if self.karma_counter in range(1, 1500):
            self.karma_counter_label.configure(image=self.karma_icon_good_1)
            self.icon_path = app_path + "/icons/good_1_100.png"
            self.karma_message = "Good work! :)"
        elif self.karma_counter in range(1500, 3000):
            self.karma_counter_label.configure(image=self.karma_icon_good_2)
            self.icon_path = app_path + "/icons/good_2_100.png"
            self.karma_message = "Great day, keep it that way. ;)"
        elif self.karma_counter >= 3000:
            self.karma_counter_label.configure(image=self.karma_icon_good_3)
            self.icon_path = app_path + "/icons/good_3_100.png"
            self.karma_message = "You're awesome :D The world is yours!"
        elif self.karma_counter in range(-499, 0):
            self.karma_counter_label.configure(image=self.karma_icon_bad_1)
            self.icon_path = app_path + "/icons/bad_1_100.png"
            self.karma_message = "Don't worry, tomorrow will be better."
        elif self.karma_counter in range(-999, -499):
            self.karma_counter_label.configure(image=self.karma_icon_bad_2)
            self.icon_path = app_path + "/icons/bad_2_100.png"
            self.karma_message = "Just try to stick to your habits."
        elif self.karma_counter <= -1000:
            self.karma_counter_label.configure(image=self.karma_icon_bad_3)
            self.icon_path = app_path + "/icons/bad_3_100.png"
            self.karma_message = (
                "Days like this happen. Shake it off and get a good night's sleep."
            )
        else:
            self.karma_counter_label.configure(image=self.karma_icon_neutral)
            self.icon_path = app_path + "/icons/neutral_100.png"
            self.karma_message = "Consistency is everything. Keep going."
