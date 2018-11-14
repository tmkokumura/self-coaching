# -*- coding: utf-8 -*-

S_QUESTION = '''
SELECT 
    question_id,
    question_text
FROM
    questions
WHERE
    question_id = ?;
'''

I_QUESTION_HIST = '''
INSERT INTO question_hists (question_id, accept_flag, prev_answer_hists_id, timestamp)
VALUES (?, ?, ?, ?);
'''

I_ANSWER_HIST = '''
INSERT INTO answer_hists (question_id, answer_text, timestamp)
VALUES (?, ?, ?);
'''