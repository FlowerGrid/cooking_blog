from .db import db_session
from .models import User

def init_cli(app):
    @app.cli.command('create-user')
    def create_user():
        print('Provide user credentials. To QUIT type "q".')
        creds = prompt_user_creds()

        if creds is None:
            print('User creation cancelled.')
            return
        
        add_user_to_db(*creds)


def prompt_user_creds():
    while True:
        username = input('Username: ')
        if username.lower() =='q':
            return
        
        email = input('Email: ')
        if email.lower() =='q':
            return
        password = input('Password: ')
        if password.lower() =='q':
            return
        
        re_password = input('Re-enter Password: ')
        if re_password.lower() == 'q':
            return

        if password == re_password:
            return (username, email, password)
        else: 
            print('Passwords did not match. Try again\n')


def add_user_to_db(username, email, password):
    user = User(
        username=username.lower(),
        email=email.lower()
        )
    user.set_password(password)

    db_session.add(user)
    db_session.commit()