# inTune - Group Project

## TO DO (team members):

### 1. Clone and Update
clone repo if not done yet and make sure you've got the latest code from main branch:
```bash
git pull origin dev
```
### 2. Create environment
```bash
conda create --name intune python=3.10
```
```bash
python -m venv .venv
```

### 3. Activate the Environment
```bash
conda activate intune
```
```bash
source .venv/bin/activate
```
### 4. Install Requirements
Install all the necessary libraries (Django, etc.):
as of now (march 2) theres only django but we'll have to run this command everytime someone installs a new package

```bash
pip install -r requirements.txt
```

### 5. Run the Server
Start the local website:
(i dont think this is necessary yet)
```bash
python manage.py runserver
```
then go to http://127.0.0.1:8000/ in browser

### 6. Go to branches locally
```bash
git fetch dev
git checkout feature/accounts (Eve)
git checkout feature/spotify (Theresa)
git checkout feature/matching (Euan)
git checkout feature/messaging (Morgan)
```

### 7. Commit and merge to dev

#### When you are finished for the day (in your local branch):
```bash
git add .
git commit -m "[Explain what you've done]"
git push 
```
#### Merge to Dev
```bash
git checkout dev
git pull
git merge feature/accounts
git merge feature/(ur branch)
git push
```

## PUSH TO DEV NOT MAIN 

## File Purposes
### .github/workflows/django.yml
#### Automated Quality Control System
- Every time someone pushes code to GitHub, an automated process starts on a fresh cloud server.
- It automatically installs all dependencies from requirements.txt and runs python manage.py test.
- If someone pushes code that "breaks" the project (e.g., a typo or a broken database model), GitHub will show a Red X. If everything is perfect, we get a Green Checkmark.
- Ensures that our main branch always stays functional and that we catch bugs before they reach the final submission.


## Team Workflow 
Keep Requirements Up to Date
If you install a new package, you must update the requirements file so the rest of the team gets it:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "add (package name) to requirements"
git push
```


### Fix base.html and home.html once urls have been registered
base.html
```bash
{% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'accounts:profile' %}">Profile</a>
                    <a class="nav-link" href="{% url 'matching:queue' %}">Find Matches</a>
                    <a class="nav-link" href="{% url 'messaging:inbox' %}">Messages</a>
                    <a class="nav-link" href="{% url 'accounts:logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
                    <a class="nav-link" href="{% url 'accounts:register' %}">Register</a>
                {% endif %}
```
home.html
```bash
<div class="text-center mt-5">
    <h1>Welcome to Intune 🎵</h1>
    <p class="lead">Find your perfect match through music</p>
    <a href="{% url 'accounts:login' %}" class="btn btn-success me-2">Login</a>
    <a href="{% url 'accounts:register' %}" class="btn btn-outline-success">Register</a>
</div>
```
Developed for WAD2 Coursework - University of Glasgow