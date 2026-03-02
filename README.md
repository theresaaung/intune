# inTune - Group Project

## TO DO (team members):

### 1. Clone and Update
clone repo if not done yet and make sure you've got the latest code from main branch:
```bash
git pull origin main
```
### 2. Create a Virtual Environment (venv)
#### Mac/Linux:
```bash
python3 -m venv venv
```
#### Windows:
```bash
python -m venv venv
```

### 3. Activate the Environment
must do this every time you open a new terminal to work on the project. kinda like conda activate rango i think (might have to double check)
#### Mac/Linux: 
```bash
source venv/bin/activate
```
#### Windows: 
```bash
venv\Scripts\activate
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

## Team Workflow 
Keep Requirements Up to Date
If you install a new package, you must update the requirements file so the rest of the team gets it:

```bash
pip freeze > requirements.txt
```

### Remember to pull code before you start
```bash
git pull origin main
```
#### When you are finished for the day:
```bash
git add .
```
``` bash
git commit -m "[Explain what you've done]"
```
```bash
git push origin main
```

Developed for WAD2 Coursework - University of Glasgow