import sys
sys.path.append("..")

from tkinter import filedialog
from tkinter import messagebox

import pygubu.builder.ttkstdwidgets
import pygubu

from crawler import setup_reddit, create_pdf


class RedditCrawlerApp:

    def __init__(self):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        #builder.add_from_file(os.path.join(sys._MEIPASS, 'interface.ui/interface.ui'))
        builder.add_from_file('interface.ui')

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('Toplevel_1')
        self.mainwindow.resizable(False, False)

        # Configure callbacks
        callbacks = {
            'on_download_clicked': self.on_download_clicked,
            'on_radio_hot_clicked': self.on_radio_hot_clicked,
            'on_radio_top_clicked': self.on_radio_top_clicked
        }

        self.on_radio_hot_clicked()

        builder.connect_callbacks(callbacks)

    def run(self):
        self.mainwindow.mainloop()

    # define the function callbacks
    def on_download_clicked(self):
        radio_group_type_strings = ["top", "hot"]
        radio_group_time_strings = ["day", "week", "month", "year", "all"]

        client_id = self.builder.tkvariables['entry_client_id'].get()
        client_secret = self.builder.tkvariables['entry_client_secret'].get()

        subreddit_name = self.builder.tkvariables['entry_subreddit'].get()
        limit = self.builder.tkvariables['entry_limit'].get()

        selection_radio_group_type = self.builder.tkvariables['radio_group_type'].get()
        selection_radio_group_time = self.builder.tkvariables['radio_group_time'].get()

        type_name = radio_group_type_strings[int(selection_radio_group_type)]
        time_name = radio_group_time_strings[int(selection_radio_group_time)]

        if client_id == "" or client_secret == "" or subreddit_name == "" or limit == "":
            messagebox.showinfo("Error", "Please fill out all of the fields above")
        elif not limit.isdigit():
            messagebox.showinfo("Error", 'The field "Number of posts" has to be a number')
        else:
            folder_selected = filedialog.askdirectory()

            reddit = setup_reddit(client_id=client_id, client_secret=client_secret)
            create_pdf(reddit, limit=int(limit), top_time=time_name, type=type_name, subreddit=subreddit_name, output_dir=folder_selected)
            self.mainwindow.destroy()

    def on_radio_hot_clicked(self):

        radio_button_names = ['Radiobutton_Time_Day', 'Radiobutton_Time_Week', 'Radiobutton_Time_Month', 'Radiobutton_Time_Year', 'Radiobutton_Time_All']

        for radio_button_name in radio_button_names:
            radio_button = self.builder.get_object(radio_button_name)

            radio_button.configure(state='disabled')

    def on_radio_top_clicked(self):

        radio_button_names = ['Radiobutton_Time_Day', 'Radiobutton_Time_Week', 'Radiobutton_Time_Month', 'Radiobutton_Time_Year', 'Radiobutton_Time_All']

        for radio_button_name in radio_button_names:
            radio_button = self.builder.get_object(radio_button_name)

            radio_button.configure(state='normal')


if __name__ == '__main__':
    app = RedditCrawlerApp()
    app.run()