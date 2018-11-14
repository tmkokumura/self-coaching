# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, make_response
from contextlib import closing
from datetime import datetime
import sqlite3
import consts
import sql
import logging
logging.basicConfig(level=consts.LOG_LEVEL, format=consts.LOG_FORMAT)

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """
    初期表示
    :return: index.html
    """
    logging.info('--- Start [index()] ---')

    question_id, question_text = select_question(1)

    logging.info('--- End [index()] ---')

    return render_template('index.html', question_id=question_id, question_text=question_text)


@app.route('/answer', methods=['POST'])
def answer():
    logging.info('--- Start [answer()] ---')

    prev_answer_hist_id = request.form.get('prev_answer_hist_id')
    question_id = request.form.get('question_id')
    answer_text = request.form.get('answer')
    logging.info('prev_answer_hist_id: {}'.format(prev_answer_hist_id))
    logging.info('question_id: {}'.format(question_id))
    logging.info('answer_text: {}'.format(answer_text))

    if prev_answer_hist_id is None:
        insert_question_hist(question_id, consts.ACCEPT_FLAG_ON)
    else:
        insert_question_hist(question_id, consts.ACCEPT_FLAG_ON, prev_answer_hist_id=prev_answer_hist_id)

    insert_answer_hist(question_id, answer_text)
    question_id, question_text = select_question(1)

    res = {'question_id': question_id, 'question_text': question_text, 'prev_answer_hist_id': prev_answer_hist_id}

    logging.info('--- End [answer()] ---')

    return make_response(jsonify(res))


@app.route('/change', methods=['POST'])
def change():
    logging.info('--- Start [change()] ---')

    prev_answer_hist_id = request.form.get('prev_answer_hist_id')
    question_id = request.form.get('question_id')
    logging.info('prev_answer_hist_id: {}'.format(prev_answer_hist_id))
    logging.info('question_id: {}'.format(question_id))

    insert_question_hist(question_id, consts.ACCEPT_FLAG_OFF, prev_answer_hist_id=prev_answer_hist_id)
    question_id, question_text = select_question(1)

    res = {'question_id': question_id, 'question_text': question_text, 'prev_answer_hist_id': prev_answer_hist_id}

    logging.info('--- End [change()] ---')

    return make_response(jsonify(res))


# 質問を取得する
def select_question(question_id):
    params = (question_id,)
    record = select(sql.S_QUESTION, params)
    return record[0][0], record[0][1]


# 質問履歴を登録する
def insert_question_hist(question_id, accept_flag, prev_answer_hists_id=None):
    params = (question_id, accept_flag, prev_answer_hists_id, format_date(datetime.now()))
    insert(sql.I_QUESTION_HIST, params)


# 回答履歴を登録する
def insert_answer_hist(question_id, answer_text):
    params = (question_id, answer_text, format_date(datetime.now()))
    insert(sql.I_ANSWER_HIST, params)


# SELECT文発行
def select(sql_str, params=None):

    logging.info('Sql statement: {}'.format(sql_str))
    logging.info('params: {}'.format(params))

    with closing(sqlite3.connect(consts.DATABASE)) as conn:
        cur = conn.cursor()

        if params is None:
            cur.execute(sql_str)
        else:
            cur.execute(sql_str, params)

        return cur.fetchall()


# INSERT文発行
def insert(sql_str, params=None):

    logging.info('Sql statement: {}'.format(sql_str))
    logging.info('params: {}'.format(params))

    with closing(sqlite3.connect(consts.DATABASE)) as conn:
        cur = conn.cursor()

        if params is None:
            cur.execute(sql_str)
        else:
            cur.execute(sql_str, params)

        conn.commit()


# 日付フォーマット
def format_date(date):
    return datetime.strftime(date, consts.SQL_DATE_FORMAT)


if __name__ == '__main__':
    app.run()