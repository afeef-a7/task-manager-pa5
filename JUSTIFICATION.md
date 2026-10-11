\# JUSTIFICATION



For the Commands section, I added the exact commands needed to install the requirements, run the tests, and run Ruff. I wrote the commands this way so Claude would not have to guess how the project should be tested or checked. The testing command was important in all of my sessions because Claude ran the tests after making changes. If I had to shorten this section, I would keep the test command and remove the install command since the project was already set up.



For the Architecture section, I told Claude to follow the routes → services → repositories structure and to use services/users.py as the main example. This helped because Claude followed the same service pattern when changing get\_task and create\_task. I also included the rule to use error classes from utils/errors.py instead of random exceptions. If I had to remove something, I would remove the general line about keeping service logic inside services/ because the services/users.py example already shows the correct pattern.



For the Conventions section, I included type hints, Google-style docstrings, and the pattern used in services/users.py. Session 2 showed that Claude followed the argument, return, error handling, and docstring pattern correctly. Later, Claude created create\_product\_route without a return type hint, so I made the type hint rule more specific and said that new functions in services/ and routes/ need parameter and return type hints. If I had to shorten this section, I would remove the line about keeping changes simple because the more specific rules are more useful.



For the Do not touch section, I added rules about not changing tests unless the prompt asks for it, not changing existing routes unless needed, and not adding dependencies unless they are added to requirements.txt. These rules are there to stop Claude from making changes outside the scope of the task. In the product endpoint session, Claude added a new route but left the existing routes alone, which showed that the rule was useful. If I had to cut this section down, I would probably remove the dependency rule because it was not relevant to any of my sessions.



If this were a team project with three developers, I would make two main changes. First, I would add rules about how branches, commits, and code reviews should be handled so everyone follows the same workflow. Second, I would add clearer ownership rules for important files so Claude does not change code another developer is working on without a reason. This would make the CLAUDE.md more useful for a team because it would control both coding style and how changes are made across the project.

