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
from tksimpledialog import Dialog
from amcquestion import AMCQuestion

class CreateQuestionDialog(Dialog):

    def __init__(self, parent, title = None):
       Dialog.__init__(self, parent, title)


    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        top_label = tk.Label(master, text="New AMC question")
        top_label.pack(padx=5, pady=5)

#   def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

    #
    # standard button semantics

#   def apply(self):

#       pass # override



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

    def addQuestion(self, value):
        self.myQuestions.set(self.myQuestions.get() +
            [AMCQuestion(label=value)])

    def removeQuestion(self, value):
        questions = self.myQuestions.get()
        del questions[value]
        self.myQuestions.set(questions)


class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        tk.Label(self, text='My Questions').pack(side='left')
        self.questionListbox = tk.Listbox(self)
        self.questionListbox.pack(side='left')

    def RefreshQuestions(self, questions):
        self.questionListbox.delete(0, 'end')
        for question in questions:
            self.questionListbox.insert('end', question.get_label())
        

class ChangerWidget(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.addButton = tk.Button(self, text='Add', width=8)
        self.addButton.pack(side='left')
        self.removeButton = tk.Button(self, text='Remove', width=8)
        self.removeButton.pack(side='left')        


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myQuestions.addCallback(self.QuestionsChanged)
        self.view1 = View(root)
        self.view2 = ChangerWidget(self.view1)
        self.view2.addButton.config(command=self.AddQuestion)
        self.view2.removeButton.config(command=self.RemoveQuestion)
        self.QuestionsChanged(self.model.myQuestions.get())
        
    def AddQuestion(self):
        d = CreateQuestionDialog(self.view2, title="Create Question")
        self.model.addQuestion("Question")

    def RemoveQuestion(self):
        self.model.removeQuestion(0)

    def QuestionsChanged(self, questions):
        self.view1.RefreshQuestions(questions)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
