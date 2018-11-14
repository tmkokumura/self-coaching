DROP TABLE question_types;
CREATE TABLE question_types (question_type_id INTEGER PRIMARY KEY, question_type_name TEXT NOT NULL);
DROP TABLE questions;
CREATE TABLE questions (question_id INTEGER PRIMARY KEY, question_text TEXT NOT NULL, question_type_id INTEGER NOT NULL);
DROP TABLE question_hists;
CREATE TABLE question_hists (question_hists_id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER NOT NULL, accept_flag INTEGER NOT NULL, prev_answer_hists_id INTEGER, timestamp TEXT NOT NULL);
DROP TABLE answer_hists;
CREATE TABLE answer_hists (answer_hists_id INTEGER PRIMARY KEY AUTOINCREMENT, answer_text TEXT, timestamp TEXT NOT NULL);