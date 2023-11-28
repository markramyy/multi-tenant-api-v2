# multi-tenant-api-v2

---
## Project 

---

1. [How to use it](#how-to-use-it)

2. [Brief explanation](#brief-explanation)

3. [Documentation](#documentation)

---
### How to use it

---

- To clone and open the application

```python

# Clone this repository
$ git clone https://github.com/markramyy/multi-tenant-api-v2.git

# Then go into the repository
$ cd multi-tenant-api-v2

# Open it in vs code or any prefered IDEs
$ code .

```

---

- Create virtual environment and install dependencies

```python

# Create a Virtualenv
$ python3 -m venv env # or python -m venv env

# Activate the env
$ source env/bin/activate # or env/Scripts/activate

# Install dependencies
$ pip install -r requirements.txt

# Update your pip command not mandatory
$ pip install --upgrade pip

```

- If the env still didn't activate probably you are running on a different shell so go check your platform and write the correct command -> https://docs.python.org/3/library/venv.html

---

- Create a superuser and run the server

```python

# You want need to make any migrations because it is already in neon tech console (an online Database platform configurations)

# If you needed to change the database settings you have to make the mogrations after you are done
$ python manage.py makemigrations
$ python manage.py migrate

# Create super user
$ python manage.py createsuperuser
# Enter any credentials you want 
# example : (email = admin@admin.com, password = admin, password = admin, y)

# Run the server
$ python manage.py runserver

```

- If you had any problem running this commands consider to change **python** to **python3**.

---

- After you run the server. Handle Authentication token :
	1. Create a new user from -> **post /api/tenants/create**
	2. Create a validation token from ->  **post /api/tenants/token**
	3. Copy the token provided and open the Authorize button at the top right of the page
	4. Go for the **tokenAuth** section and in the Value text box paste your token BUT it must be in the right format -> **Token {the copied token without the brackets}**
	5. Now you can do what ever you want until you logout.

---

- When logging in the admin view using the super user and after you login, you have faced an error page just refresh the page or press the go back button it will work just fine.

---
### Brief explanation

---

1. **Modular Architecture**: Implemented modular design by dividing functionality into dedicated Django apps (`core`, `tenants`, `items`), promoting clean separation of concerns and easier maintenance.

2. **Custom User Model**: Utilized a custom user model for flexibility in authentication and user management, allowing for future enhancements specific to the project's needs.

3. **Robust Database Setup**: Configured PostgreSQL with SSL for a secure, scalable database backend, indicating readiness for handling complex queries and transactions in production.

4. **API-Centric Design**: Emphasized on API development with RESTful patterns, employing Django REST framework for structured endpoints and DRF Spectacular for API schema generation and documentation.

5. **Security Measures**: Enforced token-based authentication for secure, stateless user sessions and interactions with the API, aligning with best practices for web service security.

6. **Automated Testing**: Included comprehensive tests within each app to ensure robustness and reliability of the custom user model and item management features.

---

### Documentation

---

- if you have come from a non technical background and can't fully understand the code that has been written. I suggest for you to go and read the **Documentation.md** file that have been attached to the project.

- [[Documentation.md]]

---
