from tkinter import *

class App:

  def __init__(self, master):

    frame = Frame(master)
    frame.pack()

    top_label = Label(frame, text="New AMC question")
    top_label.grid(row=0, columnspan=3)

    self.question_label = StringVar()
    label_label = Label(frame, text="Question label:")
    label_label.grid(row=1, sticky=W)
    label_entry = Entry(frame, textvariable=self.question_label)
    label_entry.grid(row=1, column=1, sticky=W)

    self.question_text = StringVar()
    question_label = Label(frame, text="Question text:")
    question_label.grid(row=2, sticky=W)
    question_entry = Entry(frame, textvariable=self.question_text)
    question_entry.grid(row=2, column=1, sticky=W)

    label_entry.focus_set()

    self.correct_ans = IntVar()
    self.ans_texts = []
    ans_labels = []
    ans_entries = []
    ans_radios = []

    rows_before_ans = 3
    self.answer_count = 4

    for n in range(self.answer_count):
      self.ans_texts.append(StringVar())
      ans_labels.append(Label(frame, text="Answer " + str(n + 1) + ":"))
      ans_labels[n].grid(row=rows_before_ans + n, sticky=W)
      ans_entries.append(Entry(frame, textvariable=self.ans_texts[n]))
      ans_entries[n].grid(row=rows_before_ans + n, column=1, sticky=W)
      ans_radios.append(Radiobutton(frame, variable=self.correct_ans,
        value=n))
      ans_radios[n].grid(row=rows_before_ans + n, column=2, sticky=W)

    write_button = Button(frame, text="Generate question",
      command=self.print_to_terminal)
    write_button.grid(row=rows_before_ans + self.answer_count, columnspan=3)

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

root = Tk()

app = App(root)

root.mainloop()
