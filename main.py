from app_frame.app import App


if __name__ == "__main__":
    app = App()
    app.load_data()
    app.clock()
    app.auto_save()
    app.mainloop()
