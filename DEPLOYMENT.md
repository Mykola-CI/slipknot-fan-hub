# Deployment

- The app was deployed to [Heroku](https://heroku.com/).
- The database was deployed to [ElephantSQL](https://www.elephantsql.com/).

- The app can be reached by the [link](https://slipknot-fan-hub-fe591bad3f33.herokuapp.com/).

## Local deployment


Create a local copy of the GitHub repository:

1. Open a folder on your computer with the terminal.
2. Run the following command
  - `gh repo clone Mykola-CI/slipknot-fan-hub`

---

3. Install the dependencies:

    - Open the terminal window and type: `pip3 install -r requirements.txt`


4. Create a `.gitignore` file in the root directory of the project where you should add env.py and __pycache__ files to prevent the privacy of your secret data.

5. Create an `.env` file. This will contain the following environment variables:

| Variable | What it does | Comments |
| ---- | ---- | ---- |
| SECRET_KEY= | sets unique identifier for the django project | |
| DEBUG=True | Server runs in DEBUG mode | on production server this variable must be added and set explicitly to False |
| DATABASE_URL=postgres:// | sets API for ElephantSQL | If you use another cloud service refer to their API setting guide |
| CLOUDINARY_URL=cloudinary:// | sets API for Cloudinary | If you use another cloud service refer to their API setting guide |
| EMAIL_HOST_USER= | django-allauth settings | required for email verification, sender's email |
| EMAIL_HOST_PASSWORD= | this is GMAIL app password API | if you use another mailing service refer to their API setting guide |
| DEFAULT_FROM_EMAIL= | django-allauth settings to show sender information | 


6. Run the following commands in a terminal to make migrations: 
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`
7. Create a superuser to get access to the admin environment.
    - `python3 manage.py createsuperuser`
    - Enter the required information (your username, email and password).
8. Run the app with the following command in the terminal:
    - `python3 manage.py runserver`
9. Open the link provided in a browser to see the app.

10. If you need to access the admin page:
    - Add /admin/ to the link provided.
    - Enter your username and password (for the superuser that you have created before).
    - You will be redirected to the admin page.

## Create Database on ElephantSQL

1. Go to [ElephantSQL](https://www.elephantsql.com/) and create a new account.

2. Create a new instance of the database.

3. Select a name for your database and select the free plan.

4. Click "Select Region"

5. Select a region close to you.

6. Click "Review"

7. Click "Create Instance"

8. Click on the name of your database to open the dashboard.

9. You will see the dashboard of your database. You will need the URL of your database to connect it to your Django project.

---

## Create Media Library on Cloudinary 

1. Install the Python packages required to connect to the Cloudinary API (if not yet installed via `pip3 install -r requirements.txt`)

`pip3 install cloudinary dj3-cloudinary-storage urllib3`

In order to be on the safe side you may specify versions that are 'freezed' in my requirements.txt

`pip3 install cloudinary~=1.40.0 dj3-cloudinary-storage~=0.0.6 urllib3~=2.2.1`

2. Sign up to [Cloudinary](https://cloudinary.com/users/register_free)

- Provide name and email address and choose a password or sign in with a social account.
- If asked, How would you best describe yourself? you can click on Developer.
- Depending on your chosen sign-up method, you may have to respond to an email verification.

3. In the Cloudinary dashboard, go to API keys.

4. In API Keys copy the CLOUDINARY_URL template and paste to .env file 

It is going to look like\ 
CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@<your_cloud_name>

5. Substitute the segments in the template with actual API Key, API Secret and your cloud name as they are displayed on the API Keys page. 

You will have to reveal API secret via OTP pass sent to your email.

## Heroku Deployment

* Set up a local workspace on your computer for Heroku:
    - Create a list of requirements that the project needs to run:
      - type this in the terminal: `pip3 freeze > requirements.txt`
    - Commit and push the changes to GitHub
    
* Go to [www.heroku.com](www.heroku.com) 
* Log in or create a Heroku account.
* Create a new app with any unique name <name app>.

* Create a Procfile in your local workplace:
    
    This file will will contain the following:
    ```python
        web: gunicorn <name app>.wsgi:application
    ```
    - Commit and push the changes to GitHub.

* Go to resources in Heroku and search for postgresql. Select Hobby dev - Free and click on the provision button to add it to the project.

* Go to the settings app in Heroku and go to Config Vars.


Click on Reveal Config Vars and add the following config variables:

| Key      | Value          | Note |
| --------- | --------- | -------- |
| CLOUDINARY_URL | ... | if you use Cloudinary for media files hosting |
| DATABASE_URL | ... | API for whatever postgres database you employ |
| DISABLE_COLLECTSTATIC | 1 | Heroku will not run collectstatic with each deployment |
| EMAIL_HOST_PASSWORD | ... | |
| EMAIL_HOST_USER | ... | |
| DEFAULT_FROM_EMAIL | ... | |
| SECRET_KEY | ... | |
| DEBUG | FALSE | so manage.py know what settings to use in production - appropriate logic set in manage.py |


* Migrate changes.
* Commit and push the changes to GitHub.
* Connect your repository to Heroku in Deployment tab of your Heroku project page.
* Deploy the app to Heroku by clicking "Deploy Branch" button. If you want to enable auto-deployment, click "Enable Automatic Deployment".


**Final Deployment**

* There is no need to set DEBUG to FALSE in your .env file on the local computer as my manage.py logic assumes that DEBUG must be explicitly added to the environment variables on your production server and set to False.  
* delete DISABLE_COLLECTSTATIC from config vars in Heroku dashboard.
* Commit and push the changes to GitHub.


---