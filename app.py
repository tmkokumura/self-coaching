# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, make_response
from contextlib import closing
from datetime import datetime
import sqlite3
import random
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

    # 最初の質問を取得する
    question_id = 1
    question_text = select_question(question_id)

    # 質問履歴を登録
    question_hist_id = insert_question_hist(question_id)

    logging.info(
        'question_hist_id={}, question_id={}, question_test={}'.format(question_hist_id, question_id, question_text))
    logging.info('--- End [index()] ---')

    return render_template('index.html', question_hist_id=question_hist_id, question_text=question_text)


@app.route('/answer', methods=['POST'])
def answer():
    """
    回答するボタン押下時
    :return:
    """
    logging.info('--- Start [answer()] ---')

    question_hist_id = request.form.get('question_hist_id')
    answer_text = request.form.get('answer_text')
    logging.info('question_hist_id: {}'.format(question_hist_id))
    logging.info('answer_text: {}'.format(answer_text))

    # 回答履歴を登録
    insert_answer_hist(question_hist_id, consts.ANSWER_TYPE_ANSWER, answer_text=answer_text)

    # 次の質問を取得
    next_question_id = get_next_question_id()
    next_question_text = select_question(next_question_id)

    # 質問履歴を登録
    next_question_hist_id = insert_question_hist(next_question_id, prev_question_hist_id=question_hist_id)

    res = {
        'question_hist_id': next_question_hist_id,
        'question_text': next_question_text
    }

    logging.info(
        'question_hist_id={}, question_id={}, question_test={}'.format(next_question_hist_id, next_question_id,
                                                                       next_question_text))
    logging.info('--- End [answer()] ---')

    return make_response(jsonify(res))


@app.route('/change', methods=['POST'])
def change():
    """
    質問を変えるボタン押下時
    :return:
    """
    logging.info('--- Start [change()] ---')

    question_hist_id = request.form.get('question_hist_id')
    logging.info('question_hist_id: {}'.format(question_hist_id))

    # 回答履歴を登録
    insert_answer_hist(question_hist_id, consts.ANSWER_TYPE_CHANGE)

    # 次の質問を取得
    next_question_id = get_next_question_id()
    next_question_text = select_question(next_question_id)

    # 質問履歴を登録
    next_question_hist_id = insert_question_hist(next_question_id, prev_question_hist_id=question_hist_id)

    res = {
        'question_hist_id': next_question_hist_id,
        'question_text': next_question_text
    }

    logging.info(
        'question_hist_id={}, question_id={}, question_test={}'.format(next_question_hist_id, next_question_id,
                                                                       next_question_text))
    logging.info('--- End [change()] ---')

    return make_response(jsonify(res))


# 次の質問IDを決定する
def get_next_question_id():
    record = select(sql.S_MIN_MIX_QUESTION_ID)
    min_question_id = record[0][0]
    max_question_id = record[0][1]
    return random.randrange(min_question_id, max_question_id - 1)


# 質問を取得する
def select_question(question_id):
    params = (question_id,)
    record = select(sql.S_QUESTION, params)
    return record[0][0]


# 質問履歴を登録する
def insert_question_hist(question_id, prev_question_hist_id=None):
    params = (question_id, prev_question_hist_id, format_date(datetime.now()))
    insert(sql.I_QUESTION_HIST, params)
    record = select(sql.S_MAX_QUESTION_HIST_ID)
    return record[0][0]


# 回答履歴を登録する
def insert_answer_hist(question_hist_id, answer_type, answer_text=None):
    params = (question_hist_id, answer_type, answer_text, format_date(datetime.now()))
    insert(sql.I_ANSWER_HIST, params)


# SELECT文発行
def select(sql_str, params=None):

    logging.debug('Sql statement: {}'.format(sql_str))
    logging.debug('params: {}'.format(params))

    with closing(sqlite3.connect(consts.DATABASE)) as conn:
        cur = conn.cursor()

        if params is None:
            cur.execute(sql_str)
        else:
            cur.execute(sql_str, params)

        return cur.fetchall()


# INSERT文発行
def insert(sql_str, params=None):

    logging.debug('Sql statement: {}'.format(sql_str))
    logging.debug('params: {}'.format(params))

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
