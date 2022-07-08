# instawork

**Instructions to run the project**

**Pre-req** - ```python3, pip, git```

1) Clone the repo 
``git clone https://github.com/bajwa10/instawork``
2) Setup a virtual environment 
   1) Install virtualenv
   ```pip install virtualenv```  
   2) Initialize a virtual environment 
   ```virtualenv venv```
   3) Activate the virtual environment
   ```source bin/activate```
   4) Install the project requirements
   ```pip install -r requirements.txt```
3) Make migrations ```python3 manage.py makemigrations home```
4) Migrate ```python3 manage.py migrate```
5) Run ```python3 manage.py runserver``` to run the server
6) Click on the server link
