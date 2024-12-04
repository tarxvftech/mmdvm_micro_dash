dev:
	source env/bin/activate && uvicorn backend:app --host 0.0.0.0 --reload
