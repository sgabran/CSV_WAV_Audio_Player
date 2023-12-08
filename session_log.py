ver = 2022-1-8-1

from tkinter import *
from datetime import datetime
import os
import os.path


# Class to give access to select methods in MainWindow class
# Class designator: "fb" for feedback
class SessionLog:
    def __init__(self, user_entry):
        self.user_entry = user_entry
        self.frame = Tk()
        self.frame.title('Session Log')
        # Disable closing the session log window
        self.frame.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.text_box_tag = 1
        self.text_box_tag_IMU_calibrate = 1
        # Counter for entries in text_box
        self.text_box_counter = 1
        self.text_box_counter_IMU_calibrate = 1
        self.text_box = Text(self.frame, height=25, width=90, font=('Arial', 8), spacing3=2, selectbackground='grey', wrap='word', highlightthickness=2)
        self.scroll_bar = Scrollbar(self.frame)
        self.scroll_bar.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=self.scroll_bar.set)
        self.button_log_save = Button(self.frame, text="Save Log", command=self.save_log, height=1, width=15)
        self.button_log_clear = Button(self.frame, text="Clear Log", command=self.clear_textbox, height=1, width=15)
        #######
        self.text_box.grid          (row=0, column=0, sticky=E, columnspan=4)
        self.scroll_bar.grid        (row=0, column=5, sticky=NS)
        self.button_log_save.grid   (row=1, sticky=W, pady=3, padx=(10, 30))
        self.button_log_clear.grid  (row=1, sticky=E, pady=3, padx=(30, 10))
        # Disable resizing the window
        self.frame.resizable(False, False)
        #######
        # self.filesave_location = 'c:/session_log/'
        self.filesave_location = self.user_entry.file_location

    # Write to textbox, include message counter. User must add new line '\n' to message
    def write_textbox(self, message, message_colour):
        tag = str(self.text_box_tag)
        counter = str(self.text_box_counter)
        self.text_box.tag_config(tag, foreground=message_colour)
        self.text_box.insert(END, (counter + ". " + message), tag)
        self.text_box_tag = self.text_box_tag + 1
        self.text_box_counter = self.text_box_counter + 1
        self.text_box.see("end")
        self.frame.update_idletasks()

    # Append to previous textbox, without including message counter
    def write_textbox_append(self, message, message_colour):
        tag = str(self.text_box_tag)
        self.text_box.tag_config(tag, foreground=message_colour)
        self.text_box.insert(END, message, tag)
        self.text_box_tag = self.text_box_tag + 1
        self.text_box.see("end")
        self.frame.update_idletasks()

    # Function that does nothing. Used in frame_sessionlog.protocol()
    def do_nothing(self):
        pass

    # Methods for Session log
    def save_log(self):
        log_text = self.text_box.get("0.0", END)
        now = datetime.now()
        now = now.strftime("%m-%d-%Y, %H.%M.%S")
        file_name = ("Session Log " + str(now) + ".txt")
        if not os.path.isdir(self.filesave_location):
            os.mkdir(self.filesave_location)
        file_address = (self.filesave_location + '/' + file_name)
        text_file = open(file_address, "w")
        n = text_file.write(str(log_text))
        text_file.close()
        message = "Session log saved: " + str(file_address) + '\n'
        message_colour = 'black'
        self.write_textbox(message, message_colour)

    # Clear log from text box
    def clear_textbox(self):
        self.text_box.delete('1.0', END)

    def enable_button_log_save(self):
        self.button_log_save["state"] = ACTIVE

    def enable_button_log_clear(self):
        self.button_log_clear["state"] = ACTIVE

    def disable_button_log_save(self):
        self.button_log_save["state"] = DISABLED

    def disable_button_log_clear(self):
        self.button_log_clear["state"] = DISABLED
