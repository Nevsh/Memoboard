import customtkinter
import uuid
from app_frame.tasks_frame.task_frame import TaskFrame


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
