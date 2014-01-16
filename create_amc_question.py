from tkinter import *

class App:

  def __init__(self, master):

    frame = Frame(master)
    frame.pack()

    top_label = Label(frame, text="New AMC question")
    top_label.pack()

    label_frame = Frame(frame)
    label_frame.pack()
    self.question_label = StringVar()
    label_label = Label(label_frame, text="Question label")
    label_label.pack(side=LEFT)
    label_entry = Entry(label_frame, textvariable=self.question_label)
    label_entry.pack(side=LEFT)

    question_frame = Frame(frame)
    question_frame.pack()
    self.question_text = StringVar()
    question_label = Label(question_frame, text="Questioni text")
    question_label.pack(side=LEFT)
    question_entry = Entry(question_frame, textvariable=self.question_text)
    question_entry.pack(side=LEFT)

    label_entry.focus_set()

    self.correct_ans = IntVar()
    self.ans_texts = []
    ans_labels = []
    ans_entries = []
    ans_radios = []
    ans_frames = []

    for n in range(4):
      ans_frames.append(Frame(frame))
      ans_frames[n].pack()
      self.ans_texts.append(StringVar())
      ans_labels.append(Label(ans_frames[n], text="Answer " + str(n + 1)))
      ans_labels[n].pack(side=LEFT)
      ans_entries.append(Entry(ans_frames[n], textvariable=self.ans_texts[n]))
      ans_entries[n].pack(side=LEFT)
      ans_radios.append(Radiobutton(ans_frames[n], variable=self.correct_ans,
        value=n))
      ans_radios[n].pack(side=LEFT)

    write_button = Button(frame, text="Generate question",
      command=self.print_to_terminal)
    write_button.pack()

  def print_to_terminal(self):

    print("\\begin{question}{" + self.question_label.get() + "}")
    print("  " + self.question_text.get())
    print("  \\begin{choices}")
    marks = ["correct" if n == self.correct_ans.get() else "wrong" for n in
      range(4)]

    for n in range(4):
      print("    \\" + marks[n] + "choice{" + self.ans_texts[n].get() + "}")

    print("  \\end{choices}")
    print("\\end{question}")

root = Tk()

app = App(root)

root.mainloop()
