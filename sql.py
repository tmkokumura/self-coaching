# -*- coding: utf-8 -*-

# 質問IDの最小値と最大値を取得
S_MIN_MIX_QUESTION_ID = '''
SELECT
    MIN(question_id),
    MAX(question_id)
FROM
    questions;
'''

# 質問を取得
S_QUESTION = '''
SELECT 
    question_text
FROM
    questions
WHERE
    question_id = ?;
'''

# 質問履歴を登録
I_QUESTION_HIST = '''
INSERT INTO question_hists (question_id, prev_question_id, timestamp)
VALUES (?, ?, ?);
'''

# 質問履歴IDの最大値を取得
S_MAX_QUESTION_HIST_ID = '''
SELECT
    MAX(question_hist_id)
FROM
    question_hists;
'''

# 回答履歴を登録
I_ANSWER_HIST = '''
INSERT INTO answer_hists (question_hist_id, answer_type, answer_text, timestamp)
VALUES (?, ?, ?, ?);
'''
