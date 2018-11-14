# -*- coding: utf-8 -*-
import logging

# database name
DATABASE = 'self-coaching.sqlite3'

# log settings
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(levelname)s %(pathname)s %(funcName)s :%(message)s'


# accept flag
ANSWER_TYPE_ANSWER = 1  # 回答した
ANSWER_TYPE_CHANGE = 2  # 質問を変えた


# format
SQL_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
