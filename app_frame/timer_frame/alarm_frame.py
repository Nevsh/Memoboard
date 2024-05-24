import customtkinter
from datetime import timedelta
from winotify import Notification, audio
from PIL import Image
from path import app_path

# icons downloaded from https://icons8.com


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
