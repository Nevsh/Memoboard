import customtkinter
from PIL import Image
from path import app_path

# icons downloaded from https://icons8.com


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
