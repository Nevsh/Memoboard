import customtkinter
import os
import json
from datetime import date, datetime, time
from winotify import Notification, audio
from PIL import Image

from app_frame.tasks_frame.task_list_frame import TaskListFrame
from app_frame.tasks_frame.task_input_frame import TaskInputFrame
from app_frame.navbar_frame import NavbarFrame
from app_frame.timer_frame.time_frame import TimeFrame
from app_frame.timer_frame.alarm_list_frame import AlarmListFrame
from app_frame.timer_frame.exercise_frame import ExerciseFrame

# icons downloaded from https://icons8.com

from path import app_path

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


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

        # Main window widgets
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

        self.clear_icon = customtkinter.CTkImage(
            Image.open(app_path + "/icons/clean_90.png"), size=(25, 25)
        )
        self.clear_button = customtkinter.CTkButton(
            self.tab_view.tab("Ideas"),
            command=self.clear_textbox,
            text="",
            image=self.clear_icon,
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

    def count_unchecked_tasks(self, task_list):
        unchecked_tasks = 0
        for task in task_list.tasks.values():
            if task.checkbox.get() == 0:
                unchecked_tasks += 1
            task.checkbox.configure(state="disabled")
        return unchecked_tasks

    def check_today_karma(self):
        unchecked_daily, unchecked_opt = self.count_unchecked_tasks(
            self.checkbox_frame1
        ), self.count_unchecked_tasks(self.checkbox_frame2)

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
            karma_calc = self.navbar_frame.karma_counter + (
                self.count_unchecked_tasks(self.checkbox_frame1) * -300
                + self.count_unchecked_tasks(self.checkbox_frame2) * -100
            )
            date_delta = date.today() - self.current_date
            karma_alert_msg = Notification(
                app_id="Memoboard",
                title=(
                    "Yesterday"
                    if date_delta.days == 1
                    else f"{self.current_date.day:02}.{self.current_date.month:02}.{self.current_date.year}"
                ),
                msg=(
                    f"\nKarma: {self.navbar_frame.karma_counter}"
                    if self.day_check
                    else f"\nKarma: {karma_calc}"
                ),
                duration="long",
                icon=self.navbar_frame.icon_path,
            )
        karma_alert_msg.set_audio(audio.Reminder, loop=False)
        karma_alert_msg.show()
