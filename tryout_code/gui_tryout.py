# # gui_tryout.py
# #
# # Tryout for the main data collection GUI
#
# # import tkinter as tk
# # from tkinter import font as tkfont
# # import matplotlib.animation as animation
#
# import sys
# import pygame as pg
#
#
# RED_HIGHLIGHT = (240, 50, 50, 100)
#
# pg.init()
# clock = pg.time.Clock()
# screen = pg.display.set_mode((500,500))
# screen_rect = screen.get_rect()
#
# see_through = pg.Surface((100,100)).convert_alpha()
# see_through.fill(RED_HIGHLIGHT)
# see_through_rect = see_through.get_rect(bottomleft=screen_rect.center)
#
#
# while pg.event.poll().type != pg.QUIT:
#     pg.draw.circle(screen, pg.Color("cyan"), screen_rect.center, 50)
#     screen.blit(see_through, see_through_rect)
#     pg.display.update()
#     clock.tick(60)
#
# pg.quit()
# sys.exit()
#
#
# #
# # class MainGUI(tk.Tk):
# #
# #     def __init__(self, *args, **kwargs):
# #         tk.Tk.__init__(self, *args, **kwargs)
# #
# #         self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
# #
# #         # the container is where we'll stack a bunch of frames
# #         # on top of each other, then the one we want visible
# #         # will be raised above the others
# #         container = tk.Frame(self)
# #         container.pack(side="top", fill="both", expand=True)
# #         container.grid_rowconfigure(0, weight=1)
# #         container.grid_columnconfigure(0, weight=1)
# #
# #         self.frames = {}
# #         for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
# #             page_name = F.__name__
# #             frame = F(parent=container, controller=self)
# #             self.frames[page_name] = frame
# #
# #             # put all of the pages in the same location;
# #             # the one on the top of the stacking order
# #             # will be the one that is visible.
# #             frame.grid(row=0, column=0, sticky="nsew")
# #
# #         self.show_frame("StartPage")
# #
# #     def show_frame(self, page_name):
# #         '''Show a frame for the given page name'''
# #         frame = self.frames[page_name]
# #         frame.tkraise()
# #
# #
# # class StartPage(tk.Frame):
# #     # data use form etc.
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         controller.attributes("-fullscreen", True)
# #
# #         label = tk.Label(self, text="(1/6)", font=controller.title_font)
# #         label.grid(column=0, row=0)
# #
# #         button_next = tk.Button(self, text="Next",
# #                             command=lambda: controller.show_frame("PageOne"))
# #         button_exit = tk.Button(self, text="Close",
# #                             command=controller.quit)
# #         button_next.grid(column=10, row=10)
# #         button_exit.grid(column=0, row=10)
# #
# #
# # class PageOne(tk.Frame):
# #     # Start Questionnaire
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         label = tk.Label(self, text="Vragenlijst (2/6)", font=controller.title_font)
# #         label.grid(column=0, row=0, columnspan=2)
# #
# #
# #         label_age = tk.Label(self, text="Hoe oud ben je?")
# #         label_age.grid(column=0, row=2)
# #         age_entry = tk.Entry(self)
# #         age_entry.grid(column=1, row=2)
# #         label_2 = tk.Label(self, text="Hoe oud ben je?")
# #         label_2.grid(column=0, row=3)
# #         two_entry = tk.Entry(self)
# #         two_entry.grid(column=1, row=3)
# #         label_3 = tk.Label(self, text="Hoe oud ben je?")
# #         label_3.grid(column=0, row=4)
# #         three_entry = tk.Entry(self)
# #         three_entry.grid(column=1, row=4)
# #
# #         button = tk.Button(self, text="Next",
# #                            command=lambda: controller.show_frame("PageTwo"))
# #         button.grid(column=3, row=10)
# #
# #
# # class PageTwo(tk.Frame):
# #     # Check EEG data-stream
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         label = tk.Label(self, text="This is page 2", font=controller.title_font)
# #         label.pack(side="top", fill="x", pady=10)
# #         button = tk.Button(self, text="Next",
# #                            command=lambda: controller.show_frame("PageThree"))
# #         button.pack()
# #
# #
# # class PageThree(tk.Frame):
# #     # Determine game difficulty
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         label = tk.Label(self, text="This is page 3", font=controller.title_font)
# #         label.pack(side="top", fill="x", pady=10)
# #         button = tk.Button(self, text="Next",
# #                            command=lambda: controller.show_frame("PageFour"))
# #         button.pack()
# #
# #
# # class PageFour(tk.Frame):
# #     # Actual game
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         label = tk.Label(self, text="This is page 4", font=controller.title_font)
# #         label.pack(side="top", fill="x", pady=10)
# #         button = tk.Button(self, text="Next",
# #                            command=lambda: controller.show_frame("PageFive"))
# #         button.pack()
# #
# #
# # class PageFive(tk.Frame):
# #     # Final questionnaire
# #     def __init__(self, parent, controller):
# #         tk.Frame.__init__(self, parent)
# #         self.controller = controller
# #         label = tk.Label(self, text="This is page 5", font=controller.title_font)
# #         label.pack(side="top", fill="x", pady=10)
# #         button = tk.Button(self, text="Close",
# #                            command=controller.quit)
# #         button.pack()
# #
# #
# # if __name__ == "__main__":
# #     app = MainGUI()
# #     app.mainloop()