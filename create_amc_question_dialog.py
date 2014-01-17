from tkinter import *
import tksimpledialog
from amcquestion import AMCQuestion

class CreateQuestionDialog(tksimpledialog.Dialog):

  def body(self, master):

    top_label = Label(master, text="New AMC question")
    top_label.grid(row=0, columnspan=3)

    self.question_label = StringVar()
    label_label = Label(master, text="Question label:")
    label_label.grid(row=1, sticky=W)
    label_entry = Entry(master, textvariable=self.question_label)
    label_entry.grid(row=1, column=1, sticky=W)

    self.question_text = StringVar()
    question_label = Label(master, text="Question text:")
    question_label.grid(row=2, sticky=W)
    question_entry = Entry(master, textvariable=self.question_text)
    question_entry.grid(row=2, column=1, sticky=W)

    self.correct_ans = IntVar()
    self.ans_texts = []
    ans_labels = []
    ans_entries = []
    ans_radios = []

    rows_before_ans = 3
    self.answer_count = 4

    for n in range(self.answer_count):
      self.ans_texts.append(StringVar())
      ans_labels.append(Label(master, text="Answer " + str(n + 1) + ":"))
      ans_labels[n].grid(row=rows_before_ans + n, sticky=W)
      ans_entries.append(Entry(master, textvariable=self.ans_texts[n]))
      ans_entries[n].grid(row=rows_before_ans + n, column=1, sticky=W)
      ans_radios.append(Radiobutton(master, variable=self.correct_ans,
        value=n))
      ans_radios[n].grid(row=rows_before_ans + n, column=2, sticky=W)

    return label_entry

  def buttonbox(self):
    box = Frame(self)
    write_button = Button(box, text="Generate question",
      command=self.ok)
    write_button.pack()
    box.pack()

  def apply(self):
    self.print_to_terminal()
    label = self.question_label.get()
    question = self.question_text.get()
    answers = [ans_text.get() for ans_text in self.ans_texts]
    correct = self.correct_ans.get()
    self.new_question = AMCQuestion(label, question, answers, correct)

  def print_to_terminal(self):

    print("\\begin{question}{" + self.question_label.get() + "}")
    print("  " + self.question_text.get())
    print("  \\begin{choices}")
    marks = ["correct" if n == self.correct_ans.get() else "wrong" for n in
      range(self.answer_count)]

    for n in range(self.answer_count):
      print("    \\" + marks[n] + "choice{" + self.ans_texts[n].get() + "}")

    print("  \\end{choices}")
    print("\\end{question}")
