# ver = 2023-12-8-1

from tkinter import *
from constants import *
import filename_methods as fm
import os.path
import tkinter.messagebox
from tkinter import filedialog
from numpy import *
import numpy as np
import soundfile as sf
import sounddevice as sd
from null_io import NullIO
import sys


class FramePlayAudioData:
    # Dependencies: MainWindow communicate with classes that are related to GUI contents and buttons
    # instantiation function. Use root for GUI and refers to main window
    def __init__(self, root_frame, user_entry, session_log):

        self.session_log = session_log
        self.root = root_frame
        self.user_entry = user_entry

        self.csv_filefullname = None
        self.wav_filefullname = None

        ######################################################################
        # GUI Frames
        self.frame = LabelFrame(self.root, width=WINDOW_WIDTH, height=120, padx=30, pady=5, text="Play Audio")
        self.frame.grid_propagate(False)

        # Grids
        # Grid can be called here or from MainWindow
        # self.frame.grid(row=3, column=0, sticky="W", padx=10, pady=0, ipadx=5, ipady=2)

        # Frames
        self.frame_sample_rate = Frame(self.frame, width=WINDOW_WIDTH)
        self.frame_choose_files = Frame(self.frame, width=WINDOW_WIDTH)
        self.frame_buttons = Frame(self.frame, width=WINDOW_WIDTH)
        self.frame_sample_rate.grid(row=0, column=0)
        self.frame_choose_files.grid(row=1, column=0)
        self.frame_buttons.grid(row=2, column=0)

        # Frame Sample Rate
        # Labels
        label_sample_rate = Label(self.frame_sample_rate, text="Sample Rate [sample/sec]", padx=5, pady=5)

        # Sample rate drop list
        self.optionmenu_sample_rate_selected = StringVar(self.frame)
        self.optionmenu_sample_rate_selected.set(SAMPLE_RATE)
        self.optionmenu_sample_rate_list = [p for p in SAMPLE_RATE_LIST]
        self.optionmenu_sample_rate = OptionMenu(self.frame_sample_rate, self.optionmenu_sample_rate_selected,
                                                 *self.optionmenu_sample_rate_list,
                                                 command=self.read_sample_rate_option)

        # Grid
        label_sample_rate.grid(row=0, column=0)
        self.optionmenu_sample_rate.grid(row=0, column=1)

        # Frame Choose File
        # Labels
        self.label_filename_text = StringVar()
        self.label_filename_text.set("--")
        self.label_filename = Label(self.frame_choose_files, textvariable=self.label_filename_text, padx=5, pady=5,
                                    fg='blue')

        # Buttons
        self.button_choose_file = Button(self.frame_choose_files, text="Choose File", command=self.button_choose_file,
                                         pady=3, width=15)

        # Grid
        self.button_choose_file.grid(row=0, column=0, sticky=W)
        self.label_filename.grid(row=0, column=1, sticky=E)

        # Frame Buttons
        # Buttons
        self.button_csv_to_wav = Button(self.frame_buttons, text="CSV to WAV", command=self.start_csv_conversion,
                                        pady=3, width=15)
        self.button_wav_play = Button(self.frame_buttons, text="Play WAV", command=self.wav_file_play,
                                      pady=3, width=15, fg='green')
        self.button_wav_stop = Button(self.frame_buttons, text="Stop WAV", command=self.wav_file_stop,
                                      pady=3, width=15, fg='red')
        self.button_open_folder = Button(self.frame_buttons, text="Open Folder",
                                         command=lambda: self.open_folder(self.user_entry.file_location), pady=3,
                                         width=15)
        self.button_exit = Button(self.frame_buttons, text="Exit", command=self.quit_program, pady=3, width=15, fg='red')

        # Grid
        self.button_csv_to_wav.grid(row=2, column=0)
        self.button_wav_play.grid(row=2, column=1, sticky=W)
        self.button_wav_stop.grid(row=2, column=2, sticky=W)
        self.button_open_folder.grid(row=2, column=3, sticky=W)
        self.button_exit.grid(row=2, column=4, sticky=W)
    ######################################################################

    ######################################################################
    def read_sample_rate_option(self, choice):
        print("::sample rate: ", choice)
        self.user_entry.sample_rate = choice

    def button_choose_file(self):
        # file_type = [('all', '*.*'), ('csv', '*.txt'), ('csv', '*.bin')]
        # file_type = [('csv', '*.csv'), ('wav', '*.wav')]
        file_type = [('all', '*.csv *.wav'), ('csv', '*.csv'), ('wav', '*.wav')]
        filefullname = filedialog.askopenfilename(initialdir=self.user_entry.file_location,
                                                  title="Select File", filetypes=file_type, defaultextension=file_type)

        self.user_entry.file_location = os.path.dirname(filefullname)

        file_name = os.path.splitext(os.path.basename(filefullname))[0]
        file_suffix = os.path.splitext(os.path.basename(filefullname))[1]
        file_location = os.path.dirname(filefullname)

        if file_suffix == ".csv":
            self.csv_filefullname = filefullname
            self.wav_filefullname = None
        elif file_suffix == ".wav":
            self.wav_filefullname = filefullname
            self.csv_filefullname = None

        self.label_filename_text.set(filefullname)

    def start_csv_conversion(self):
        self.gui_entry_lock()
        if self.csv_filefullname is None:
            tkinter.messagebox.showerror(title="Load Files", message="No Files Selected")
        elif fm.FileNameMethods.check_filename_exists(self.csv_filefullname) is None:
            tkinter.messagebox.showerror(title="Load Files", message="Files Does Not Exist")
        else:
            message = "Convert .csv to .wav .. sample rate =" + str(self.user_entry.sample_rate) + '\n'
            message_colour = "blue"
            self.session_log.write_textbox(message, message_colour)
            self.wav_filefullname = self.csv_to_wav(self.csv_filefullname, self.user_entry.sample_rate)

        self.gui_entry_unlock()

    @staticmethod
    def csv_to_wav(filefullname, samplerate):
        csv_data = np.loadtxt(filefullname, delimiter=',', dtype=float32)
        csv_data /= np.max(np.abs(csv_data))
        file_root_name = os.path.splitext(filefullname)[0]
        wav_filefullname = str(file_root_name) + ".wav"
        # Single column data will be identified as mono. 2 column data will be stereo
        sf.write(wav_filefullname, csv_data, samplerate)
        return wav_filefullname

    def wav_file_play(self):
        if self.wav_filefullname is None:
            tkinter.messagebox.showerror(title="Load Files", message="No Files Selected")
        elif fm.FileNameMethods.check_filename_exists(self.wav_filefullname) is None:
            tkinter.messagebox.showerror(title="Load Files", message="Files Does Not Exist")
        else:
            data, fs = sf.read(self.wav_filefullname, dtype='float32')
            sd.play(data, fs)

    @staticmethod
    def wav_file_stop():
        sd.stop()

    # Disable user entries in offline mode
    def gui_entry_lock(self):
        NullIO.stop_io()
        self.set_state(self.root, state='disabled')
        # self.set_state(self.frame_buttons, state='disabled')
        # self.set_state(self.frame_choose_files, state='disabled')
        NullIO.resume_io()

    # Enable user entries in offline mode
    def gui_entry_unlock(self):
        NullIO.stop_io()
        self.set_state(self.root, state='normal')
        NullIO.resume_io()

    # def set_state(self, widget, state='disabled'):
    def set_state(self, widget, state):
        print(type(widget))
        try:
            widget.configure(state=state)
        except tkinter.TclError:
            pass
        for child in widget.winfo_children():
            self.set_state(child, state=state)

    def open_folder(self, folder_path):
        temp_path = os.path.realpath(folder_path)
        try:
            os.startfile(temp_path)
        except:
            try:
                os.mkdir(FILE_LOCATION)
                self.user_entry.file_location = FILE_LOCATION
                self.session_log.write_textbox("Folder Created", "blue")
                print("Folder Created")
            except OSError as e:
                print("Failed to Create Folder")
                e = Exception("Failed to Create Folder")
                self.session_log.write_textbox(str(e), "red")
                raise e

    @staticmethod
    def quit_program():
        # quit()  # quit() does not work with pyinstaller, use sys.exit()
        sys.exit()
