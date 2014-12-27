from tkinter import *
from tksimpledialog import Dialog
from amcquestion import AMCQuestion

class EditQuestionDialog(Dialog):

  def __init__(self, current_question, parent, title = None):
    self.updated_question = None
    self.question = current_question
    Dialog.__init__(self, parent, title)

  def body(self, master):

    top_label = Label(master, text="Edit AMC question")
    top_label.grid(row=0, columnspan=3)

    self.question_label = StringVar()
    self.question_label.set(self.question.get_label())
    label_label = Label(master, text="Question label:")
    label_label.grid(row=1, sticky=W)
    label_entry = Entry(master, textvariable=self.question_label)
    label_entry.grid(row=1, column=1, sticky=W)

    self.question_text = StringVar()
    self.question_text.set(self.question.get_question())
    question_label = Label(master, text="Question text:")
    question_label.grid(row=2, sticky=W)
    question_entry = Entry(master, textvariable=self.question_text)
    question_entry.grid(row=2, column=1, sticky=W)

    self.correct_ans = IntVar()
    self.correct_ans.set(self.question.get_correct())
    self.ans_texts = []
    ans_labels = []
    ans_entries = []
    ans_radios = []

    rows_before_ans = 3
    self.answer_count = 4

    for n in range(self.answer_count):
      self.ans_texts.append(StringVar())
      if n < len(self.question.get_answers()):
        self.ans_texts[n].set(self.question.get_answers()[n])
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
    write_button = Button(box, text="Commit changes",
      command=self.ok)
    write_button.pack(side=LEFT, padx=5, pady=5)
    cancel_button = Button(box, text="Cancel", command=self.cancel)
    cancel_button.pack(side=LEFT, padx=5, pady=5)
    box.pack()

  def apply(self):
    label = self.question_label.get()
    question = self.question_text.get()
    answers = [ans_text.get() for ans_text in self.ans_texts]
    correct = self.correct_ans.get()
    self.updated_question = AMCQuestion(label, question, answers, correct)


class CreateQuestionDialog(Dialog):

  def __init__(self, parent, title = None):
    self.new_question = None
    Dialog.__init__(self, parent, title)

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

    # Set the focus on the label Entry box
    return label_entry

  def buttonbox(self):
    box = Frame(self)
    write_button = Button(box, text="Generate question",
      command=self.ok, default='active')
    write_button.pack(side=LEFT, padx=5, pady=5)
    cancel_button = Button(box, text="Cancel", command=self.cancel)
    cancel_button.pack(side=LEFT, padx=5, pady=5)

    self.bind("<Return>", self.ok)
    self.bind("<Escape>", self.cancel)

    box.pack()

  def apply(self):
    label = self.question_label.get()
    question = self.question_text.get()
    answers = [ans_text.get() for ans_text in self.ans_texts]
    correct = self.correct_ans.get()
    self.new_question = AMCQuestion(label, question, answers, correct)

