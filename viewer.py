import utils

from tkinter.ttk import Button
from tkinter import Tk, Text, BOTH, X, LEFT, BOTTOM, StringVar
from tkinter.ttk import Frame, Label, Entry


class Viewer(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("15 Puzzle Viewer")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)
        label_moves = Label(frame1, text="Moves", width=6)
        label_moves.pack(side=LEFT, padx=5, pady=5)
        entry_moves = Entry(frame1)
        entry_moves.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=BOTH, expand=True, pady=20, padx=5)
        label_table = Label(frame2, text="Table", width=6)
        label_table.pack()
        text_table = Text(frame2)
        text_table.pack(expand=True, fill=BOTH)

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, padx=5, side=BOTTOM, before=frame2)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(3, weight=1)
        quit_button = Button(frame3, text="Quit", command=self.quit)
        quit_button.grid(row=0, column=1)
        next_button = Button(frame3, text="Next", command=self.next)
        next_button.grid(row=0, column=2)

    def next(self):
        self.master.switch_frame(ViewPage)


class ViewPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.pack(fill=BOTH, expand=True)

        self.step = 1
        rows = 4
        columns = 4

        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)
        self.label_moves = Label(self.frame1, text="Step " + str(self.step))
        self.label_moves.pack(expand=True, side=LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(fill=BOTH, expand=True)
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(columns+1, weight=1)

        self.tiles = [[0 for x in range(rows)] for y in range(columns)]
        for row in range(rows):
            for column in range(columns):
                self.tiles[row][column] = Button(self.frame2, text=row*rows+column)
                self.tiles[row][column].grid(row=row, column=column+1)

        self.frame3 = Frame(self)
        self.frame3.pack(fill=BOTH, side=BOTTOM, before=self.frame2)
        self.button_back = Button(self.frame2, text="Back", command=self.back)
        self.button_back.grid(row=rows, column=1)
        self.button_previous = Button(self.frame2, text="Previous step", command=self.previous_step)
        self.button_previous.grid(row=rows, column=2)
        self.button_next = Button(self.frame2, text="Next step", command=self.next_step)
        self.button_next.grid(row=rows, column=3)

    def next_step(self):
        self.step += 1
        self.update_data()

    def previous_step(self):
        if self.step == 1:
            return

        self.step -= 1
        self.update_data()

    def back(self):
        self.master.switch_frame(StartPage)

    def update_data(self):
        self.label_moves.config(text="Step " + str(self.step))



if __name__ == '__main__':
    app = Viewer()
    app.mainloop()
    
    # rows, columns = utils.process_size_input()
    # data = utils.process_table_input(rows, columns)






