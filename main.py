import customtkinter
import os
import uuid
import json
import re
import random
from datetime import date, datetime, timedelta, time
from winotify import Notification, audio
from PIL import Image

# icons downloaded from https://icons8.com

app_path = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


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


# class TaskInputFrame creates a frame for adding a new task
class TaskInputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)

        self.radio_var = customtkinter.StringVar(value="")

        self.radio1 = customtkinter.CTkRadioButton(
            self,
            text="Daily",
            variable=self.radio_var,
            value="daily",
            font=master.master.master.app_font,
        )
        self.radio1.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")

        self.radio2 = customtkinter.CTkRadioButton(
            self,
            text="To-Do",
            variable=self.radio_var,
            value="optional",
            font=master.master.master.app_font,
        )
        self.radio2.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="w")

        self.task_entry = customtkinter.CTkEntry(
            self, placeholder_text="New task", font=("Century Gothic", 13)
        )
        self.task_entry.grid(
            row=1, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=2
        )

        self.button = customtkinter.CTkButton(
            self,
            text="Add Task",
            command=master.master.master.add_new_task,
            font=master.master.master.app_font,
        )
        self.button.grid(
            row=2, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=2
        )

    def get_new_task(self):
        self.button.focus_set()
        if self.radio_var.get() == "daily" or self.radio_var.get() == "optional":
            if self.task_entry.get() != "":
                new_task = (self.task_entry.get(), self.radio_var.get())
                self.task_entry.delete(0, "end")
                return new_task

            return ("NO_TASK", "")

        return ("NOTHING_CHOSEN", "")


# class TaskListFrame creates a frame in which newly created TaskFrame objects will be stored
class TaskListFrame(customtkinter.CTkScrollableFrame):
    end_of_day = False

    def __init__(self, master, title, height, width):
        super().__init__(master, height=height, width=width)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.master = master
        self.checkboxes = []
        self.row_count = 1
        self.task_list_frame_karma = 0
        self.tasks = {}

    def add_new_task_to_frame(self, task, t_type):
        task_id = str(uuid.uuid4())
        new_task = TaskFrame(self, task, t_type, t_id=task_id, t_state="normal")
        new_task.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.tasks[task_id] = new_task
        self.row_count += 1
        if TaskListFrame.end_of_day is True:
            new_task.checkbox.configure(state="disabled")

    def load_task_to_frame(self, task, t_type, t_id, t_done, t_checked, t_state):
        new_task = TaskFrame(self, task, t_type, t_id=t_id, t_state=t_state)
        new_task.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.tasks[t_id] = new_task
        new_task.done = t_done
        if t_checked == 1:
            new_task.checkbox.select()
        self.row_count += 1

    def get_task_frame_karma(self):
        return self.task_list_frame_karma

    def inc_task_list_frame_karma(self, master, karma):
        self.task_list_frame_karma += karma
        master.master.master.inc_karma(self.task_list_frame_karma)


# class TaskFrame creates a frame which contains a task with a checkbox and a delete button
class TaskFrame(customtkinter.CTkFrame):
    def __init__(self, master, task, t_type, t_id, t_state):
        super().__init__(master, fg_color=("gray90", "gray27"))
        self.grid_columnconfigure(0, weight=1)
        self.master = master
        self.done = False
        self.task = task
        self.t_type = t_type
        self.t_id = t_id
        self.t_state = t_state

        self.delete_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/delete_96.png"), size=(25, 25)
        )
        self.checkbox = customtkinter.CTkCheckBox(
            self,
            text=task,
            command=self.task_done,
            font=("Century Gothic", 13),
            state=self.t_state,
        )
        self.checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.checkbox_del_button = customtkinter.CTkButton(
            self,
            text="",
            command=self.del_task,
            width=10,
            font=("Century Gothic", 13, "bold"),
            image=self.delete_icon,
            fg_color="transparent",
            hover_color=("gray82", "gray40"),
        )
        self.checkbox_del_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def del_task(self):
        self.master.tasks.pop(self.t_id)
        self.destroy()

    def task_done(self):
        if self.done is False:
            if self.t_type == "daily":
                self.master.master.master.master.inc_karma(300)
            else:
                self.master.master.master.master.inc_karma(300)
            self.done = True
        elif self.done is True:
            if self.t_type == "daily":
                self.master.master.master.master.inc_karma(-300)
            else:
                self.master.master.master.master.inc_karma(-300)
            self.done = False


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


class AlarmListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(
            master,
            width=298,
            height=380,
            label_text="Alarms",
            label_font=master.master.master.app_font,
            label_fg_color=("gray70", "gray35"),
        )
        self.grid_columnconfigure(0, weight=1)
        self.row_count = 0
        self.alarms = {}

    def add_new_alarm_to_frame(self, alarm_time):
        alarm_id = str(uuid.uuid4())
        new_alarm = AlarmFrame(
            self,
            alarm_id=alarm_id,
            alarm_time=alarm_time,
            alarm_mode="off",
            rem_msg="",
            rem_on=False,
        )
        new_alarm.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.alarms[alarm_id] = new_alarm
        self.row_count += 1

    def load_alarm_to_frame(self, alarm_id, alarm_time, alarm_mode):
        new_alarm = AlarmFrame(
            self,
            alarm_id=alarm_id,
            alarm_time=alarm_time,
            alarm_mode=alarm_mode,
            rem_msg="",
            rem_on=False,
        )
        new_alarm.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="ew")
        if alarm_mode == "on":
            new_alarm.alarm_mode_switch.toggle()
            new_alarm.alarm_mode_switch.toggle()
        self.alarms[alarm_id] = new_alarm
        self.row_count += 1


class AlarmFrame(customtkinter.CTkFrame):
    def __init__(self, master, alarm_id, alarm_time, alarm_mode, rem_msg, rem_on):
        super().__init__(master, fg_color=("gray90", "gray27"))
        self.grid_columnconfigure(0, weight=1)
        self.alarm_id = alarm_id
        self.alarm_time = alarm_time
        self.rem_msg = rem_msg
        self.rem_on = rem_on

        self.alarm_mode_switch_var = customtkinter.StringVar(value=alarm_mode)
        self.alarm_mode_switch = customtkinter.CTkSwitch(
            self,
            text="",
            variable=self.alarm_mode_switch_var,
            onvalue="on",
            offvalue="off",
            command=self.alarm,
        )
        self.alarm_mode_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.alarm_time_label = customtkinter.CTkLabel(
            self, text=self.alarm_time, font=("Century Gothic", 15, "bold")
        )
        self.alarm_time_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.delete_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/delete_96.png"), size=(25, 25)
        )
        self.alarm_del_button = customtkinter.CTkButton(
            self,
            text="",
            command=self.del_alarm,
            width=10,
            image=self.delete_icon,
            fg_color="transparent",
            hover_color=("gray82", "gray40"),
        )
        self.alarm_del_button.grid(row=0, column=2, padx=(46, 10), pady=10, sticky="e")

        self.alarm_msg = Notification(
            app_id="Memoboard",
            title="Alarm",
            msg="Time is up!\nIt's " + self.alarm_time,
            duration="long",
            icon=app_path + "/icons/memory_64.png",
        )
        self.alarm_msg.set_audio(audio.Reminder, loop=False)
        self.reminder_msg = Notification(
            app_id="Memoboard",
            title="Exercise Time!",
            msg=self.rem_msg,
            duration="long",
            icon=app_path + "/icons/memory_64.png",
        )
        self.reminder_msg.set_audio(audio.Reminder, loop=False)

    def del_alarm(self):
        self.master.alarms.pop(self.alarm_id)
        self.destroy()

    def alarm(self):
        real_time = None
        if self.rem_on is True:
            real_time = self.master.master.master.master.current_time
        else:
            real_time = self.master.master.master.master.master.master.current_time
        real_time_str = str(real_time.time().replace(microsecond=0))
        real_time_delay = real_time + timedelta(seconds=1)
        real_time_delay_str = str(real_time_delay.time().replace(microsecond=0))
        if self.alarm_time in (real_time_str, real_time_delay_str):
            if self.rem_on is True:
                self.master.master.master.master.exercise_frame.ex_label.configure(
                    text=self.rem_msg, fg_color=("gray90", "gray27")
                )
                self.master.master.master.master.exercise_frame.reminder = False
                self.reminder_msg.show()
                self.alarm_mode_switch.deselect()
                self.master.master.master.master.exercise_frame.reminder_switch.toggle()
            else:
                self.alarm_msg.show()
                self.alarm_mode_switch.deselect()
        if self.alarm_mode_switch.get() == "on":
            self.after(1000, self.alarm)


