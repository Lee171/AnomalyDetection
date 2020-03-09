import tkinter as tk
import threading

from gui.checkbox import Checkbar
from gui.utils.helper_methods import load_similarity_list


class SimilarityFunctionsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Widgets
        self.similarity_functions_title = tk.Label(self, text="Choose similarity functions",
                                                   font=controller.title_font)

        self.similarity_functions = Checkbar(self, load_similarity_list(), checkCallback=self.set_similarity_score)

        self.back_button = tk.Button(self, text="Back",
                                     command=lambda: controller.show_frame("FeatureSelectionWindow"))

        self.run_button = tk.Button(self, text="Run",
                                    command=self.run_models)

        self.save_model_var = tk.IntVar()
        self.save_model_check_button = tk.Checkbutton(self, text="save model", variable=self.save_model_var,
                                                      command=self.set_saving_model)

        # Layout using grid
        self.similarity_functions_title.grid(row=0, column=2, pady=3)
        self.similarity_functions.grid(row=2, column=2, pady=3)

        self.grid_rowconfigure(13, minsize=100)
        self.back_button.grid(row=50, column=2, pady=3)
        self.run_button.grid(row=50, column=15, pady=3)

        self.save_model_check_button.grid(row=48, column=15, pady=3)

    def set_similarity_score(self):
        similarity_list = set()
        for check, var in zip(self.similarity_functions.get_checks(),
                              self.similarity_functions.get_vars()):
            if var.get():  # show the algorithms options
                similarity_list.add(check.cget("text"))
        self.controller.set_similarity_score(similarity_list)

    def run_models(self):
        the_process = threading.Thread(name='process', target=self.controller.run_models)
        the_process.start()
        self.controller.show_frame("LoadingWindow")

    def set_saving_model(self):
        self.controller.set_saving_model(self.save_model_var.get() == 1)
