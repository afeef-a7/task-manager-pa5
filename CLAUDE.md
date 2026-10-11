# Task Manager



This is a Python task manager project using Flask.



## Commands

- Install: `python -m pip install -r requirements.txt`

- Run tests: `python -m pytest -v`

- Lint: `python -m ruff check .`



## Architecture

- Follow the routes → services → repositories structure already used in the project.

- Keep service logic inside `services/` instead of putting it in the route files.

- Follow `services/users.py` as the main example for how service functions should be written.

- Use the error classes from `utils/errors.py` instead of using random exceptions.



## Conventions

- All new functions in `services/` and `routes/` must include parameter and return type hints.

- Use Google-style docstrings.

- Follow the argument, return, error handling, and Google-style docstring pattern used in `services/users.py`.

- Keep changes simple and only change what is needed for the task.



## Do not touch

- Do not change files inside `tests/` unless the prompt specifically asks for a test change.

- Do not change existing routes in `routes/api.py` unless the task requires it.

- Do not add new dependencies unless they are actually needed and added to `requirements.txt`.


## Week 5 Additions

### Do not touch
- When working only on `routes/api.py`, do not directly import or access `USERS` from `services/users.py`. Use service functions instead.
- When working only on `tests/test_notifications.py`, do not modify `services/users.py` or `routes/api.py`.
- When working on notification service functions in `services/users.py`, do not modify `routes/api.py` unless the task specifically requires an API change.

### Architecture
- Keep user data access and validation in `services/users.py`, following the existing service pattern in `services/users.py`; `routes/api.py` should call these functions rather than access `USERS` directly.

### Commands
- Run tests after each subagent: `python -m pytest -q`.
