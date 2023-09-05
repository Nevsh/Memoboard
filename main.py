import customtkinter
import tkinter
import os
import uuid
import json
import time as tm
from datetime import date, datetime
from winotify import Notification, audio
from PIL import Image

app_path = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


# class NavbarFrame creates a frame that functions as a navbar
class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=("gray65", "gray40"), corner_radius=0)
        self.master = master
        self.icon_path = app_path + "/Icons/neutral_96.png"
        self.karma_message = "Consistency is everything. Keep going."
        self.karma_icon_neutral = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/neutral_96.png"), size=(32, 32)
        )
        self.karma_icon_bad_3 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/bad_3_96.png"), size=(32, 32)
        )
        self.karma_icon_bad_2 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/bad_2_96.png"), size=(32, 32)
        )
        self.karma_icon_bad_1 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/bad_1_96.png"), size=(32, 32)
        )
        self.karma_icon_good_1 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/good_1_96.png"), size=(32, 32)
        )
        self.karma_icon_good_2 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/good_2_96.png"), size=(32, 32)
        )
        self.karma_icon_good_3 = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/good_3_96.png"), size=(32, 32)
        )
        self.karma_counter = 0
        self.karma_label = customtkinter.CTkLabel(
            self,
            text="Karma: ",
            font=master.app_font,
            text_color=("white"),
        )
        self.karma_label.grid(row=0, column=4, padx=(10, 90), pady=10, sticky="e")
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
            Image.open(app_path + "/Icons/light_96.png"), size=(28, 28)
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
            Image.open(app_path + "/Icons/save_96.png"), size=(28, 28)
        )
        # self.save_button = customtkinter.CTkButton(
        #     self,
        #     text="",
        #     width=10,
        #     command=master.save_data,
        #     image=self.save_icon,
        #     fg_color=("gray76", "gray54"),
        #     hover_color=("gray88", "gray64"),
        #     border_spacing=0,
        # )
        # self.save_button.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        self.end_of_day_icon = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/dusk_96.png"), size=(30, 30)
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
                "00:00",
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
        print(self.karma_counter)
        print(self.karma_counter in range(-1, -501))
        self.karma_counter_label.configure(text=f"{self.karma_counter} | ")
        if self.karma_counter in range(1, 1500):
            self.karma_counter_label.configure(image=self.karma_icon_good_1)
            self.icon_path = app_path + "/Icons/good_1_96.png"
            self.karma_message = "Good work! :)"
        elif self.karma_counter in range(1500, 3000):
            self.karma_counter_label.configure(image=self.karma_icon_good_2)
            self.icon_path = app_path + "/Icons/good_2_96.png"
            self.karma_message = "Great day, keep it that way. ;)"
        elif self.karma_counter >= 3000:
            self.karma_counter_label.configure(image=self.karma_icon_good_3)
            self.icon_path = app_path + "/Icons/good_3_96.png"
            self.karma_message = "You're awesome :D The world is yours!"
        elif self.karma_counter in range(-499, 0):
            self.karma_counter_label.configure(image=self.karma_icon_bad_1)
            self.icon_path = app_path + "/Icons/bad_1_96.png"
            self.karma_message = "Don't worry, tomorrow will be better."
        elif self.karma_counter in range(-999, -499):
            self.karma_counter_label.configure(image=self.karma_icon_bad_2)
            self.icon_path = app_path + "/Icons/bad_2_96.png"
            self.karma_message = "Just try to stick to your habits."
        elif self.karma_counter <= -1000:
            self.karma_counter_label.configure(image=self.karma_icon_bad_3)
            self.icon_path = app_path + "/Icons/bad_3_96.png"
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
            text="Optional",
            variable=self.radio_var,
            value="optional",
            font=master.master.master.app_font,
        )
        self.radio2.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="w")

        self.task_entry = customtkinter.CTkEntry(
            self, placeholder_text="New (optional) task", font=("Century Gothic", 13)
        )
        self.task_entry.grid(
            row=1, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=2
        )

        self.button = customtkinter.CTkButton(
            self,
            text="Add task",
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
    def __init__(self, master, title, height, width):
        super().__init__(master, height=height, width=width)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.master = master
        self.checkboxes = []
        self.row_count = 1
        self.task_list_frame_karma = 0
        self.tasks = {}

        # self.title = customtkinter.CTkLabel(
        #     self,
        #     text=self.title,
        #     fg_color=("gray70", "gray35"),
        #     corner_radius=6,
        #     font=master.master.master.app_font,
        # )
        # self.title.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="ew")

    def add_new_task_to_frame(self, task, t_type):
        task_id = str(uuid.uuid4())
        new_task = TaskFrame(self, task, t_type, t_id=task_id)
        new_task.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.tasks[task_id] = new_task
        self.row_count += 1

    def load_task_to_frame(self, task, t_type, t_id, t_done, t_checked):
        new_task = TaskFrame(self, task, t_type, t_id=t_id)
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
    def __init__(self, master, task, t_type, t_id):
        super().__init__(master, fg_color=("gray90", "gray27"))
        self.grid_columnconfigure(0, weight=1)
        self.master = master
        self.done = False
        self.task = task
        self.t_type = t_type
        self.t_id = t_id

        self.delete_icon = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/delete_96.png"), size=(25, 25)
        )
        self.checkbox = customtkinter.CTkCheckBox(
            self, text=task, command=self.task_done, font=("Century Gothic", 13)
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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Main window properties and layout settings
        self.title("Memoboard")
        self.geometry("780x620")
        self.iconbitmap("./Icons/memory_64.ico")
        self.app_font = customtkinter.CTkFont("Century Gothic", 15, "bold")
        self.alert_msg = Notification(
            app_id="Memoboard",
            title="Feierabend",
            msg="Gute Arbeit. Lass den Tag ausklingen.",
            duration="long",
            icon=app_path + "/Icons/memory_64.png",
        )
        self.alert_msg.set_audio(audio.Reminder, loop=False)
        self.current_date = date.today()
        self.tmr_date = date(2023, 9, 5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.f_width = self.winfo_width() / 2
        self.f_height = self.winfo_height() / 2

        self.navbar_frame = NavbarFrame(self)
        self.navbar_frame.grid(row=0, column=0, sticky="ew", columnspan=2)

        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.tab_view.add("Tasks")
        self.tab_view.add("Ideas")
        self.tab_view.tab("Tasks").grid_columnconfigure((0, 1), weight=1)
        self.tab_view.tab("Tasks").grid_rowconfigure(1, weight=1)

        self.textbox = customtkinter.CTkTextbox(
            self.tab_view.tab("Ideas"),
            font=("Century Gothic", 32),
            fg_color=("white", "gray10"),
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", columnspan=2)

        self.delete_icon = customtkinter.CTkImage(
            Image.open(app_path + "/Icons/delete_96.png"), size=(25, 25)
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
        # self.checkbox_frame1.grid_propagate(False)
        self.checkbox_frame2 = TaskListFrame(
            self.tab_view.tab("Tasks"),
            "Optional",
            width=self.f_width,
            height=self.f_height,
        )
        self.checkbox_frame2.configure(
            label_text="Optional",
            label_font=self.app_font,
            label_fg_color=("gray70", "gray35"),
        )
        self.checkbox_frame2.grid(
            row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew"
        )
        # self.checkbox_frame2.grid_propagate(False)

        # self.checkbox_frame1.configure(fg_color="transparent")
        # self.checkbox_frame2.configure(fg_color="transparent")

        # Text field with button to add a new (optional) task
        self.new_task_frame = TaskInputFrame(self.tab_view.tab("Tasks"))
        self.new_task_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

    # test method
    # def set_tmr(self):
    #     tm.sleep(5.0)
    #     self.tmr_date = date(2023, 9, 6)

    def add_new_task(self):
        task, t_type = self.new_task_frame.get_new_task()
        if task == "NOTHING_CHOSEN":
            # Hint to choose an option
            # self.set_tmr()
            print("Nothing chosen")
        elif task == "NO_TASK":
            # Hint to enter a new task
            print("No task")
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

        karma_score = self.navbar_frame.karma_counter
        switch_mode = self.navbar_frame.mode_switch_var.get()
        day_end = self.navbar_frame.end_of_day_var.get()
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
                task_list.append(task_dict)

        create_task_dict(tasks_daily, tasks_daily_list)
        create_task_dict(tasks_optional, tasks_optional_list)

        data_dict = {}
        data_dict["karma"] = karma_score
        data_dict["mode"] = switch_mode
        data_dict["day_end"] = day_end
        data_dict["daily"] = tasks_daily_list
        data_dict["optional"] = tasks_optional_list
        data_dict["ideas"] = ideas_text
        data_dict["ideas_font"] = self.font_size_var.get()
        data_dict["day"] = self.current_date.day
        data_dict["month"] = self.current_date.month
        data_dict["year"] = self.current_date.year

        data_dict_str = json.dumps(data_dict)

        with open("data.json", "w") as data_json:
            data_json.write(data_dict_str)

    def load_data(self):
        with open("data.json", "r") as data_json:
            data_from_json = data_json.read()

        data_converted = json.loads(data_from_json)
        self.navbar_frame.karma_counter = data_converted["karma"]
        self.navbar_frame.karma_counter_label.configure(
            text=f"Karma: {data_converted['karma']} | "
        )
        self.navbar_frame.end_of_day_var.set(data_converted["day_end"])

        if data_converted["mode"] == "on":
            self.navbar_frame.mode_switch.toggle()

        def load_tasks(tasks_list):
            for task in tasks_list:
                if tasks_list[0]["type"] == "daily":
                    self.checkbox_frame1.load_task_to_frame(
                        task["name"],
                        task["type"],
                        task["id"],
                        task["done"],
                        task["checked"],
                    )
                else:
                    self.checkbox_frame2.load_task_to_frame(
                        task["name"],
                        task["type"],
                        task["id"],
                        task["done"],
                        task["checked"],
                    )

        load_tasks(data_converted["daily"])
        load_tasks(data_converted["optional"])
        self.textbox.insert(0.0, data_converted["ideas"])
        self.set_font_size(data_converted["ideas_font"])
        self.font_size_var.set(data_converted["ideas_font"])
        self.current_date = date(
            data_converted["year"], data_converted["month"], data_converted["day"]
        )
        # update karma icon image according to karma score when starting app
        self.navbar_frame.update_karma(0)

    def clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        today = date.today()
        self.after(1000, self.clock)
        set_time = self.navbar_frame.end_of_day_var.get() + ":00"

        if current_time == set_time:
            self.check_today_karma()
        if self.current_date < today:
            self.reset_tasks(today)

    def auto_save(self):
        self.save_data()
        self.after(10000, self.auto_save)

    def reset_tasks(self, today):
        for task in self.checkbox_frame1.tasks.values():
            if task.checkbox.get() == 1:
                task.checkbox.toggle()
        list_opt_done = []
        # print(self.checkbox_frame2.tasks)
        for key, task in self.checkbox_frame2.tasks.items():
            if task.checkbox.get() == 1:
                list_opt_done.append(key)
                task.destroy()
        for key in list_opt_done:
            self.checkbox_frame2.tasks.pop(key)
        # print(self.checkbox_frame2.tasks)
        self.navbar_frame.karma_counter = 0
        self.navbar_frame.update_karma(0)
        self.current_date = today

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

        karma_alert_msg = Notification(
            app_id="Memoboard",
            title="Feierabend",
            msg=self.navbar_frame.karma_message,
            duration="long",
            icon=self.navbar_frame.icon_path,
        )
        karma_alert_msg.set_audio(audio.Reminder, loop=False)
        karma_alert_msg.show()


app = App()
# check if data.json initially exists
app.load_data()
app.clock()
app.auto_save()
app.mainloop()
