POLL_PREFETCH_FIELDS = [
    'question_set',
    'question_set__rankingquestion',
    'question_set__rankingquestion__rankvote_set',
    'question_set__textchoicesquestion',
    'question_set__textchoicesquestion__textchoice_set',
    'question_set__textchoicesquestion__textchoice_set__choicevote_set',
    'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set',
    'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set__choicenuancevote_set',
]

QUESTION_PREFETCH_FIELDS = [
    field.replace('question_set__', '') for field in POLL_PREFETCH_FIELDS[1:]]

QUESTION_TYPES = ['rankingquestion', 'textchoicesquestion']
