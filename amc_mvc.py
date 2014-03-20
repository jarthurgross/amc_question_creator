##Some points to mention...
##
##The model knows nothing about the view or the controller.
##The view knows nothing about the controller or the model.
##The controller understands both the model and the view.
##
##The model uses observables, essentially when important data is changed,
##any interested listener gets notified through a callback mechanism.
##
##The following opens up two windows, one that reports how much money you
##have, and one that has two buttons, one to add money and one to remove
##money.
##
##The important thing is that the controller is set up to monitor changes
##in the model.  In this case the controller notices that you clicked a
##button and modifies the money in the model which then sends out a
##message that it has changed.  The controller notices this and updates
##the widgets.
##
##The cool thing is that anything modifying the model will notify the
##controller.  In this case it is the controller modifying the model, but it
##could be anything else, even another controller off in the distance
##looking at something else.
##
##The main idea is that you give a controller the model and view that it
##needs, but the model's can be shared between controllers so that when
##the model is updated, all associated views are updated. -Brian Kelley
##
## following is a Tkinter approximation of the original example.

import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import os
from tksimpledialog import Dialog
from amcquestion import AMCQuestion
from amc_question_dialogs import CreateQuestionDialog, EditQuestionDialog


class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
             func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class Model:
    def __init__(self):
        self.myQuestions = Observable([])
        self.saveFile = Observable(os.getcwd() + "/amc_questions_output.tex")

    def addQuestion(self, question):
        self.myQuestions.set(self.myQuestions.get() +
            [question])

    def removeQuestion(self, index):
        questions = self.myQuestions.get()
        del questions[index]
        self.myQuestions.set(questions)

    def changeQuestion(self, index, question):
        questions = self.myQuestions.get()
        questions[index] = question
        self.myQuestions.set(questions)

    def setFile(self, filename):
        self.saveFile.set(filename)


class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        tk.Label(self, text='AMC questions').grid(row=0, columnspan=3)

        self.newButton = tk.Button(self, text="New question")
        self.newButton.grid(row=1, sticky='w')

        self.editButton = tk.Button(self, text="Edit question")
        self.editButton.grid(row=1, column=1, sticky='w')

        self.deleteButton = tk.Button(self, text="Delete question")
        self.deleteButton.grid(row=1, column=2, sticky='w')

        self.questionListbox = tk.Listbox(self)
        self.questionListbox.grid(row=2, columnspan=3)

        self.saveLabel = tk.Label(self)
        self.saveLabel.grid(row=3, columnspan=3, sticky='w')

        self.selectFileButton = tk.Button(self, text="Choose file")
        self.selectFileButton.grid(row=4, column=1, sticky='w')

        self.saveFileButton = tk.Button(self, text="Save")
        self.saveFileButton.grid(row=4, column=2, sticky='w')


    def RefreshQuestions(self, questions):
        self.questionListbox.delete(0, 'end')
        for question in questions:
            self.questionListbox.insert('end', question.get_label())
        

class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myQuestions.addCallback(self.QuestionsChanged)
        self.model.saveFile.addCallback(self.FileChanged)
        self.view = View(root)
        self.view.newButton.config(command=self.AddQuestion)
        self.view.deleteButton.config(command=self.RemoveQuestion)
        self.view.editButton.config(command=self.EditQuestion)
        self.view.selectFileButton.config(command=self.SelectFile)
        self.view.saveFileButton.config(command=self.SaveFile)
        self.QuestionsChanged(self.model.myQuestions.get())
        self.FileChanged(self.model.saveFile.get())
        
    def AddQuestion(self):
        d = CreateQuestionDialog(self.view, title="Create Question")
        if d.new_question:
            self.model.addQuestion(d.new_question)

    def RemoveQuestion(self):
        selectionTuple = self.view.questionListbox.curselection()
        # Only remove a question when one is selected
        if len(selectionTuple) > 0:
            self.model.removeQuestion(int(selectionTuple[0]))

    def EditQuestion(self):
        selectionTuple = self.view.questionListbox.curselection()
        # Only open edit dialog when a question is selected
        if len(selectionTuple) > 0:
            d = EditQuestionDialog(self.model.myQuestions.get()[int(
                selectionTuple[0])], self.view, title="Edit Question")
            # Only replace the selected question if an edit was committed
            if d.updated_question:
                self.model.changeQuestion(int(selectionTuple[0]),
                    d.updated_question)

    def SelectFile(self):
        filename = asksaveasfilename(initialfile=
            "amc_questions_output.tex")
        if filename != "":
            self.model.setFile(filename)

    def SaveFile(self):
        questionsString = self.WriteTest()
        with open(self.model.saveFile.get(), 'w') as f:
            f.write(questionsString)
        f.closed

    def QuestionsChanged(self, questions):
        self.view.RefreshQuestions(questions)

    def FileChanged(self, filename):
        self.view.saveLabel.config(text=filename)

    def WriteTest(self):
        questions_string = "% Created with AMC Question Creator"
        questions = self.model.myQuestions.get()
        for question in questions:
            questions_string += "\n\n\\begin{question}{" + \
                question.get_label() + "}"
            questions_string += "\n  " + question.get_question()
            questions_string += "\n  \\begin{choices}"
            answers = question.get_answers()
            marks = ["correct" if n == question.get_correct() else "wrong" for
                n in range(len(answers))]
            for n in range(len(answers)):
              questions_string += \
                "\n    \\" + marks[n] + "choice{" + answers[n] + "}"
            questions_string += "\n  \\end{choices}"
            questions_string += "\n\\end{question}"

        return questions_string


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
