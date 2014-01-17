class AMCQuestion:

  def __init__(self, label="", question="", answers=[], correct=0):
    self.label = label
    self.question = question
    self.answers = answers
    self.correct = correct

  def get_label(self): 
    return self.label

  def get_question(self): 
    return self.question

  def get_answers(self): 
    return self.answers

  def get_correct(self): 
    return self.correct
