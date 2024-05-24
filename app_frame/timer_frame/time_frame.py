import customtkinter
import re
from winotify import Notification, audio
from PIL import Image
from path import app_path

# icons downloaded from https://icons8.com


class TimeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.timer_time = 0
        self.timer_time_id = ""
        self.countdown_set = False
        self.countdown = customtkinter.CTkEntry(
            self, placeholder_text="00:00:00", width=62
        )
        self.countdown.grid(row=0, column=1, sticky="ns", padx=10, pady=10)
        self.countdown_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/hourglass_96.png"), size=(26, 26)
        )
        self.countdown_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.countdown_icon,
            width=60,
            command=self.set_countdown,
        )
        self.countdown_btn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.alarm_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/alarm_90.png"), size=(28, 28)
        )
        self.alarm_save_btn = customtkinter.CTkButton(
            self, text="", image=self.alarm_icon, width=60, command=self.set_alarm
        )
        self.alarm_save_btn.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.timer = customtkinter.CTkLabel(
            self,
            text="00:00:00",
            font=("Century Gothic", 48, "bold"),
            width=300,
            height=100,
            fg_color=("gray70", "gray30"),
            corner_radius=10,
        )
        self.timer.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=0)
        self.timer_start_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/start_90.png"), size=(26, 26)
        )
        self.timer_start_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.timer_start_icon,
            font=master.master.master.app_font,
            width=60,
            command=self.run_timer,
        )
        self.timer_start_btn.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.timer_pause_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/pause_90.png"), size=(26, 26)
        )
        self.timer_stop_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.timer_pause_icon,
            font=master.master.master.app_font,
            width=60,
            command=self.stop_timer,
        )
        self.timer_stop_btn.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.timer_reset_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/reset_100.png"), size=(26, 26)
        )
        self.timer_reset_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.timer_reset_icon,
            font=master.master.master.app_font,
            width=60,
            command=self.reset_timer,
        )
        self.timer_reset_btn.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        self.alert_msg = Notification(
            app_id="Memoboard",
            title="Alarm",
            msg="Time is up!",
            duration="long",
            icon=app_path + "/icons/memory_64.png",
        )
        self.alert_msg.set_audio(audio.Reminder, loop=False)

    def run_timer(self):
        self.timer_start_btn.configure(state="disabled", fg_color=("gray40", "gray60"))
        self.countdown_btn.configure(state="disabled", fg_color=("gray40", "gray60"))
        seconds = self.timer_time % 60
        minutes = int((self.timer_time / 60) % 60)
        hours = int((self.timer_time / 3600) % 24)
        current_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timer.configure(text=current_time)
        if current_time == "00:00:00" and self.countdown_set is True:
            self.alert_msg.show()
            self.reset_timer()
            return
        if self.countdown_set is True:
            self.timer_time -= 1
        else:
            self.timer_time += 1
        self.timer_time_id = self.after(1000, self.run_timer)

    def stop_timer(self):
        if self.timer_time_id != "":
            self.after_cancel(self.timer_time_id)
        if self.countdown_set is True:
            self.countdown_btn.configure(
                state="normal", fg_color=("#2CC985", "#2FA572")
            )
        else:
            self.timer_start_btn.configure(
                state="normal", fg_color=("#2CC985", "#2FA572")
            )

    def reset_timer(self):
        self.master.master.master.input_clue.configure(text="", fg_color="transparent")
        self.timer_time = 0
        self.timer.configure(text="00:00:00")
        self.countdown_set = False
        self.timer_start_btn.configure(state="normal", fg_color=("#2CC985", "#2FA572"))
        self.countdown_btn.configure(state="normal", fg_color=("#2CC985", "#2FA572"))
        self.stop_timer()

    def set_countdown(self):
        time_str = self.countdown.get()
        valid_time = re.match("([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", time_str)
        if time_str == "":
            self.master.master.master.input_clue.configure(
                text="Please enter a valid time.", fg_color=("white", "gray30")
            )
        elif valid_time is None:
            self.master.master.master.input_clue.configure(
                text="Valid format: HH:MM:SS\nAllowed entry: 00:00:00 - 23:59:59",
                fg_color=("white", "gray30"),
            )
        else:
            self.master.master.master.input_clue.configure(
                text="", fg_color="transparent"
            )
            time_list = time_str.split(":")
            int_time_list = [int(x) for x in time_list]
            time_in_seconds = (
                int_time_list[0] * 3600 + int_time_list[1] * 60 + int_time_list[2]
            )
            if self.countdown_set is False:
                self.timer_time = time_in_seconds
            self.countdown_set = True
            self.run_timer()

    def set_alarm(self):
        time_str = self.countdown.get()
        valid_time = re.match("([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", time_str)
        if time_str == "":
            self.master.master.master.input_clue.configure(
                text="Please enter a valid time.", fg_color=("white", "gray30")
            )
        elif valid_time is None:
            self.master.master.master.input_clue.configure(
                text="Valid format: HH:MM:SS\nAllowed entry: 00:00:00 - 23:59:59",
                fg_color=("white", "gray30"),
            )
        else:
            self.master.master.master.input_clue.configure(
                text="", fg_color="transparent"
            )
            self.master.master.master.alarm_list.add_new_alarm_to_frame(time_str)
