# PA5 Retrospective

## 1. Plan Mode Value

In Session 2 of PLAN_LOG.md, Claude originally planned tests that would change the shared TASKS dictionary without restoring it. I amended the plan and asked Claude to add a restore_tasks fixture along with Flask API tests. This helped prevent the new PATCH tests from affecting other tests and possibly requiring changes to be reverted later. In Session 4, Claude found similar problems in older tests, which were then fixed. After the final review, all 65 tests passed, and the shared-state check showed that TASKS was unchanged.

## 2. Plan Mode Limits

In Session 1 of PLAN_LOG.md, Claude did not fully follow the amended plan. I asked it to add tests for creating tasks with different priorities. The plan used user_id=1, but Claude changed it to user_id=3 because using user 1 would interfere with an existing test. The tests passed, but this showed me that approving a plan does not mean Claude will follow every detail exactly. I still need to review the changes and compare them with what I approved.

## 3. Subagent Value

The most important boundary in Task 2 was between services/users.py and routes/api.py. SA-2 was responsible for the service functions, while SA-3 was responsible for the API endpoints. However, SA-2 did not create a get_users function, so SA-3 accessed the USERS dictionary directly in routes/api.py. This went against the architecture rule in CLAUDE.md. If I had done everything in one session, I might not have noticed which part caused this problem. After the four subagents finished, I fixed it by adding get_users to services/users.py and updating the route to use it. All 86 tests still passed.

## 4. Gap Analysis

The rule I would most want to enforce automatically is that routes/api.py should not access the USERS dictionary directly. SA-3 showed that Claude could follow its file restrictions but still break an architecture rule. A hook could check changes to routes/api.py and block them if they directly import USERS from services/users.py. This would help make sure user data is accessed through service functions instead of directly through the route file.
