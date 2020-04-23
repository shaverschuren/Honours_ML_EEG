from tkinter import *


def ok():
    selected_level = selection.get()

    if selected_level in ["1", "2", "3"]:  # Check whether a level choice has been made
        master.destroy()


def main():
    global master
    global selection

    master = Tk()
    master.geometry("700x300")
    master.title("Level selection")
    selection = StringVar(master)

    label1 = Label(master, text="Selecteer nu a.u.b. het level waarbij je je zelf het prettigst voelt.")
    label2 = Label(master, text="Probeer hierbij als richtlijn een level te kiezen waarbij je met redelijk gemak ongeveer elke 5 seconden een set vindt.")
    label3 = Label(master, text="Klik op de onderstaande knop om een level te kiezen en klik daarna op OK")

    drop_down = OptionMenu(master, selection, "1", "2", "3")

    ok_button = Button(master, text="OK", command=ok)

    label1.pack()
    label2.pack()
    label3.pack()
    drop_down.pack()
    ok_button.pack()

    mainloop()

    return selection.get()


if __name__ == "__main__":
    main()