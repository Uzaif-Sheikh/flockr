'''
H15 Orange, Team 3

Implementation of auth.py functions for
assignment 1 spec. Iteration 1
'''

from error import InputError, AccessError
from data import handle_search, check_email, used_email, find_user_id, get_token, \
                find_password_registered, update_token_user, logout, login, register, \
                check_valid_token, passwordreset_request, data_get_reset_email, \
                passwordreset_reset, data_get_user_name, data_add_reset_pair, \
                data_get_reset_email, data_remove_reset_request, data_set_password


def auth_login(email, password):

    '''
    This function takes in email and password of a register user and //
    returns a unique id and token for that login time.
    '''

    auth_login_exception(email, password)

    unique_user = login(email, password)

    return unique_user

def auth_logout(token):

    '''
    This function takes in token for a user who is already logged in and //
    sets their token to None to end their current session and returns True or False.
    '''

    auth_logout_exception(token)

    logout_token = logout(token)

    if logout_token == True:
        return {'is_success' : True}

    return {'is_success' : False}

def auth_register(email, password, name_first, name_last):

    '''
    This function takes in email, password, first name, last name of a user and //
    and register the user and return a unique id and token.
    '''

    #checks for all the exceptions initially.
    auth_register_exception(email, password, name_first, name_last)

    register_details = register(email, password, name_first, name_last)

    return register_details

def auth_passwordreset_request(email):
    '''
    This function takes in email of a register user and send an send //
    an secret code to their email
    '''
    password_reset_exception(email)

    passwordreset_request(email)

def auth_passwordreset_reset(reset_code, new_password):
    '''
    This function takes in reset_code and new_password of a user //
    and update their password
    '''

    auth_passwordreset_reset_exception(reset_code, new_password)

    passwordreset_reset(reset_code, new_password)

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def auth_logout_exception(token):
    '''
    AccessError when token doesn't refer to a valid user
    '''

    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def auth_register_exception(email, password, name_first, name_last):

    '''
    This funtion take email, password, first name, last name and check for //
    an exception and raises it.
    '''

    if check_email(email) is False:
        raise InputError(description='Invalid E-mail id')

    if used_email(email) is True:
        raise InputError(description='E-mail id already used.')

    if len(password) < 6:
        raise InputError(description='Password must contain more than 6 characters.')

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First_name should be between 1 to 50 characters.')

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description='Last_name should be between 1 to 50 characters.')

def auth_login_exception(email, password):

    '''
    This funtion take email, password and check for //
    an exception and raises it.
    '''

    if check_email(email) is False:
        raise InputError('Invalid E-mail id')

    if used_email(email) is False:
        raise InputError('''Unregistered email.''')

    if find_password_registered(email, password) is False:
        raise InputError('Incorrect password')

def auth_passwordreset_reset_exception(reset_code, new_password):
    '''
    Raise InputError if:
        reset_code is not a valid reset code
        Password entered is not a valid password
    '''
    if data_get_reset_email(reset_code) == None:
        raise InputError(description='Incorrect reset code')

    if len(new_password) < 6:
        raise InputError(description='Password must contain more than 6 characters.')


def password_reset_exception(email):
    '''
    Raise an InputError if the email doesn't
    refer to a registered user

    THIS EXCEPTION IS NOT SPECIFIED BY THE SPEC BUT IS
    IMPLEMENTED IN THE EXAMPLAR FLOCKR APP
    '''

    if used_email(email) is False:
        raise InputError('''Unregistered email''')
