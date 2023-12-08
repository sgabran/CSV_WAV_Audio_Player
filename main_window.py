from tkinter import *
from user_entry import UserEntry
from session_log import SessionLog
from frame_play_audio_data import FramePlayAudioData


# Class to create GUI
class MainWindow:
    # Dependencies: MainWindow communicate with classes that are related to GUI contents and buttons
    def __init__(self):  # instantiation function. Use root for GUI and refers to main window

        root = Tk()
        root.title("CSV and WAV Audio File Manager")
        self.root_frame = root
        self.user_entry = UserEntry()
        self.session_log = SessionLog(self.user_entry)
        self.frame_play_audio_data = FramePlayAudioData(root, self.user_entry, self.session_log)

        ######################################################################
        # GUI Frames
        self.frame_root_title = Frame(root, highlightthickness=0)
        # Disable resizing the window
        root.resizable(False, False)
        # Grids
        self.frame_play_audio_data.frame.grid(row=3, column=0, sticky="W", padx=10, pady=(5, 10), ipadx=5, ipady=2)
        # Launch GUI
        self.root_frame.mainloop()
        ######################################################################
