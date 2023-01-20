developed by: [Eduardo Lima](https://www.linkedin.com/in/eduardo-lima-araujo/)

<h1 align = 'center'>  Survivors API</h1>
<h2 align = 'center'>
<a href="https://mnxwj3.deta.dev/docs">Documentation</a>
</h2>

---
This is an API developed with [FastAPI](https://fastapi.tiangolo.com), a Python framework for building API's. The purpose of this application itself is to store survivors from a zombie apocalypse and allow them to find the closest survivor from their location.
<br/><br/>
All the survivors are stored in a <b>PostgreSQL database</b> hosted on [Supabase](https://supabase.com) and the application is hosted on [Deta](https://www.deta.sh).
<br/><br/>
The API's documentation is automatic and interactive, provided by [Swagger](https://swagger.io/docs/), which is already embedded in FastAPI as a feature.

---
## 📁  <u>**Setup</u>**
<p></p>
In order to run the application locally for debugging or running the tests, follow the steps below:

<br>

### **1. <u>Deploy locally**</u>

<p></p>

#### **1.1 Cloning the repository**
```cmd
$ git clone https://github.com/limaedu/projeto_latitude_survivorsAPI
```
#### **1.2 (Optional) Creating a virtual environment** (recommended)
```cmd
$ pip install virtualenv
```
```cmd
$ virtualenv -p python3 <env_name> #create environment
$ .\<env_name>\scripts\activate #activating
```

#### **1.3 Installing dependecies**

```cmd
$ pip install -r requirements.txt
```

#### **1.4 Deploying locally**

```cmd
$ uvicorn main:app --reload
```
After the last command, the API will be running on local server http://127.0.0.1:8000 by default.
           
---

### **2.  <u>Running the tests</u>**

<br>

Testing your application is really important for ensuring that it is performing as expected for expected and unexpected requests. That is why, the [TDD](http://agiledata.org/essays/tdd.html) methodology is an established technique for delivering quality softwares.

In this project, tests were built for all the endpoints, ensuring that they were all behaving as expected, including the exception handling. 

In order to test the **database** without affecting the PostgreSQL in production, when the tests are executed locally, a local **sqlite** database called **test.db** is created and stores all the mocked data.
<p></p>

#### **2.1 Executing the tests**

```cmd
$ pytest -v
```
---

### **2.  <u>Future improvements</u>**
<p></p>

- Implementing authentication, such as Bearer with JWT Tokens
- Develop more unit and integration tests
- Deploying the tests to a CI/CD plataform such as Jenkins or GitHub Actions
