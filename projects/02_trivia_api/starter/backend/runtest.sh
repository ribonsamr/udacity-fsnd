dropdb trivia_test &>/dev/null
createdb trivia_test &>/dev/null
psql trivia_test < trivia.psql &>/dev/null
python test_flaskr.py