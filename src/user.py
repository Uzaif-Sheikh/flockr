'''
H15C, Group 3
User account features, iteration 2.
'''

import urllib.request
from flask import request
import requests
from PIL import Image
from io import BytesIO
from error import InputError, AccessError
from data import check_valid_user_id, get_token, get_uid, check_email_in_use, \
                check_valid_email, check_valid_first_last_name, get_profile, \
                setname, setemail, sethandle, handle_search, check_valid_token, \
                crop_image, set_profile_url

def user_profile(token, u_id):
    '''
    For a valid user, returns information about their user_id, email,
    first name, last name, and handle
    '''
    u_id = int(u_id)

    # Check for exception handling
    profile_exception(token, u_id)

    # Get user data
    profile = get_profile(u_id)

    return profile

def user_profile_setname(token, name_first, name_last):
    '''For a valid first name and last name updates the users first and
    last name
    '''
    # Checking for the validity of the first and last name
    profile_setname_exception(token, name_first, name_last)

    setname(token, name_first, name_last)

    return {
    }

def user_profile_setemail(token, email):
    '''Implementation of the user profile setmail function with error handling'''

    # Exception handling
    user_setemail_valid_exception(token, email)
    user_setemail_use_exception(email)

    setemail(token, email)

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    for a valid hanld_str which is between 3 and 20 characters, and unique for user
    update the handle_str
    '''
    #checking for the validity of the handle
    sethandle_exception(token, handle_str)

    sethandle(token, handle_str)

    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image within
    bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
    '''

    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    profile_uploadphoto_exception(token, img_url, x_start, y_start, x_end, y_end)

    image_name = crop_image(img_url, x_start, y_start, x_end, y_end)

    set_profile_url(token, image_name)

    return {}

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def sethandle_exception(token, handle_str):
    '''
    Input error checking for sethandle feature
    '''

    # Raising InputError if the length of handle_str less than 3 or larger than 20
    if len(handle_str) < 3:
        raise InputError(description="Too short handle String")
    if len(handle_str) > 20:
        raise InputError(description="Too long handle String")

    # Raising InputError if the handle_str already exists
    if handle_search(handle_str) == True:
        raise InputError(description="This handle is already used")

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def user_setemail_use_exception(email):
    '''Exception handling for email that is already in use'''

    if check_email_in_use(email):
        raise InputError(description="Email already in  use")

def user_setemail_valid_exception(token, email):
    '''Exception handling for invalid email entry'''

    if not check_valid_email(email):
        raise InputError(description="Invalid Email format")

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def profile_exception(token, u_id):
    '''Raise Errors when invalid parameters are passed in'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when u_id does not refer to a valid user
    if not check_valid_user_id(u_id):
        raise InputError(description="Invalid User ID")

    # Raise InputError if authorised user is invalid
    if not check_valid_user_id(get_uid(token)):
        raise InputError(description="Not an Authorised User")

def profile_setname_exception(token, name_first, name_last):
    '''
    Raising InputError if first name is invalid
    or InputError if last name is invalid
    '''

    if not check_valid_first_last_name(name_first):
        raise InputError(description="Invalid First Name")


    if not check_valid_first_last_name(name_last):
        raise InputError(description="Invalid Last Name")

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def profile_uploadphoto_exception(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Raising InputError/AccessError when unwanted action is taken
    '''

    # img_url returns an HTTP status other than 200.
    try:
        status = urllib.request.urlopen(img_url).getcode()
        if status != 200:
            raise InputError(description="Image not 200 boss")
    except:
        raise InputError(description="Image not 200 boss")

    # Image uploaded is not a JPG by checking if .jpg is in URL
    if ".jpg" not in img_url:
        raise InputError(description="JPG not in image url")

    # get dimensions of image
    data = requests.get(img_url).content
    im = Image.open(BytesIO(data))
    width, height = im.size

    # any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
    if x_start > width or x_end > width or x_start < 0 or x_end < 1:
        raise InputError(description="Too wide")
    elif y_start > height or y_end > height or y_start < 0 or y_end < 1:
        raise InputError(description="Too long")

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
