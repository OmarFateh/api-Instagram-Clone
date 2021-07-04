# Instagram Clone API
> Instagram clone API made with django framework and django API rest framework.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [TODO](#TODO)


## Technologies
* Python 3.9
* Django 2.2.19
* Django Rest Framework 3.12.2

## Setup
The first thing to do is to clone the repository:  
`$ git clone https://github.com/OmarFateh/api-Instagram-Clone.git`  
Setup project environment with virtualenv and pip.  
`$ virtualenv project-env`  
Activate the virtual environment  
`$ source project-env/Scripts/activate`  
Install all dependencies  
`$ pip install -r requirements.txt`  
Run the server  
`py manage.py runserver`

## Features
* Authentication: Registeration, login, logout, change and reset password.
* A user can have a private account, can follow other users and followed by them as well.
* A user can view all images of his following, like them and add/update/delete comments. 
* A user can add/update/delete an image with hashtags and caption.
* A user can tag other users in his image.
* A user gets notification when other users tag him, like his image or add a comment to his image.
* A user can view all his tagged images.
* A user can images to his favourite list.
* A user can view all his favourite list images.
* A user can explore and view images of other profiles, with whom there's mutual friends.

## TODO
* Implement Stories
* Implement Direct Messages (DM)
