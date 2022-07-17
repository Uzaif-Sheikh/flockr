'''
H15C, Group 3
Testing user features.
'''

import pytest
from other import clear
from auth import auth_register
from error import InputError, AccessError
from user import user_profile, user_profile_setname, user_profile_setemail, \
                user_profile_sethandle, user_profile_uploadphoto


@pytest.fixture(name='users')
def fixture_users():
    '''This is a pytest fixture used to define some user variables required for testing
    in all functions'''

    # Here, we assume that the auth_register function works perfectly

    clear()

    # Creating user Bob, the Flockr owner
    bob = auth_register('bob@gmail.com', 'ilovemeatballs', 'bob', 'lin')
    u_id_bob = bob['u_id']
    token_bob = bob['token']

    # Create member Marley
    marley = auth_register('marley@gmail.com', 'ilovecheese', 'marley', 'lin')
    u_id_marley = marley['u_id']
    token_marley = marley['token']

    # Create member Shubham
    shubham = auth_register('shubham@gmail.com', 'ilovetoswim', 'shubham', 'johar')
    u_id_shubham = shubham['u_id']
    token_shubham = shubham['token']

    # Create member Smith
    result_smith = auth_register('123@gmail.com', '4321!@#$', 'hayden', 'smith')
    u_id_smith = result_smith['u_id']
    token_smith = result_smith['token']

    # Create member Uzaif
    uzi = auth_register('uzisheikh@gmail.com', 'ilovekebab', 'uzaif', 'sheikh')
    u_id_uzaif = uzi['u_id']
    token_uzaif = uzi['token']

    return {'bob': [u_id_bob, token_bob], 'marley': [u_id_marley, token_marley],
            'shubham': [u_id_shubham, token_shubham], 'smith': [u_id_smith, token_smith],
            'uzi': [u_id_uzaif, token_uzaif]}

def test_user_profile_inputerror(users):
    ''' Test all possible InputError cases for user_profile'''

    # Generate invalid u_id by adding arbitrary numbers to the only valid u_id available
    invalid_u_id_a = users['shubham'][0] + 20
    invalid_u_id_b = users['shubham'][0] + 30
    invalid_u_id_c = users['shubham'][0] + 40

    # Checking for InputError with u_id that does not refer to a valid user
    with pytest.raises(InputError):
        user_profile(users['bob'][1], invalid_u_id_a)

    with pytest.raises(InputError):
        user_profile(users['bob'][1], invalid_u_id_b)

    with pytest.raises(InputError):
        user_profile(users['bob'][1], invalid_u_id_c)

def test_user_profile_functionality(users):
    '''Make sure the user_profile returns the right results'''

    result = {
        'user': {
            'u_id': users['bob'][0],
            'email': 'bob@gmail.com',
            'name_first': 'bob',
            'name_last': 'lin',
            'handle_str': 'boblin',
            'profile_img_url': '',
        },
    }

    assert user_profile(users['bob'][1], users['bob'][0]) == result

def test_user_profile_setname_inputerrors(users):
    '''Testing that input error raises exception on invalid cases'''

    # Raising exception when either First or Last name is empty
    with pytest.raises(InputError):
        user_profile_setname(users['shubham'], '', '')

    with pytest.raises(InputError):
        user_profile_setname(users['marley'], '', 'lin')

    with pytest.raises(InputError):
        user_profile_setname(users['bob'], 'bob', '')

    # Raising exception when either First or Last name is more than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(users['marley'], 'marley',
                             'checkingwhenthelastnamelengthismorethanfiftycharacters')

    with pytest.raises(InputError):
        user_profile_setname(users['bob'],
                             'checkingforexceptionerrorswhenfirstnameismorethatfiftychars', 'lin')

def test_user_profile_setname(users):
    '''Testing that user_profile_setname functions successfully updates First and Last name'''

    result_first_name = {
        'user': {
            'u_id': users['bob'][0],
            'email': 'bob@gmail.com',
            'name_first': 'Xu',
            'name_last': 'lin',
            'handle_str': 'boblin',
            'profile_img_url': '',
        }
    }

    # Updating user bob's first name
    user_profile_setname(users['bob'][1], 'Xu', 'lin')

    assert user_profile(users['bob'][1], users['bob'][0]) == result_first_name

    result_last_name = {
        'user' : {
            'u_id': users['bob'][0],
            'email': 'bob@gmail.com',
            'name_first': 'bob',
            'name_last': 'sheikh',
            'handle_str': 'boblin',
            'profile_img_url': '',
        }
    }

    # Updating user bob's last name
    user_profile_setname(users['bob'][1], 'bob', 'sheikh')

    assert user_profile(users['bob'][1], users['bob'][0]) == result_last_name

    result_first_last_name = {
        'user' : {
            'u_id': users['bob'][0],
            'email': 'bob@gmail.com',
            'name_first': 'Batman',
            'name_last': 'Robin',
            'handle_str': 'boblin',
            'profile_img_url': '',
        }
    }

    # Updating User bob's first and last name
    user_profile_setname(users['bob'][1], 'Batman', 'Robin')

    assert user_profile(users['bob'][1], users['bob'][0]) == result_first_last_name

