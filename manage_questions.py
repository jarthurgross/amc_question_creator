from tkinter import *

class AMCQuestion:

  def __init__(self, label="", question="", answers=[], correct=0):
    self.label = label
    self.question = question
    self.answers = answers
    self.correct = correct

  def get_label(self):
    return self.label

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
    questions.append(AMCQuestion("question " + str(len(questions))))
    self.refresh_listbox()
    print("Create " + questions[-1].get_label() + ".")

  def edit_question(self):
    selection_tuple = self.question_listbox.curselection()
    # Do nothing if nothing selected.
    if len(selection_tuple) > 0:
      print("Edit " + questions[int(selection_tuple[0])].get_label() + ".")

  def delete_question(self):
    selection_tuple = self.question_listbox.curselection()
    # Do nothing if nothing selected.
    if len(selection_tuple) > 0:
      print("Delete " + questions[int(selection_tuple[0])].get_label() + ".")
      questions.pop(int(selection_tuple[0]))
      self.refresh_listbox()

  def refresh_listbox(self):
    self.question_listbox.delete(0, END)
    for question in questions:
      self.question_listbox.insert(END, question.get_label())

questions = []

root = Tk()

app = App(root)

root.mainloop()

