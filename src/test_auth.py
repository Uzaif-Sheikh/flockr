'''
H15 Orange, Team 3

Implementation of test_auth.py functions for
assignment 1 spec. Iteration 1
'''


import pytest
from other import clear
from auth import auth_login, auth_register, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from channels import channels_create
from channel import channel_invite, channel_join
from error import InputError, AccessError

def test_auth_register_login_new():

    '''
    This function tests the auth_register functionality /
    '''

    clear()

    result = auth_register('bob@gmail.com', 'ilovemeatballs', 'bob', 'lin')
    token = result['token']

    #checking that login for a newly registed user
    # returns the same uid, token pair initially when the user logins.

    assert auth_login('bob@gmail.com', 'ilovemeatballs') == result

    assert auth_logout(token) == {'is_success': True}

    #logout should be successful if user is already in

    with pytest.raises(AccessError):
        auth_logout(token)

    #logout should fail if user is not logged in \

    result1 = auth_register('shubhbamjohar123@gmail.com', 'heismad', 'shubham', 'johar')
    token1 = result1['token']

    assert auth_login('shubhbamjohar123@gmail.com', 'heismad') == result1

    #checking for login for a registed user \

    assert auth_logout(token1) == {'is_success': True}

    #logout should be successful if user is already in \

    with pytest.raises(AccessError):
        auth_logout(token)

    #logout should fail if user is not logged in \

    with pytest.raises(AccessError):
        auth_logout(token)

    #logout check for already logged out user \

    result2 = auth_register('bob124@gmail.com', 'ilovemeatballs', 'bobi', 'lin')
    token2 = result2['token']

    assert auth_login('bob124@gmail.com', 'ilovemeatballs') == result2

    #checking for login for a registed user

    assert auth_logout(token2) == {'is_success': True}

    #logout should be successful if user is already in


    with pytest.raises(AccessError):
        auth_logout(token)

    #logout should fail if user is not logged in

    # checking that the uid, token pair returned is same \
    # if the user tries to login again if he is already logged in
    result_bob_login = auth_login('bob124@gmail.com', 'ilovemeatballs')

    result_bob_again_login = auth_login('bob124@gmail.com', 'ilovemeatballs')

    assert result_bob_again_login == result_bob_login

    assert auth_logout(result_bob_again_login['token']) == {'is_success' : True}

    #testing that after the user has logged out, is he still able to access the other stuff

    result_shubham_login_again = auth_login('shubhbamjohar123@gmail.com', 'heismad')

    token_shubham = result_shubham_login_again['token']

    channel_phy5678_details = channels_create(token_shubham, 'PHY5678', False)

    channel_id_phy5678 = channel_phy5678_details['channel_id']

    with pytest.raises(AccessError):
        channel_invite(result_bob_again_login['token'], \
                               channel_id_phy5678, result_shubham_login_again['u_id'])

    assert auth_logout(token_shubham) == {'is_success' : True}

    # result_bob_again = auth_login('bob@gmail.com', 'ilovemeatballs')

    with pytest.raises(AccessError):
        channel_join(result_shubham_login_again['token'], channel_id_phy5678)

