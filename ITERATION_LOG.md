## Session 1 — October 4, 2026

### Prompt used

Add error handling to the get_task function in @services/tasks.py. Do not change the function signature. Run pytest -v when done.

### What Claude did

Claude added a NotFoundError check to get_task in services/tasks.py. It followed the same pattern as get_user in services/users.py, added a Google-style docstring, and did not change the function signature. It also ran the tests and all 4 passed.

### Observation

Claude followed the CLAUDE.md rules correctly in this session. The rules about following services/users.py, using the error classes from utils/errors.py, and using Google-style docstrings helped it make the change correctly.

### CLAUDE.md update

No update for this session because Claude followed the instructions correctly.

## Session 2 — October 4, 2026

### Prompt used

Refactor create_task in @services/tasks.py to match the style of get_user in @services/users.py exactly. Run pytest -v when done.

### What Claude did

Claude refactored create_task to match the style in services/users.py. It added a Google-style docstring and a ValidationError for an empty title. It also ran the tests and all 4 passed.

### Observation

Claude followed the CLAUDE.md rules correctly again. It used services/users.py as the example and followed the same error handling and docstring style.

### CLAUDE.md update

I made the convention more specific by saying that service functions should follow the argument, return, raise, and docstring pattern used in services/users.py.

## Session 3 — October 4, 2026

### Prompt used

Goal: Add a new endpoint to create a product.

Constraints: Do not change any existing endpoints.

Verification: Run pytest -v when done.

### What Claude did

Claude created services/products.py with a create_product function and added a new POST /api/products endpoint in routes/api.py. It followed the existing error handling style and all 6 tests still passed.

### Observation

Claude mostly followed the CLAUDE.md, but it added create_product_route without a return type hint even though my CLAUDE.md says to use type hints for functions. The tests still passed, so they did not catch this issue.

### CLAUDE.md update

I changed the type hint rule to make it more specific because Claude added a new route function without a return type hint.

I changed:

`Use type hints for functions.`

to:

`All new functions in services/ and routes/ must include parameter and return type hints.`