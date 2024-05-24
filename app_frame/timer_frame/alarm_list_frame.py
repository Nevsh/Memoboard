import customtkinter
import uuid
from app_frame.timer_frame.alarm_frame import AlarmFrame


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
