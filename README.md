# Project - Image upload service
#### Test task for Mediasoft
###
## The service provides the ability to upload user images
## The user can:
- Upload images with post header
- View images from the gallery
- Delete them
## The admin user can:
- Block user accounts
- Delete user accounts
- View user posts
- Edit and delete them
- Create user accounts
- Create admin user accounts
###
## To check:
1. Clone the project from repository
    #### $ git clone https://github.com/Reeftor/Mediasoft_job_test.git -b develop
2. Go to project directory and install requirements
    #### $ pip install -r requirements.txt 
   or
    #### $ python3 -m pip install -r requirements.txt
3. Go to /testproject directory and create your admin account
    #### $ manage.py createsuperuser
   or
    #### $ python3 manage.py createsuperuser
4. Run server
    #### $ manage.py runserver
   or
    #### $ python3 manage.py runserver
5. Open browser and go to http://127.0.0.1:8000
#
### Project developed by Dmitry Lotarev
