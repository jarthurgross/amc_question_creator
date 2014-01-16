from tkinter import *

class App:

  def __init__(self, master):

    frame = Frame(master)
    frame.pack()

    top_label = Label(frame, text="AMC questions")
    top_label.grid(row=0, columnspan=3)

    new_button = Button(frame, text="New question",
      command=self.create_question)
    new_button.grid(row=1, sticky=W)

    edit_button = Button(frame, text="Edit question",
      command=self.edit_question)
    edit_button.grid(row=1, column=1, sticky=W)

    delete_button = Button(frame, text="Delete question", 
      command=self.delete_question)
    delete_button.grid(row=1, column=2, sticky=W)

    self.question_listbox = Listbox(frame)
    self.question_listbox.grid(row=2, columnspan=3)

  def create_question(self):
    print("Create new question.")

  def edit_question(self):
    print("Edit question.")

  def delete_question(self):
    print("Delete question.")

root = Tk()

app = App(root)

root.mainloop()