class ExerciseFrame(customtkinter.CTkFrame):
    def __init__(self, master, font):
        super().__init__(master)
        self.master = master
        self.exercise = None
        self.reminder = False
        self.reminder_alarm = None
        self.chosen_time = "none"
        self.exercises = [
            [[2, 5, 10], "min", "meditation"],
            [[10, 20, 30], "", "push ups"],
            [[5, 10, 15], "", "pull ups"],
            [[30, 60, 90], "sec", "Mabu"],
        ]

        self.ex_label = customtkinter.CTkLabel(
            self,
            text="Random Exercise",
            fg_color=("gray70", "gray35"),
            width=300,
            corner_radius=6,
            font=font,
        )
        self.ex_label.grid(
            row=0, column=0, padx=6, pady=(6, 0), sticky="ew", columnspan=2
        )

        self.reminder_switch_var = customtkinter.StringVar(value="off")
        self.reminder_switch = customtkinter.CTkSwitch(
            self,
            text="Reminder",
            font=("Century Gothic", 15, "bold"),
            onvalue="on",
            offvalue="off",
            variable=self.reminder_switch_var,
            command=self.set_reminder,
            state="disabled",
        )
        self.reminder_switch.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.reminder_menu_var = customtkinter.StringVar(value="none")
        self.reminder_menu = customtkinter.CTkOptionMenu(
            self,
            values=["none", "15 min", "30 min", "60 min", "90 min", "120 min"],
            variable=self.reminder_menu_var,
            dynamic_resizing=True,
            width=100,
            font=("Century Gothic", 15),
            command=self.block_reminder,
        )
        self.reminder_menu.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.ex_button = customtkinter.CTkButton(
            self, text="Generate Exercise", command=self.get_random_exercise, font=font
        )
        self.ex_button.grid(
            row=3, column=0, padx=10, pady=10, sticky="sew", columnspan=2
        )

        self.ex_label = customtkinter.CTkLabel(
            self, text="", fg_color=("gray90", "gray27")
        )
        self.ex_label.grid(
            row=2, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def get_random_exercise(self):
        exercise_list = self.exercises[random.randint(0, len(self.exercises) - 1)]
        amount = str(exercise_list[0][random.randint(0, len(exercise_list[0]) - 1)])
        unit = exercise_list[1]
        exercise_name = exercise_list[2]
        self.exercise = f"{amount} {unit} {exercise_name}"

        if self.reminder is False:
            self.ex_label.configure(text=self.exercise, fg_color=("gray90", "gray27"))
        else:
            pass

    def set_reminder(self):
        if self.reminder_switch_var.get() == "on":
            self.reminder_menu.configure(state="disabled")
            self.chosen_time = self.reminder_menu_var.get()
            self.reminder = True
            self.get_random_exercise()
            chosen_time_str = self.chosen_time.split()[0]
            current_time = self.master.master.master.current_time
            reminder_time = current_time + timedelta(minutes=int(chosen_time_str))
            reminder_time_str = str(reminder_time.time().replace(microsecond=0))
            self.reminder_alarm = AlarmFrame(
                self,
                alarm_id=0,
                alarm_time=reminder_time_str,
                alarm_mode="off",
                rem_msg=self.exercise,
                rem_on=True,
            )
            self.reminder_alarm.alarm_mode_switch.toggle()
        else:
            self.reminder = False
            self.reminder_menu.configure(state="normal")
            self.reminder_alarm.destroy()

    def block_reminder(self, value):
        self.chosen_time = value
        if self.chosen_time == "none":
            self.reminder_switch.configure(state="disabled")
        else:
            self.reminder_switch.configure(state="normal")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Main window properties and layout settings
        self.title("Memoboard")
        self.window_width = 780
        self.window_height = 620
        self.minsize(self.window_width, self.window_height)
        self.maxsize(self.window_width, self.window_height)
        self.iconbitmap("./icons/memory_32.ico")
        self.app_font = customtkinter.CTkFont("Century Gothic", 15, "bold")
        self.current_date = date.today()
        self.current_time = datetime.now()
        self.day_check = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.f_width = self.winfo_width() / 2
        self.f_height = self.winfo_height() / 2
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.pos_y = int(self.screen_height / 2 - self.window_height / 2)
        self.pos_x = int(self.screen_width / 2 - self.window_width / 2)
        self.geometry(
            f"{self.window_width}x{self.window_height}+{self.pos_x}+{self.pos_y}"
        )

        self.navbar_frame = NavbarFrame(self)
        self.navbar_frame.grid(row=0, column=0, sticky="ew", columnspan=2)

        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.tab_view.add("Tasks")
        self.tab_view.add("Ideas")
        self.tab_view.add("Timer")
        self.tab_view.tab("Tasks").grid_columnconfigure((0, 1), weight=1)
        self.tab_view.tab("Tasks").grid_rowconfigure(1, weight=1)

        self.input_clue = customtkinter.CTkLabel(
            self.tab_view.tab("Timer"),
            text="",
            font=("Century Gothic", 15, "bold"),
            text_color=("black", "white"),
            fg_color="transparent",
            corner_radius=10,
            pady=5,
        )
        self.input_clue.grid(row=0, column=0, sticky="n", pady=20)
        self.time_frame = TimeFrame(self.tab_view.tab("Timer"))
        self.time_frame.grid(row=0, column=0, sticky="n", pady=(70, 10))
        self.alarm_list = AlarmListFrame(self.tab_view.tab("Timer"))
        self.alarm_list.grid(
            row=0, column=1, sticky="n", padx=0, pady=(70, 10), rowspan=2
        )
        self.tab_view.tab("Timer").grid_columnconfigure((0, 1), weight=1)

        self.exercise_frame = ExerciseFrame(self.tab_view.tab("Timer"), self.app_font)
        self.exercise_frame.grid(row=1, column=0, sticky="ns", pady=(0, 10))

        self.tab_view.columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(
            self.tab_view.tab("Ideas"),
            font=("Century Gothic", 32),
            fg_color=("white", "gray10"),
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", columnspan=2)

        self.delete_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/clean_90.png"), size=(25, 25)
        )
        self.clear_button = customtkinter.CTkButton(
            self.tab_view.tab("Ideas"),
            command=self.clear_textbox,
            text="",
            image=self.delete_icon,
            width=50,
            font=self.app_font,
        )
        self.clear_button.grid(row=0, column=1, sticky="e", pady=(0, 5))

        self.font_size_var = customtkinter.StringVar(value="medium")
        self.font_size_textbox = customtkinter.CTkOptionMenu(
            self.tab_view.tab("Ideas"),
            values=["small", "medium", "large"],
            variable=self.font_size_var,
            dynamic_resizing=True,
            width=100,
            command=self.set_font_size,
            font=("Century Gothic", 15),
        )
        self.font_size_textbox.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.tab_view.tab("Ideas").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Ideas").grid_rowconfigure(1, weight=1)

        # individual frames with checkboxes for daily and optional tasks
        self.checkbox_frame1 = TaskListFrame(
            self.tab_view.tab("Tasks"),
            "Daily",
            width=self.f_width,
            height=self.f_height,
        )
        self.checkbox_frame1.configure(
            label_text="Daily",
            label_font=self.app_font,
            label_fg_color=("gray70", "gray35"),
        )
        self.checkbox_frame1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_frame2 = TaskListFrame(
            self.tab_view.tab("Tasks"),
            "Optional",
            width=self.f_width,
            height=self.f_height,
        )
        self.checkbox_frame2.configure(
            label_text="To-Do",
            label_font=self.app_font,
            label_fg_color=("gray70", "gray35"),
        )
        self.checkbox_frame2.grid(
            row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew"
        )

        # Text field with button to add a new (optional) task
        self.new_task_frame = TaskInputFrame(self.tab_view.tab("Tasks"))
        self.new_task_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

    def add_new_task(self):
        task, t_type = self.new_task_frame.get_new_task()
        if task == "NOTHING_CHOSEN":
            # Hint to choose an option
            pass
        elif task == "NO_TASK":
            # Hint to enter a new task
            pass
        else:
            if t_type == "daily":
                self.checkbox_frame1.add_new_task_to_frame(task, t_type)
            else:
                self.checkbox_frame2.add_new_task_to_frame(task, t_type)

    def inc_karma(self, karma):
        self.navbar_frame.update_karma(karma)

    def clear_textbox(self):
        self.tab_view.focus_set()
        self.textbox.delete(0.0, "end")

    def set_font_size(self, value):
        if value == "small":
            self.textbox.configure(font=("Century Gothic", 24))
        elif value == "medium":
            self.textbox.configure(font=("Century Gothic", 32))
        else:
            self.textbox.configure(font=("Century Gothic", 42))

    def save_data(self):
        tasks_daily = self.checkbox_frame1.tasks
        tasks_optional = self.checkbox_frame2.tasks
        alarms = self.alarm_list.alarms
        alarm_list = []

        karma_score = self.navbar_frame.karma_counter
        switch_mode = self.navbar_frame.mode_switch_var.get()
        day_end_time = self.navbar_frame.end_of_day_var.get()
        tasks_daily_list = []
        tasks_optional_list = []
        ideas_text = self.textbox.get(0.0, "end").strip("\n")

        def create_task_dict(tasks, task_list):
            for task in tasks.values():
                task_dict = {}
                task_dict["name"] = task.task
                task_dict["type"] = task.t_type
                task_dict["id"] = task.t_id
                task_dict["done"] = task.done
                task_dict["checked"] = task.checkbox.get()
                task_dict["state"] = task.checkbox.cget("state")
                task_list.append(task_dict)

        create_task_dict(tasks_daily, tasks_daily_list)
        create_task_dict(tasks_optional, tasks_optional_list)

        def create_alarm_dict(alarms, alarm_list):
            for alarm in alarms.values():
                alarm_dict = {}
                alarm_dict["id"] = alarm.alarm_id
                alarm_dict["time"] = alarm.alarm_time
                alarm_dict["mode"] = alarm.alarm_mode_switch_var.get()
                alarm_list.append(alarm_dict)

        create_alarm_dict(alarms, alarm_list)

        data_dict = {}
        data_dict["karma"] = karma_score
        data_dict["mode"] = switch_mode
        data_dict["day_end_time"] = day_end_time
        data_dict["daily"] = tasks_daily_list
        data_dict["optional"] = tasks_optional_list
        data_dict["ideas"] = ideas_text
        data_dict["ideas_font"] = self.font_size_var.get()
        data_dict["day"] = self.current_date.day
        data_dict["month"] = self.current_date.month
        data_dict["year"] = self.current_date.year
        data_dict["day_end_state"] = TaskListFrame.end_of_day
        data_dict["alarm"] = alarm_list
        data_dict["day_check"] = self.day_check

        data_dict_str = json.dumps(data_dict)

        with open("data.json", "w") as data_json:
            data_json.write(data_dict_str)

    def load_data(self):
        if os.path.isfile(app_path + "/data.json") is False:
            data_dict = {}
            data_dict["karma"] = 0
            data_dict["mode"] = "off"
            data_dict["day_end_time"] = "20:00"
            data_dict["daily"] = []
            data_dict["optional"] = []
            data_dict["ideas"] = ""
            data_dict["ideas_font"] = "medium"
            data_dict["day"] = self.current_date.day
            data_dict["month"] = self.current_date.month
            data_dict["year"] = self.current_date.year
            data_dict["day_end_state"] = TaskListFrame.end_of_day
            data_dict["alarm"] = []
            data_dict["day_check"] = self.day_check

            data_dict_str = json.dumps(data_dict)
            with open("data.json", "w") as data_json:
                data_json.write(data_dict_str)
        with open("data.json", "r") as data_json:
            data_from_json = data_json.read()

        data_converted = json.loads(data_from_json)
        self.navbar_frame.karma_counter = data_converted["karma"]
        self.navbar_frame.karma_counter_label.configure(
            text=f"Karma: {data_converted['karma']} | "
        )
        self.navbar_frame.end_of_day_var.set(data_converted["day_end_time"])

        if data_converted["mode"] == "on":
            self.navbar_frame.mode_switch.toggle()

        def load_tasks(task_list):
            for task in task_list:
                if task_list[0]["type"] == "daily":
                    self.checkbox_frame1.load_task_to_frame(
                        task["name"],
                        task["type"],
                        task["id"],
                        task["done"],
                        task["checked"],
                        task["state"],
                    )
                else:
                    self.checkbox_frame2.load_task_to_frame(
                        task["name"],
                        task["type"],
                        task["id"],
                        task["done"],
                        task["checked"],
                        task["state"],
                    )

        load_tasks(data_converted["daily"])
        load_tasks(data_converted["optional"])
        self.textbox.insert(0.0, data_converted["ideas"])
        self.set_font_size(data_converted["ideas_font"])
        self.font_size_var.set(data_converted["ideas_font"])
        self.current_date = date(
            data_converted["year"], data_converted["month"], data_converted["day"]
        )
        TaskListFrame.end_of_day = data_converted["day_end_state"]

        def load_alarms(alarm_list):
            for alarm in alarm_list:
                self.alarm_list.load_alarm_to_frame(
                    alarm["id"], alarm["time"], alarm["mode"]
                )

        load_alarms(data_converted["alarm"])
        self.day_check = data_converted["day_check"]

        # update karma icon image according to karma score when starting app
        self.navbar_frame.update_karma(0)

    def clock(self):
        self.current_time = datetime.now()
        current_time_str = datetime.now().strftime("%H:%M:%S")
        today = date.today()
        self.after(1000, self.clock)
        set_time = self.navbar_frame.end_of_day_var.get() + ":00"
        hours, mins, secs = int(set_time[:2]), int(set_time[3:5]), 0
        c_hour, c_min, c_sec = (
            int(current_time_str[:2]),
            int(current_time_str[3:5]),
            int(current_time_str[6:8]),
        )
        c_time = time(c_hour, c_min, c_sec)
        set_endtime = time(hours, mins, secs)
        end_day = time(hour=23, minute=59, second=59)

        if (set_endtime <= c_time <= end_day) and self.day_check == False:
            self.day_check = True
            self.check_today_karma()
            TaskListFrame.end_of_day = True
        if self.current_date < today:
            self.day_check = False
            self.reset_tasks(today)

    def auto_save(self):
        self.save_data()
        self.after(10000, self.auto_save)

    def reset_tasks(self, today):
        self.notify_about_karma("START")
        for task in self.checkbox_frame1.tasks.values():
            task.checkbox.configure(state="normal")
            if task.checkbox.get() == 1:
                task.checkbox.toggle()
        list_opt_done = []
        for key, task in self.checkbox_frame2.tasks.items():
            task.checkbox.configure(state="normal")
            if task.checkbox.get() == 1:
                list_opt_done.append(key)
                task.destroy()
        for key in list_opt_done:
            self.checkbox_frame2.tasks.pop(key)
        self.navbar_frame.karma_counter = 0
        self.navbar_frame.update_karma(0)
        self.current_date = today
        TaskListFrame.end_of_day = False

    def check_today_karma(self):
        def count_unchecked_tasks(task_list):
            unchecked_tasks = 0
            for task in task_list.tasks.values():
                if task.checkbox.get() == 0:
                    unchecked_tasks += 1
                task.checkbox.configure(state="disabled")
            return unchecked_tasks

        unchecked_daily, unchecked_opt = count_unchecked_tasks(
            self.checkbox_frame1
        ), count_unchecked_tasks(self.checkbox_frame2)

        self.navbar_frame.update_karma(
            (unchecked_daily * -300) + (unchecked_opt * -100)
        )

        self.notify_about_karma("END")

    def notify_about_karma(self, timing):
        if timing == "END":
            karma_alert_msg = Notification(
                app_id="Memoboard",
                title="That's it for today",
                msg=self.navbar_frame.karma_message,
                duration="long",
                icon=self.navbar_frame.icon_path,
            )
        else:
            karma_alert_msg = Notification(
                app_id="Memoboard",
                title="Yesterday",
                msg=f"\nKarma: {self.navbar_frame.karma_counter}",
                duration="long",
                icon=self.navbar_frame.icon_path,
            )
        karma_alert_msg.set_audio(audio.Reminder, loop=False)
        karma_alert_msg.show()


app = App()
app.load_data()
app.clock()
app.auto_save()
app.mainloop()
