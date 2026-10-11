\# Task Manager



This is a Python task manager project using Flask.



\## Commands

\- Install: `python -m pip install -r requirements.txt`

\- Run tests: `python -m pytest -v`

\- Lint: `python -m ruff check .`



\## Architecture

\- Follow the routes → services → repositories structure already used in the project.

\- Keep service logic inside `services/` instead of putting it in the route files.

\- Follow `services/users.py` as the main example for how service functions should be written.

\- Use the error classes from `utils/errors.py` instead of using random exceptions.



\## Conventions

\- Use type hints for functions.

\- Use Google-style docstrings.

\- Follow the same style already used in `services/users.py`.

\- Keep changes simple and only change what is needed for the task.



\## Do not touch

\- Do not change files inside `tests/` unless the prompt specifically asks for a test change.

\- Do not change existing routes in `routes/api.py` unless the task requires it.

\- Do not add new dependencies unless they are actually needed and added to `requirements.txt`.

