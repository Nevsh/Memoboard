import customtkinter
import random
from datetime import timedelta
from app_frame.timer_frame.alarm_frame import AlarmFrame


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
            self.ex_button.configure(state="disabled")
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
            self.ex_button.configure(state="normal")
            self.reminder_alarm.destroy()

    def block_reminder(self, value):
        self.chosen_time = value
        if self.chosen_time == "none":
            self.reminder_switch.configure(state="disabled")
        else:
            self.reminder_switch.configure(state="normal")
