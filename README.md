# inTune - Group Project

## TO DO (team members):

### 1. Clone and Update
clone repo if not done yet and make sure you've got the latest code from main branch:
```bash
git pull origin main
```
### 2. Create environment
```bash
conda create --name intune python=3.10
```

### 3. Activate the Environment
```bash
conda activate intune
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