def test_user_profile_setemail_inputerrors(users):
    '''Testing that input error raises exception on invalid cases'''

    # Raising exception when email is of invalid format
    with pytest.raises(InputError):
        user_profile_setemail(users['shubham'][1], 'shubham')

    with pytest.raises(InputError):
        user_profile_setemail(users['marley'][1], 'lin@')

    with pytest.raises(InputError):
        user_profile_setemail(users['bob'][1], 'bob@gmail.python')

    with pytest.raises(InputError):
        user_profile_setemail(users['shubham'][1], '')

    with pytest.raises(InputError):
        user_profile_setemail(users['smith'][1], 'smith.com')

    # Raising exception when email is already in use
    with pytest.raises(InputError):
        user_profile_setemail(users['marley'][1], '123@gmail.com')

    with pytest.raises(InputError):
        user_profile_setemail(users['bob'][1], 'shubham@gmail.com')

    with pytest.raises(InputError):
        user_profile_setemail(users['uzi'][1], 'marley@gmail.com')

def test_user_profile_setemail(users):
    '''Testing that user_profile_setemail functions successfully updates user's email'''

    result_email = {
        'user' : {
            'u_id': users['uzi'][0],
            'email': 'uzaifsheikh@gmail.com',
            'name_first': 'uzaif',
            'name_last': 'sheikh',
            'handle_str': 'uzaifsheikh',
            'profile_img_url': '',
        }
    }

    # Updates uzi's email to uzaifsheikh@gmail.com
    user_profile_setemail(users['uzi'][1], 'uzaifsheikh@gmail.com')

    assert user_profile(users['uzi'][1], users['uzi'][0]) == result_email

def test_user_profile_sethandle_inputerrors(users):
    '''
    Testing that input errors raise exception on invalid cases
    '''
    # Generate invalid handle_str by adding 24 characters to the only valid handle_str available
    invalid_handle_str_a = 'shubham' + 'abcdefghijklmnopqretuvwxyz'
    invalid_handle_str_b = 'marley' + 'abcdefghijklmnopqretuvwxyz'
    invalid_handle_str_c = 'bob' + 'abcdefghijklmnopqretuvwxyz'

    #Raising exception when handle_str is less than 3 characters
    with pytest.raises(InputError):
        user_profile_sethandle(users['shubham'][1], '')
    with pytest.raises(InputError):
        user_profile_sethandle(users['shubham'][1], 'a')
    with pytest.raises(InputError):
        user_profile_sethandle(users['shubham'][1], 'ab')

    #Raising exception when handle_str is more than 20 characters
    with pytest.raises(InputError):
        user_profile_sethandle(users['shubham'][1], invalid_handle_str_a)
    with pytest.raises(InputError):
        user_profile_sethandle(users['marley'][1], invalid_handle_str_b)
    with pytest.raises(InputError):
        user_profile_sethandle(users['bob'][1], invalid_handle_str_c)

    #Raising exception when handle_str is already used by another user
    with pytest.raises(InputError):
        user_profile_sethandle(users['shubham'][1], 'boblin')
    with pytest.raises(InputError):
        user_profile_sethandle(users['marley'][1], 'boblin')

def test_user_profile_sethandle(users):
    '''
    Testing that user_profile_sethandle function successfully updates user's handle
    '''

    # create a user bob with all details
    result_handle_str_one = {
        'user': {
            'u_id': users['bob'][0],
            'email': 'bob@gmail.com',
            'name_first': 'bob',
            'name_last': 'lin',
            'handle_str': 'bobbylinny',
            'profile_img_url': '',
        }
    }

    #update user bob's handle_str
    user_profile_sethandle(users['bob'][1], 'bobbylinny')

    assert user_profile(users['bob'][1], users['bob'][0]) == result_handle_str_one

def test_user_profile_upload_photo_InputError(users):
    '''
    InputError when any of:
        img_url returns an HTTP status other than 200.
        any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
        Image uploaded is not a JPG
    '''

    png_url = "https://i.pinimg.com/originals/57/a3/ea/57a3ea3c3a56f8d0f0ff08f744a08b10.png"
    jpg_url = "https://images.immediate.co.uk/production/volatile/sites/3/2019/07/Shrek-2-2e51949.jpg?quality=90&crop=65px%2C0px%2C608px%2C405px&resize=608%2C405"
    not_200_url = "https://pmcvariety.files.wordpress.com/2015/07/naruto_movie-lionsgate.jpg?w=1000"

    with pytest.raises(InputError):
        # img_url returns an HTTP status other than 200.
        user_profile_uploadphoto(users['bob'][1], not_200_url, "0", "0", "100", "100")

    with pytest.raises(InputError):
        # Image uploaded is not a JPG
        user_profile_uploadphoto(users['bob'][1], png_url, "0", "0", "100", "100")

    
        # any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
    with pytest.raises(InputError):

        user_profile_uploadphoto(users['bob'][1], jpg_url, "1000", "0", "100", "100")
    
    with pytest.raises(InputError):
        
        user_profile_uploadphoto(users['bob'][1], jpg_url, "0", "1000", "100", "100")
        
    with pytest.raises(InputError):

        user_profile_uploadphoto(users['bob'][1], jpg_url, "0", "0", "1000", "100")
        
    with pytest.raises(InputError):

        user_profile_uploadphoto(users['bob'][1], jpg_url, "0", "0", "100", "1000")
        

def test_user_profile_exception(users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        user_profile(123, users['bob'][0])

def test_user_profile_setemail_exception(users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        user_profile_setemail(123, 'shubham@gmail.com')

def test_user_profile_sethandle_exception(users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        user_profile_sethandle(123, 'yeet')

def test_user_profile_setname_exception(users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        user_profile_setname(123, 'Xu', 'lin')

def test_user_profile_upload_photo_excpetion(users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        user_profile_uploadphoto(123, "https://images.immediate.co.uk/production/volatile/sites/3/2019/07/Shrek-2-2e51949.jpg?quality=90&crop=65px%2C0px%2C608px%2C405px&resize=608%2C405", "300", "300", "400", "400")
