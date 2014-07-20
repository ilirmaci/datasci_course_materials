#! /bin/bash

sqlite3 reuters.db < problem1a.sql > select.txt
sqlite3 reuters.db < problem1b.sql > select_project.txt
sqlite3 reuters.db < problem1c.sql > union.txt
sqlite3 reuters.db < problem1d.sql > count.txt
sqlite3 reuters.db < problem1e.sql > big_documents.txt
sqlite3 reuters.db < problem1f.sql > two_words.txt

sqlite3 matrix.db < problem2g.sql > multiply.txt
sqlite3 reuters.db < problem2h.sql > similarity_matrix.txt
sqlite3 reuters.db < problem2i.sql > keyword_search.txt