def test_auth_register_exception():

    '''
    This function tests all the exception //
    handling of auth_register function.
    '''

    clear()
    auth_register('123@gmail.com', '$56$@3', 'usmaan', 'chandhok')
    auth_register('hi123@gmail.com', '4321!@#$', 'hayden', 'smith')
    auth_register('manboss@gmail.com', 'iamboss123', 'man', 'boss')
    auth_register('kingchandhok@gmail.com', 'sleepingbeauty', 'king', 'chandhok')
    auth_register('uzaifsheikh69@gmail.com', 'heiscool', 'uzaif', 'sheikh')

    # checking for InputError with Invaild email

    with pytest.raises(InputError):

        auth_register('bobgamil.com', '1234!@#$', 'bob', 'lima')

    with pytest.raises(InputError):

        auth_register('123@.com', '753951', 'usmaan', 'chandhok')

    with pytest.raises(InputError):

        auth_register('7890', '12<>2134', 'hayden', 'smith')

    with pytest.raises(InputError):

        auth_register('usmaan', '3451236', 'iamusmaan', 'boss')

    # checking for InputError with email already used by another user

    with pytest.raises(InputError):

        auth_register('123@gmail.com', '4567123', 'uzaif', 'sheikh')

    with pytest.raises(InputError):

        auth_register('manboss@gmail.com', '2345123', 'bob', 'boss')

    with pytest.raises(InputError):
        auth_register('kingchandhok@gmail.com', 'sleepingbeauty', 'king', 'chandhok')

    with pytest.raises(InputError):

        auth_register('Uzaifsheikh69@gmail.com', 'heiscool', 'uzaif', 'sheikh')


    # checking for InputError with password less that 6 character

    with pytest.raises(InputError):

        auth_register('one@gamil.com', '1', 'cold', 'play')

    with pytest.raises(InputError):

        auth_register('two@gamil.com', '12345', 'xu', 'gao')

    with pytest.raises(InputError):

        auth_register('three3@gamil.com', 'iopt', 'frankie', 'thefox')

    with pytest.raises(InputError):

        auth_register('four4@gmail.com', '!@#', 'lady', 'gaga')


    # checking for InputError with Invaild first and last name

    with pytest.raises(InputError):

        auth_register('five5@gmail.com', 'iamfive', '', '')

    with pytest.raises(InputError):

        auth_register('six6@gmail.com', 'iamsix66', '66', '')

    with pytest.raises(InputError):

        auth_register('seven7@gmail.com', 'iamseven7', '', '8888')

    with pytest.raises(InputError):

        auth_register('nine9@gmail.com', 'iamnine9', \
                           'aaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssshhhhhhhh', 'king')

    with pytest.raises(InputError):

        auth_register('ten10@gmail.com', 'iamten10', 'chris', \
                           'bbbbbbbbbbbbbrrrrrrrrrrrrroooooooooowwwwwwwwwwnnnnnnnnn')

    with pytest.raises(InputError):

        auth_register('iamcool@gmail.com', 'iamthebestperson', \
                           'estimatinggggthesilencefotheworldaroundusisanewnormandweneedtocheck'
                           'thesameforallofus', \
                           'inequality')


def test_auth_login_exception():

    '''
    This function tests the exception handling \\
    of the auth_login function.
    '''

    clear()
    auth_register('123@gmail.com', '4321!@#$', 'hayden', 'smith')
    auth_register('usmaanboss@gmail.com', 'iamboss123', 'usmaan', 'boss')
    auth_register('hello@gmail.com', 'helloworld', 'usmaan', 'boss')
    auth_register('xugaoissmart@gmail.com', 'iamcool', 'xu', 'gao')



    # checking for InputError with Invaild email

    with pytest.raises(InputError):

        auth_login('123gamil.com', '4321!@#$')

    with pytest.raises(InputError):

        auth_login('usmaanboss@.com', 'iamboss123')

    with pytest.raises(InputError):

        auth_login('123', 'iamboss123')

    with pytest.raises(InputError):

        auth_login('boss', '4321!@#$')


    # Giving the email not belong to any user

    with pytest.raises(InputError):

        auth_login('123_4@gmail.com', '4321!@#$')

    with pytest.raises(InputError):

        auth_login('usmaanbosss@gmail.com', 'iamboss123')

    with pytest.raises(InputError):

        auth_login('bob@yahoo.com', 'gmailisbetter')

    with pytest.raises(InputError):

        auth_login('xugaoistherealboss@gmail.com', 'iamxu')

    # checking for InputError with incorrect password

    with pytest.raises(InputError):

        auth_login('123@gmail.com', '4321!@#$345')

    with pytest.raises(InputError):

        auth_login('usmaanboss@gmail.com', 'iamnotboss123')

    with pytest.raises(InputError):

        auth_login('hello@gmail.com', 'HelloWorld')

    with pytest.raises(InputError):

        auth_login('hello@gmail.com', '4321!@#$')

    with pytest.raises(InputError):

        auth_login('123@gmail.com', 'iamboss123')

def test_auth_logout_exception():
    '''
    An AccessError must be raised for any invalid token.
    '''
    clear()

    with pytest.raises(AccessError):
        auth_logout(123)

def test_auth_pasauth_passwordreset_reset_InputError():
    '''
    Test the inputerrors for password reset
    '''

    clear()

    result = auth_register('bob@gmail.com', 'ilovemeatballs', 'bob', 'lin')
    token = result['token']

    auth_logout(token)

    auth_passwordreset_request('bob@gmail.com')

    with pytest.raises(InputError):
        auth_passwordreset_reset('notcorrectlol', 'iforgotmypassword')

def test_auth_pasauth_passwordreset_request():
    '''
    Test the inputerrors for password reset
    '''

    clear()

    result = auth_register('bob@gmail.com', 'ilovemeatballs', 'bob', 'lin')
    token = result['token']

    auth_logout(token)

    with pytest.raises(InputError):
        auth_passwordreset_request('invalid@gmail.com')