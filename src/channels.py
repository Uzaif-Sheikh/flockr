'''
H15 Orange, Group 3

Implementation of channels.py functions as specified on the
assignment 1 spec.

Iteration 1
'''

from error import InputError
from error import AccessError
from data import get_uid, get_list, get_listall, create_channel, check_valid_token

def channels_list(token):
    '''
    Channels list returns the list of channels user
    in part of from the data file (data.py)
    '''

    channels_list_exception(token)

    channels = get_list(token)

    return {
        'channels': channels
    }

def channels_listall(token):
    '''Channels listall returns the list of channels
    from the data file (data.py)
    '''

    channels_listall_exception(token)

    channels = get_listall(token)

    return {
        'channels': channels
    }

def channels_create(token, name, is_public):
    '''
    Creates a channel and append it at the end of the list of data['channels']
    '''

    #Exception handling
    channels_create_exception(token, name)

    channel_id = create_channel(token, name, is_public)

    return {
        'channel_id': channel_id
    }

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def channels_list_exception(token):
    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def channels_listall_exception(token):
    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def channels_create_exception(token, name):
    '''Exception handling for channels_create_exception'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if len(name) > 20 or len(name) == 0:
        raise InputError(description='Name should be less than 20 characters.')





