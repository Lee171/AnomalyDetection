#! /usr/bin/env python
#  -*- coding: utf-8 -*-

'''
Anomaly Detection of GPS Spoofing Attacks on UAVs
Authors: Lior Pizman & Yehuda Pashay
GitHub: https://github.com/liorpizman/AnomalyDetection
DataSets: 1. ADS-B dataset 2. simulated data
---
Loading window which is part of GUI application
'''

import os
import threading

from tkinter.font import Font, BOLD
from gui.shared.helper_methods import strfdelta
from gui.widgets.animated_gif import AnimatedGif
from datetime import timedelta
from timeit import default_timer as timer
from gui.widgets.hover_button import HoverButton
from gui.widgets.menubar import Menubar
from gui.shared.constants import LOADING_WINDOW_SETTINGS, CROSS_WINDOWS_SETTINGS
from gui.widgets_configurations.helper_methods import set_logo_configuration, set_copyright_configuration, \
    set_widget_to_left, set_button_configuration

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


class LoadingWindow(tk.Frame):
    """
    A Class used to be presented while the models are running in the background of the application

    Methods
    -------
    reset_widgets()
            Description | Reset check bar values

    back_window()
            Description | Handle a click on back button

    stop_model_process()
            Description | Handle a click on stop button

    reinitialize()
            Description | Reinitialize frame values and view

    update_clock()
            Description | Updates the time on the clock

    loading_process()
            Description | Run chosen models and move to results window

    show_model_process_label(y_coordinate, algorithm):
            Description | Show model process label on the screen
    """

    def __init__(self, parent, controller):

        """
        Parameters
        ----------

        :param parent: window
        :param controller: GUI controller
        """

        tk.Frame.__init__(self, parent)

        # Page init
        self.controller = controller
        self.menubar = Menubar(controller)
        # Disables ability to tear menu bar into own window
        self.controller.option_add('*tearOff', 'FALSE')
        system_logo = CROSS_WINDOWS_SETTINGS.get('LOGO')
        photo_location = os.path.join(system_logo)
        global logo_img
        logo_img = tk.PhotoImage(file=photo_location)

        # Page header
        self.logo_png = tk.Button(self)
        self.logo_png.place(relx=0.28, rely=0.029, height=172, width=300)
        set_logo_configuration(self.logo_png, image=logo_img)

        self.instructions = tk.Label(self)
        self.instructions.place(relx=0.015, rely=0.3, height=32, width=635)
        self.instructions.configure(text='''Creating models and runs them, please wait...''',
                                    font=Font(size=9, weight=BOLD))
        set_widget_to_left(self.instructions)

        # Page body
        loading_gif = LOADING_WINDOW_SETTINGS.get('LOADING_GIF')
        delay_between_frames = LOADING_WINDOW_SETTINGS.get('DELAY_BETWEEN_FRAMES')

        self.title_font = Font(family='Helvetica', size=12, weight="bold")

        self.loading_gif = AnimatedGif(self, loading_gif, delay_between_frames)
        self.loading_gif.place(relx=0.1, rely=0.35, height=330, width=600)

        self.clock_label = tk.Label(self, text="", font=self.title_font)
        self.clock_label.place(relx=0.38, rely=0.7, height=32, width=150)

        # Page footer
        self.stop_button = HoverButton(self, command=self.stop_model_process)
        self.stop_button.place(relx=0.813, rely=0.839, height=25, width=81)
        set_button_configuration(self.stop_button, text='''Stop''')

        self.back_button = HoverButton(self, command=self.back_window)
        self.back_button.place(relx=0.017, rely=0.839, height=25, width=81)
        set_button_configuration(self.back_button, text='''Back''')
        self.back_button.configure(state='disabled')

        self.copyright = tk.Label(self)
        self.copyright.place(relx=0, rely=0.958, height=25, width=750)
        set_copyright_configuration(self.copyright)

        # Page logic
        self.loading_gif.start()

    def reset_widgets(self):
        """
        Reset check bar values
        :return: empty values in the widgets
        """

        pass

    def back_window(self):
        """
        Handle back button click
        :return: previous window
        """

        self.controller.reinitialize_frame("SimilarityFunctionsWindow")

    def stop_model_process(self):
        """
        Handle stop button click
        :return: freeze state
        """

        self.back_button.configure(state='active')
        self.stop_button.configure(state='disabled')
        try:
            self.model_process_thread.join()
        except Exception:
            pass

    def reinitialize(self):
        """
        Reinitialize frame values and view
        :return: new frame view
        """

        self.model_process_thread = threading.Thread(name='model_process', target=self.loading_process)
        self.model_process_thread.start()
        self.start_time = timer()
        self.update_clock()

    def update_clock(self):
        """
        Updates the time on the clock
        :return: updated time
        """

        now = timer()
        duration = timedelta(seconds=now - self.start_time)
        self.clock_label.configure(text=strfdelta(duration, '%H:%M:%S'))
        self.controller.after(200, self.update_clock)

    def loading_process(self):
        """
        Run chosen models and move to results window
        :return: results window
        """

        similarity_score, test_data_path, results_path, new_model_running = self.controller.init_models()

        if new_model_running:
            chosen_algorithms = self.controller.get_algorithms()
        else:
            chosen_algorithms = set(self.controller.get_existing_algorithms().keys())

        y_coordinate = 0.34
        enumerate_details = 0

        for algorithm in chosen_algorithms:
            self.controller.run_models(algorithm, similarity_score, test_data_path, results_path, new_model_running)

            if enumerate_details < 3:
                self.algorithm_process_finished = tk.Label(self)
                self.algorithm_process_finished.place(relx=0.015, rely=y_coordinate, height=22, width=250)
                self.algorithm_process_finished.configure(text='''{0} model already created...'''.format(algorithm))
                set_widget_to_left(self.algorithm_process_finished)

                y_coordinate += 0.04

                self.after(1500, self.show_model_process_label(y_coordinate, algorithm))

                y_coordinate += 0.04

            enumerate_details += 1

        self.controller.reinitialize_frame("ResultsWindow")

    def show_model_process_label(self, y_coordinate, algorithm):
        """
        Show model process label on the screen
        :param y_coordinate: y place coordinate
        :param algorithm: which algorithm to display
        :return: new label
        """

        self.model_process_finished = tk.Label(self)
        self.model_process_finished.place(relx=0.015, rely=y_coordinate, height=22, width=200)
        self.model_process_finished.configure(text='''{0} model is active now...'''.format(algorithm))
        set_widget_to_left(self.model_process_finished)
