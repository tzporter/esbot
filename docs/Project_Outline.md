# Project Outline
## Software Stack
Due to our group members’ prior experience with Python, we have chosen to develop a Python-based software stack. The back end will be FastAPI, The front end will be Streamlit, and the Data storage will be done through PostgreSQL.

#### Back End
We have selected Fast API as the back end because it is the premier back end option for python. We intend to make calls to the Groq API through this. 

We considered many LLM options such as Local hosting and APIs (including Gemini and OpenAI). Due to price restrictions, we eliminated OpenAI, and we eliminated local hosting due to the additional complexity. In the end, we chose Groq because of its wide variety of accessible models, all of which have much higher free usage limits than Gemini. Groq is also a good option because Ollama, Gemini and Groq are all easily swappable thanks to the standardization of the OpenAI API (see https://ai.google.dev/gemini-api/docs/openai)

#### Front End
We chose StreamLit, an open-source app framework, because it was designed for AI applications, making it fundamentally compatible with our goal. In addition, it is Python-based, which aligns with our previous experience.
#### Database
We chose Postgre SQL because we wanted a simple and complete storage solution. While there are other options out there, our team members have prior experience with this one, making it an ideal option.
#### Containerization
We chose to use Docker to containerize our application. This allows us to use a consistent set of libraries that isn’t affected by our different operating systems. Additionally, it means that our set of libraries can be updated via GitHub, allowing all of our devices to stay perfectly synced.


## Team Roles
While people are assigned to specific roles, all members are expected to check each other’s work and ensure the quality of the entire system.

Front end: Melek
Back end: Zeynep, Sena
Database, Containerization: Truman
Documentation: Everyone
