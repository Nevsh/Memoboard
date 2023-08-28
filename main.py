import customtkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")


class AddTaskFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)

        self.radio1 = customtkinter.CTkRadioButton(self, text="Daily")
        self.radio1.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
        self.radio2 = customtkinter.CTkRadioButton(self, text="Optional")
        self.radio2.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="w")
        self.task_entry = customtkinter.CTkEntry(
            self, placeholder_text="New (optional) task"
        )
        self.task_entry.grid(
            row=1, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=2
        )
        self.button = customtkinter.CTkButton(
            self, text="Add task", command=master.button_callback
        )
        self.button.grid(
            row=2, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=2
        )


class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
        print(checkbox)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Main window properties and layout settings
        self.title("Memoboard")
        self.geometry("720x360")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # individual frames with checkboxes for daily and optional tasks
        self.checkbox_frame1 = CheckboxFrame(
            self, "Daily", values=["Task 1", "Task 2", "Task 3"]
        )
        self.checkbox_frame1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_frame2 = CheckboxFrame(
            self,
            "Optional",
            values=["Optional task 1", "Optional task 2", "Optional task 3"],
        )
        self.checkbox_frame2.grid(
            row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew"
        )

        self.checkbox_frame1.configure(fg_color="transparent")
        self.checkbox_frame2.configure(fg_color="transparent")

        # Text field with button to add a new (optional) task
        self.new_task_frame = AddTaskFrame(self)
        self.new_task_frame.grid(
            row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

    def button_callback(self):
        print("Added a new Task")


app = App()
app.mainloop()
