parse_data:
	python3 data/aspell/parse.py

	python3 data/birkbeck/parse.py

	python3 data/holbrook/parse.py
	
	python3 data/wikipedia/parse.py

	python3 data/sentences/gen_errors.py
	python3 data/sentences/parse.py


run_all:
	python3 models/eval_hunspell.py
	python3 models/eval_pyspell.py
	python3 models/eval_symspell.py
	python3 models/eval_t5.py
	python3 models/eval_textblob.py