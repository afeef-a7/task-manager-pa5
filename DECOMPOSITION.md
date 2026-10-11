# Task 2 - Subagent Pipeline

## Decomposition

### SA-1: User Data

* Input: services/users.py, CLAUDE.md
* Task: Add notification\_pref to user records with a default of "none".
* Output: services/users.py
* Constraint: Do not touch routes/api.py, tests/test\_tasks.py, utils/errors.py, or any task-related functions.
* Hand-off: Existing users and newly created users have notification\_pref set to "none".
* Test result: 65 passed in 0.35s using pytest -q. Ruff passed. Claude modified only services/users.py and followed the file restrictions. Its first test attempt could not run because Flask was missing in its environment, so it created a temporary environment outside the project and reran the tests successfully.

Exact prompt:
Add notification\_pref to the existing USERS records and newly created users in services/users.py. The default must be "none". Keep the existing functions and behavior unchanged except for the new field. Follow CLAUDE.md. Do not change routes/api.py, tests/, or utils/errors.py. Run pytest -q and report the result.

### SA-2: Notification Service

* Input: services/users.py, utils/errors.py, CLAUDE.md
* Task: Add service functions for getting and updating notification preferences.
* Output: services/users.py
* Constraint: Do not touch routes/api.py, tests/, utils/errors.py, or task-related files.
* Hand-off: Service functions that retrieve and update email, sms, or none preferences and reject invalid values.
* Test result: 65 passed in 0.39s using pytest -q. Ruff passed. Claude added get\_notification\_pref and update\_notification\_pref to services/users.py. It reported no changes to restricted source files. Claude also installed dependencies into the project's .venv because they were missing in its environment.

Exact prompt:
Add get\_notification\_pref and update\_notification\_pref service functions in services/users.py. Allow only "email", "sms", or "none". Use NotFoundError for missing users and ValidationError for invalid preferences from utils/errors.py. Follow the patterns in services/users.py, including type hints and Google-style docstrings. Do not modify routes/api.py, tests/, utils/errors.py, or task-related files. Run pytest -q and report the result.

### SA-3: Notification API

* Input: routes/api.py, services/users.py, utils/errors.py, CLAUDE.md
* Task: Add notification endpoints and ensure user responses include notification\_pref.
* Output: routes/api.py
* Constraint: Do not touch services/users.py, tests/, utils/errors.py, or task-related routes.
* Hand-off: Working notification GET and PATCH endpoints and user responses containing notification\_pref.
* Test result: 65 passed in 0.35s using pytest -q. Ruff passed. Claude modified routes/api.py and added three endpoints. However, GET /users accesses USERS directly in routes/api.py because SA-3 was not allowed to change services/users.py. This followed the file restrictions but did not fully follow the service-layer architecture in CLAUDE.md. Claude also added type validation in the PATCH route.

Exact prompt:
In routes/api.py, add GET and PATCH /users/[int:user\_id](int:user_id)/notifications using the notification service functions. PATCH must accept notification\_pref in JSON and return the updated preference. Add GET /users to return all users, since this project currently only has the user detail endpoint. Make sure user list and detail responses include notification\_pref. Follow CLAUDE.md and existing route patterns. Do not modify services/, tests/, utils/errors.py, or existing task routes. Run pytest -q and report the result.

### SA-4: Notification Tests

* Input: tests/test\_tasks.py, app.py, routes/api.py, services/users.py, utils/errors.py, CLAUDE.md
* Task: Add automated tests covering notification preferences and API responses.
* Output: tests/test\_notifications.py
* Constraint: Do not touch services/, routes/, utils/, app.py, or tests/test\_tasks.py.
* Hand-off: Tested notification feature with documented passing results.

Test result: 86 passed in 0.40s using pytest -q. Ruff passed. Claude created only tests/test\_notifications.py with 21 new tests. The tests covered default preferences, valid and invalid updates, missing users, notification endpoints, user responses, and restored shared test data.

Exact prompt:
Create tests/test\_notifications.py to test notification preferences. Cover default "none", changing to email and sms, invalid preferences returning 422, missing users returning 404, GET notification preferences, and notification\_pref in user detail and list responses. Use Flask test-client tests and isolated test data that is restored after each test. Follow CLAUDE.md. Do not modify production files or tests/test\_tasks.py. Run pytest -q and report the result.


## Divergence

1. **Constraint violations:** Claude followed the file restrictions for all four subagents. However, SA-3 accessed the USERS dictionary directly in routes/api.py when implementing GET /users. This went against the architecture rule in CLAUDE.md that says service logic should stay inside services/. Claude did this because SA-3 was not allowed to edit services/users.py.

2. **Hand-off problems and recovery:** SA-2 provided the notification service functions needed by SA-3, but it did not provide a function for listing all users. SA-3 needed this for GET /users, so Claude used the USERS dictionary directly in the route instead. The tests passed, but the architecture problem was still unresolved. A better solution would be to add a get_users function in services/users.py and have the route call it.

3. **What I would change:** If I did this again, I would include get_users in SA-2's task and hand-off. That would allow SA-3 to implement the user-list endpoint without accessing USERS directly or breaking the service-layer rule.

## Integration Correction

After all four subagents finished, I fixed the architecture issue found in SA-3. I added get_users() to services/users.py and updated routes/api.py so GET /users calls the service instead of accessing USERS directly. This was done separately from the subagent sessions to keep their original results documented. After the correction, pytest -q passed all 86 tests and Ruff reported no errors.
