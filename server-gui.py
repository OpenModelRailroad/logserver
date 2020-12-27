"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import webbrowser
from subprocess import Popen
from sys import stdout, stdin, stderr
from tkinter import *
from tkinter import messagebox

import psutil


class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''

    def __init__(self, text_area):
        self.text_area = text_area


class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''

    def write(self, str):
        self.text_area.insert(END, str)
        self.text_area.see(END)
        self.flush()

    def flush(self):
        pass


class CoreGUI(object):
    server_process = None
    start_button_text = None
    browser = None

    def __init__(self, parent):
        self.parent = parent
        self.server_running = False

        # Console Text Widget
        self.text_box = Text(self.parent, height=16, width=79, wrap='word')
        self.text_box.place(x=5, y=5)
        sys.stdout = StdoutRedirector(self.text_box)

        # Server Start Button
        self.start_button_text = StringVar()
        self.start_button = Button(self.parent, textvariable=self.start_button_text, command=self.start_server, width=10)
        self.start_button_text.set("Start Server")
        self.start_button.place(x=560, y=270)

        # Open Browser Checkbox
        self.checkvar = BooleanVar()
        self.browsercheck = Checkbutton(self.parent, text="Open Browser", variable=self.checkvar, onvalue=True, offvalue=False)
        self.checkvar.set(False)
        self.browsercheck.place(x=5, y=270)

        # Server Port Label
        self.portlabel = Label(self.parent, text="Server Port")
        self.portlabel.place(x=120, y=272)

        # Server Port Textbox
        self.portvar = StringVar()
        self.portvar.set(8000)
        self.portentry = Entry(self.parent, textvariable=self.portvar, width=6)
        self.portentry.place(x=185, y=272)

    def start_server(self):
        if self.server_running:
            answer = messagebox.askquestion("Stop Server?", "Do you really want stop the server?", icon='warning')
            if answer == 'yes':
                self.server_running = False
                self.start_button_text.set("Start Server")
                self.kill_process(self.server_process.pid)
        else:
            self.server_running = True
            self.start_button_text.set("Stop Server")
            self.server_process = Popen("python manage.py runserver 0.0.0.0:" + self.portvar.get(), shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            print(self.checkvar.get())
            if self.checkvar.get():
                self.browser = webbrowser
                self.browser.open("http://127.0.0.1:" + self.portvar.get())

    def kill_process(self, proc_id):
        process = psutil.Process(proc_id)
        for proc in process.children(recursive=True):
            print("stopping process %d" % proc.pid)
            proc.kill()
        try:
            process.kill()
        except psutil.NoSuchProcess:
            pass


if __name__ == '__main__':
    root = Tk()
    root.title("OMRR Logserver GUI")
    root.geometry("648x300")
    root.iconbitmap(os.path.join(os.getcwd(), 'static', 'images', 'omrr-logo.ico'))
    p1 = PhotoImage(file=os.path.join(os.getcwd(), 'static', 'images', 'omrr-logo.png'))
    root.iconphoto(True, p1)
    root.resizable = False
    gui = CoreGUI(root)
    root.mainloop()
