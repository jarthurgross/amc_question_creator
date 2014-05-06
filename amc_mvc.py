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
    '''A mutable element of the model that can notify the controller when
    modified
    '''
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


class Test:
    def __init__(self):
        self.string = ""
        self.indent = 0

    def newLine(self, newlines, string):
        self.string += "\n"*newlines + "  "*self.indent + string

    def increaseIndent(self):
        self.indent += 1

    def decreaseIndent(self):
        self.indent = max(0, self.indent - 1)


def sanitizeLaTeX(s):
    chars_to_escape = ['#', '$', '%', '&', '_', '^', '{', '}']
    segments = s.split('\\')
    for n in range(len(segments)):
        for char in chars_to_escape:
            segments[n] = segments[n].replace(char, '\\' + char)
        segments[n] = segments[n].replace('~', '\\textasciitilde{}')
    sanitized = '\\textbackslash{}'.join(segments)

    return sanitized


class Model:
    def __init__(self):
        self.myQuestions = Observable([])
        self.saveFile = Observable(os.getcwd() + "/amc_questions_output.tex")
        self.papertypes = ["letterpaper", "a4paper"]
        self.papertype = self.papertypes[0]

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

    def newLine(newlines, indent, string):
        return "\n"*newlines + "  "*indent + string

    def writeTest(self):
        test = Test()
        test.newLine(0, "%Created with AMC Question Creator")
        papertype = self.papertypes[0]
        test.newLine(1, "\\documentclass[" + papertype + "]{article}")

        test.newLine(2, "\\usepackage[utf8x]{input}")
        test.newLine(1, "\\usepackage[T1]{fontenc}")

        # Select options for the AMC package
        options = ""
        box = True
        completemulti = True
        separateanswersheet = True
        if box:
            options += ",box"
        if completemulti:
            options += ",completemulti"
        if separateanswersheet:
            options += ",separateanswersheet"
        options = options[1:] # Remove leading comma

        test.newLine(2,
            "\\usepackage[" + options + "]{automultiplechoice}")

        test.newLine(2, "\\begin{document}")

        # Imagine this must seed a pseudorandom number generator. Am not
        # randomizing questions right now, so will not use.
        random_seed = ""
        # random_seed = "1237893"
        if len(random_seed) > 0:
            test.newLine(2, indent, "\\AMCrandomseed{" + random_seed + "}")

        # Redefine how questions are defined on answer sheet
        form_question_format = "\\vspace{AMCformVSpace}\\par " + \
            "{\\sc Question #1:} "
        if len(form_question_format) > 0:
            test.newLine(2,
                "\n\n\\def\\AMCformQuestion#1{" + form_question_format + "}")

        copies = 10
        test.newLine(2, "\\onecopy{" + str(copies) + "}{")

        test.newLine(2, "%%% beginning of the test sheet header:")

        title = "QCM"
        test.newLine(2, "\\noindent{\\bf " + sanitizeLaTeX(title) +
            " \\hfill TEST}")

        date = "Mar. 26, 2014"
        test.newLine(2, "\\vspace*{.5cm}")
        test.newLine(1, "\\begin{minipage}{.4\\linewidth}")
        test.increaseIndent()
        test.newLine(1, "\\centering\\large\\bf Test\\\\ Examination on" +
            sanitizeLaTeX(date))
        test.decreaseIndent()
        test.newLine(1, "\\end{minipage}")

        # Write the questions themselves
        questions = self.myQuestions.get()
        for question in questions:
            test.newLine(2, "\\begin{question}{" + question.get_label() + "}")
            test.increaseIndent()
            test.newLine(1, sanitizeLaTeX(question.get_question()))
            test.newLine(1, "\\begin{choices}")
            answers = question.get_answers()
            marks = ["correct" if n == question.get_correct() else "wrong" for
                n in range(len(answers))]
            test.increaseIndent()
            for n in range(len(answers)):
              test.newLine(1, "\\" + marks[n] + "choice{" +
                  sanitizeLaTeX(answers[n]) + "}")
            test.decreaseIndent()
            test.newLine(1, "\\end{choices}")
            test.decreaseIndent()
            test.newLine(1, "\\end{question}")

        return test.string


class View(tk.Toplevel):
    def __init__(self, master, papertypes):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        cur_row = 0

        tk.Label(self, text='AMC questions').grid(row=cur_row, columnspan=3)

        cur_row += 1

        self.paperSize = tk.StringVar(self)
        self.paperSize.set(papertypes[0])
        self.paperOptionMenu = tk.OptionMenu(self, self.paperSize,
            *papertypes)
        self.paperOptionMenu.grid(row=cur_row, column=1, sticky='w')

        cur_row += 1

        self.newButton = tk.Button(self, text="New question")
        self.newButton.grid(row=cur_row, sticky='w')

        self.editButton = tk.Button(self, text="Edit question")
        self.editButton.grid(row=cur_row, column=1, sticky='w')

        self.deleteButton = tk.Button(self, text="Delete question")
        self.deleteButton.grid(row=cur_row, column=2, sticky='w')

        cur_row += 1

        self.questionListbox = tk.Listbox(self)
        self.questionListbox.grid(row=cur_row, columnspan=3)

        cur_row += 1

        self.saveLabel = tk.Label(self)
        self.saveLabel.grid(row=cur_row, columnspan=3, sticky='w')

        cur_row += 1

        self.selectFileButton = tk.Button(self, text="Choose file")
        self.selectFileButton.grid(row=cur_row, column=1, sticky='w')

        self.saveFileButton = tk.Button(self, text="Save")
        self.saveFileButton.grid(row=cur_row, column=2, sticky='w')


    def RefreshQuestions(self, questions):
        self.questionListbox.delete(0, 'end')
        for question in questions:
            self.questionListbox.insert('end', question.get_label())


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myQuestions.addCallback(self.QuestionsChanged)
        self.model.saveFile.addCallback(self.FileChanged)
        self.view = View(root, self.model.papertypes)
        self.ConfigureView()
        self.QuestionsChanged(self.model.myQuestions.get())
        self.FileChanged(self.model.saveFile.get())

    def ConfigureView(self):
        #self.view.paperOptionMenu.config(command=self.UpdatePaperType)
        self.view.newButton.config(command=self.AddQuestion)
        self.view.deleteButton.config(command=self.RemoveQuestion)
        self.view.editButton.config(command=self.EditQuestion)
        self.view.selectFileButton.config(command=self.SelectFile)
        self.view.saveFileButton.config(command=self.SaveFile)
        
    def UpdatePaperType(self, papertype):
        self.model.papertype = papertype

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
        questionsString = self.model.writeTest()
        with open(self.model.saveFile.get(), 'w') as f:
            f.write(questionsString)
        f.closed

    def QuestionsChanged(self, questions):
        self.view.RefreshQuestions(questions)

    def FileChanged(self, filename):
        self.view.saveLabel.config(text=filename)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
