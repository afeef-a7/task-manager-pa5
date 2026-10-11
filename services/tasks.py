from utils.errors import NotFoundError, ValidationError

TASKS: dict[int, dict] = {
    1: {"id": 1, "title": "Buy groceries",  "done": False, "user_id": 1, "priority": 3},
    2: {"id": 2, "title": "Write report",   "done": False, "user_id": 1, "priority": 3},
    3: {"id": 3, "title": "Call dentist",   "done": True,  "user_id": 2, "priority": 3},
}

def process_order(task_id: int) -> dict:
    task = TASKS[task_id]
    task["done"] = True
    return task

def get_task(task_id: int) -> dict:
    """Retrieve a task by ID.

    Args:
        task_id: The unique identifier for the task.

    Returns:
        The task record as a dictionary.

    Raises:
        NotFoundError: If no task exists with the given ID.
    """
    if task_id not in TASKS:
        raise NotFoundError("Task")
    return TASKS[task_id]

def get_tasks_by_user(user_id: int) -> list[dict]:
    """Retrieve all tasks belonging to a user.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        A list of task records belonging to the user.
    """
    return [task for task in TASKS.values() if task["user_id"] == user_id]

def create_task(title: str, user_id: int, priority: int = 3) -> dict:
    """Create a new task.

    Args:
        title: The task's title.
        user_id: The ID of the user the task belongs to.
        priority: The task's priority from 1 to 5. Defaults to 3.

    Returns:
        The newly created task record.

    Raises:
        ValidationError: If title is empty or priority is not an integer
            between 1 and 5.
    """
    if not title or not title.strip():
        raise ValidationError("title", "cannot be empty")
    _validate_priority(priority)
    new_id = max(TASKS.keys()) + 1
    TASKS[new_id] = {"id": new_id, "title": title,
                     "done": False, "user_id": user_id, "priority": priority}
    return TASKS[new_id]

def update_task_priority(task_id: int, priority: int) -> dict:
    """Update the priority of an existing task.

    Args:
        task_id: The unique identifier for the task.
        priority: The new priority from 1 to 5.

    Returns:
        The updated task record.

    Raises:
        NotFoundError: If no task exists with the given ID.
        ValidationError: If priority is not an integer between 1 and 5.
    """
    task = get_task(task_id)
    _validate_priority(priority)
    task["priority"] = priority
    return task

def get_tasks(priority: int | None = None) -> list[dict]:
    """Retrieve all tasks, optionally filtered by priority.

    Args:
        priority: If given, only tasks with this priority (1 to 5) are returned.

    Returns:
        A list of task records.

    Raises:
        ValidationError: If priority is not an integer between 1 and 5.
    """
    if priority is None:
        return list(TASKS.values())
    _validate_priority(priority)
    return [task for task in TASKS.values() if task["priority"] == priority]

def parse_priority(value: str) -> int:
    """Convert a query-string priority to a validated integer.

    Args:
        value: The raw priority value from the request.

    Returns:
        The priority as an integer from 1 to 5.

    Raises:
        ValidationError: If value is not exactly one of "1", "2", "3", "4" or "5".
    """
    if value not in {"1", "2", "3", "4", "5"}:
        raise ValidationError("priority", "must be an integer between 1 and 5")
    return int(value)

def _validate_priority(priority: int) -> None:
    """Validate a task priority.

    Args:
        priority: The priority value to check.

    Raises:
        ValidationError: If priority is not an integer between 1 and 5.
    """
    if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
        raise ValidationError("priority", "must be an integer between 1 and 5")
