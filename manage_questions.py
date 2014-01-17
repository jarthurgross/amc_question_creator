from tkinter import *
from tkinter.filedialog import asksaveasfilename
import os
from amc_question_dialogs import CreateQuestionDialog, EditQuestionDialog
from amcquestion import AMCQuestion

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

    self.output_filename = os.getcwd() + "/amc_questions_output.tex"
    self.save_label = Label(frame, text=self.output_filename)
    self.save_label.grid(row=3, columnspan=3, sticky=W)

    select_file_button = Button(frame, text="Choose file",
      command=self.select_file)
    select_file_button.grid(row=4, column=1, sticky=W)

    save_file_button = Button(frame, text="Save", command=self.save_file)
    save_file_button.grid(row=4, column=2, sticky=W)

  def create_question(self):
    d = CreateQuestionDialog(root)
    if d.new_question:
      questions.append(d.new_question)
      self.refresh_listbox()
      print("Created " + questions[-1].get_label() + ".")

  def edit_question(self):
    selection_tuple = self.question_listbox.curselection()
    # Do nothing if nothing selected.
    if len(selection_tuple) > 0:
      d = EditQuestionDialog(questions[int(selection_tuple[0])], root)
      if d.updated_question:
        questions[int(selection_tuple[0])] = d.updated_question
        self.refresh_listbox()
        print("Edited " + questions[int(selection_tuple[0])].get_label() + ".")

  def delete_question(self):
    selection_tuple = self.question_listbox.curselection()
    # Do nothing if nothing selected.
    if len(selection_tuple) > 0:
      print("Deleted " + questions[int(selection_tuple[0])].get_label() + ".")
      questions.pop(int(selection_tuple[0]))
      self.refresh_listbox()

  def refresh_listbox(self):
    self.question_listbox.delete(0, END)
    for question in questions:
      self.question_listbox.insert(END, question.get_label())

  def select_file(self):
    temp_filename = asksaveasfilename(initialfile=
      "amc_questions_output.tex")
    # Don't change the filename if the method returns an empty string.
    if temp_filename != "":
      self.output_filename = temp_filename
    self.save_label.config(text=self.output_filename)

  def save_file(self):
    questions_string = "% Created with AMC Question Creator"
    for question in questions:
      questions_string += "\n\n\\begin{question}{" + question.get_label() + "}"
      questions_string += "\n  " + question.get_question()
      questions_string += "\n  \\begin{choices}"
      answers = question.get_answers()
      marks = ["correct" if n == question.get_correct() else "wrong" for n in
        range(len(answers))]
      for n in range(len(answers)):
        questions_string += \
          "\n    \\" + marks[n] + "choice{" + answers[n] + "}"
      questions_string += "\n  \\end{choices}"
      questions_string += "\n\\end{question}"
    with open(self.output_filename, 'w') as f:
      f.write(questions_string)
    f.closed
    print("Saved to " + self.output_filename)

questions = []

root = Tk()

app = App(root)

root.mainloop()

