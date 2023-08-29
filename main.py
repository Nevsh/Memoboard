import customtkinter
import tkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


class TaskInputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)

        self.radio_var = tkinter.StringVar(value="")

        self.radio1 = customtkinter.CTkRadioButton(
            self, text="Daily", variable=self.radio_var, value="daily"
        )
        self.radio1.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")

        self.radio2 = customtkinter.CTkRadioButton(
            self, text="Optional", variable=self.radio_var, value="optional"
        )
        self.radio2.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="w")

        self.task_entry = customtkinter.CTkEntry(
            self, placeholder_text="New (optional) task"
        )
        self.task_entry.grid(
            row=1, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=2
        )

        self.button = customtkinter.CTkButton(
            self, text="Add task", command=master.add_new_task
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


class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values, height, width):
        super().__init__(master, height=height, width=width)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.master = master
        self.checkboxes = []
        self.row_count = 1

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=2
        )

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.row_count += 1
        print(checkbox)

    def add_new_task_to_frame(self, task):
        print(self.row_count, task)
        checkbox = customtkinter.CTkCheckBox(self, text=task)
        checkbox.grid(row=self.row_count, column=0, padx=10, pady=(10, 0), sticky="w")
        checkbox_del_button = customtkinter.CTkButton(
            self, text="X", command=self.master.del_task, width=28
        )
        checkbox_del_button.grid(
            row=self.row_count, column=1, padx=10, pady=(10, 0), sticky="e"
        )
        self.row_count += 1

    def del_task_from_frame(self, task):
        pass


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Main window properties and layout settings
        self.title("Memoboard")
        self.geometry("720x530")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.f_width = self.winfo_width() / 2
        self.f_height = self.winfo_height() / 2

        # individual frames with checkboxes for daily and optional tasks
        self.checkbox_frame1 = CheckboxFrame(
            self,
            "Daily",
            values=["Task 1", "Task 2", "Task 3"],
            width=self.f_width,
            height=self.f_height,
        )
        self.checkbox_frame1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_frame1.grid_propagate(False)
        self.checkbox_frame2 = CheckboxFrame(
            self,
            "Optional",
            values=["Optional task 1", "Optional task 2", "Optional task 3"],
            width=self.f_width,
            height=self.f_height,
        )
        self.checkbox_frame2.grid(
            row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew"
        )
        self.checkbox_frame2.grid_propagate(False)

        # self.checkbox_frame1.configure(fg_color="transparent")
        # self.checkbox_frame2.configure(fg_color="transparent")

        # Text field with button to add a new (optional) task
        self.new_task_frame = TaskInputFrame(self)
        self.new_task_frame.grid(
            row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

    def add_new_task(self):
        task, type = self.new_task_frame.get_new_task()
        if task == "NOTHING_CHOSEN":
            # Hint to choose an option
            print("Nothing chosen")
        elif task == "NO_TASK":
            # Hint to enter a new task
            print("No task")
        else:
            print("ADDING")
            if type == "daily":
                print("ADDED TO DAILY:")
                self.checkbox_frame1.add_new_task_to_frame(task)
            else:
                print("ADDED TO OPTIONAL:")
                self.checkbox_frame2.add_new_task_to_frame(task)

    def del_task(self):
        pass


app = App()
app.mainloop()
