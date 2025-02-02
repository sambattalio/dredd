''' quiz.py: Quiz class '''

import difflib
import os
import yaml

# Dredd Quiz Class ------------------------------------------------------------

class Quiz(object):
    ''' Dredd Quiz Class '''

    def __init__(self, quiz_path):
        questions_path = os.path.join(quiz_path, 'questions.yaml')
        answers_path   = os.path.join(quiz_path, 'answers.yaml')

        with open(questions_path) as questions_stream:
            self.questions = yaml.load(questions_stream)

        with open(answers_path) as answers_stream:
            self.answers   = yaml.load(answers_stream)

    def evaluate(self, responses):
        ''' Evaluate Quiz responses '''
        result = {}
        for question, response in responses.items():
            try:
                if self.questions[question]['type'] == 'single':
                    result[question] = self.evaluate_single(question, response)
                elif self.questions[question]['type'] == 'multiple':
                    result[question] = self.evaluate_multiple(question, response)
                elif self.questions[question]['type'] == 'order':
                    result[question] = self.evaluate_order(question, response)
                elif self.questions[question]['type'] == 'blank':
                    result[question] = self.evaluate_blank(question, response)
                else:
                    result[question] = 0
            except KeyError:
                result[question] = 0

        result['score'] = float('{:0.4f}'.format(sum(result.values())))
        return result

    def evaluate_single(self, question, response):
        for answer, value in self.answers[question]:
            if response == answer:
                return value
        return 0

    def evaluate_multiple(self, question, responses):
        if isinstance(responses, str):
            responses = [responses]

        answers, value = self.answers[question]
        return difflib.SequenceMatcher(None, sorted(responses), sorted(answers)).ratio() * value

    def evaluate_order(self, question, responses):
        answers, value = self.answers[question]
        return difflib.SequenceMatcher(None, responses, answers).ratio() * value

    def evaluate_blank(self, question, responses):
        result = 0

        if isinstance(responses, str):
            responses = [responses]

        for response, answers in zip(responses, self.answers[question]):
            for answer, value in answers:
                if answer.lower() == response.lower():
                    result += value
                    break
        return result

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
