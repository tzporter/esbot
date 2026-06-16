# Manual API Testing Observations Summary

This report summarizes our findings and what we observed while manually testing our ESBot REST API using Postman.

## 1. Were all status codes as expected?
Yes, in the end, all HTTP status codes matched what we expected in our API design. 

However, during the first few runs of the quiz generation workflow, we ran into a database crash before getting a clean HTTP response. The terminal threw a `sqlite3.IntegrityError: NOT NULL constraint failed: quizrequest.session_id`. After debugging the code, we realized this happened because we were passing raw integer IDs (like `session_id=1`) to our child models. This caused SQLModel/SQLAlchemy to lose track of the database session, making it try to set `session_id` to `None` during the commit phase. 

To fix this, we refactored our repository layer to use Object Relationships instead of raw integers. By passing the fully loaded `UserSession` object directly (`session=session_obj`), the ORM successfully mapped the data dependencies, and now the API returns proper status codes like `200 OK` every time.

## 2. Did the error messages provide useful feedback?
Yes, the API error messages are very helpful and make it easy to understand if something went wrong on the server side or if the input payload was wrong.

The best example of this was when we tested what happens if the AI service drops or disconnects. When we mocked the AI provider to throw a connection error, our backend code caught the exception perfectly. Instead of crashing the whole server or leaking a messy python stack trace to the user, the API handled it cleanly and returned a clear `503 Service Unavailable` status code with the JSON message `{"detail": "AI service unavailable"}`. 

## 3. Did any request behave unexpectedly?
The most unexpected behavior found was related to leftover data between different request steps. Since API tests run through the actual database, data created by one request stays in the tables for the next requests.

At first, when we tried to test quiz answer submissions, the requests started failing unexpectedly with foreign key errors. We found out this was because older sessions and chat messages from previous test runs were still sitting in the SQLite database and messing up the current logic. 

To solve this, we had to add a strict database cleanup step in our test setup. By deleting records from the tables in a reverse-dependency order, we cleared out all side effects. Now, every single API request behaves exactly as predicted without getting blocked by old data.