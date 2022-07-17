'''
H15C, Group 3
Messaging Features Implementation
'''

from error import InputError, AccessError
from data import get_uid, is_member, send_later, check_time_sent, \
                check_valid_channel_id, check_message_exsits, pin_message, \
                unpin_message, get_channel_id, already_pinned, sent_message_user, \
                check_react_exists, is_owner, add_react_message, add_unreact_message, \
                is_flockr_owner, send_message, remove_message, edit_message, \
                check_valid_token

def message_send(token, channel_id, message):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    channel_id = int(channel_id)

    send_exception_handling(token, message, get_uid(token), channel_id)

    message_id = send_message(token, channel_id, message, get_uid(token))

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''

    message_id = int(message_id)

    remove_exception_handling(token, message_id, get_uid(token))

    remove_message(token, message_id)

    return {
    }

def message_edit(token, message_id, message):
    '''Given a message_id for a message, this function will update
       the message with new message and returns nothing '''

    message_id = int(message_id)

    edit_exception_handling(token, message_id, get_uid(token))

    edit_message(token, message_id, message)

    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''Given message from user to the channel specified by
        channel_id is send at the time in future '''

    sendlater_exception(token, channel_id, message, time_sent)

    message_id = send_later(token, channel_id, message, time_sent)

    return {
        'message_id': message_id,
    }

def message_react(token, message_id, react_id):
    '''Given message from user to the channel specified by
        channel_id is send at the time in future '''

    react_exception_handling(token, message_id, react_id)

    add_react_message(token, message_id, react_id)

    return {
    }

def message_unreact(token, message_id, react_id):
    '''Given the message by message_id it unreact'''

    unreact_exception_handling(token, message_id, react_id)

    add_unreact_message(token, message_id, react_id)

    return{
    }

def message_pin(token, message_id):
    '''Given the token for a user and message_id for a message
        it will pin the message'''

    pin_exception_handling(token, message_id)

    pin_message(message_id)

    return {
    }

def message_unpin(token, message_id):
    '''Given the token for a user and message_id for a message
        it will unpin the message'''

    unpin_exception_handling(token, message_id)

    unpin_message(message_id)

    return {
    }

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def send_exception_handling(token, message, uid_user, channel_id):
    '''Checks for the exception handling cases for sending the messages'''

    #Raise an input error if the length of the message is more than 1000.
    if len(message) > 1000:
        raise InputError(description='Message too long.')

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
    
    # AccessError when Authorised user is not a member of channel with
    # channel_id
    if not is_member(channel_id, uid_user):
        raise AccessError(description='User Not a member of the Channel')

def remove_exception_handling(token, message_id, uid_user):
    '''Checks for the exception handling cases for removing the messages'''

    #Raise an InputError, when the message no longer exists.
    if check_message_exsits(message_id) is False:
        raise InputError(description='Message does not exists')

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    #Raise an AccessError, if the user asking for the request to
    # remove the message has not sent the message themselves

    if sent_message_user(uid_user, message_id) is False \
    and is_owner(message_id, uid_user) is False and \
    is_flockr_owner(uid_user) is False:
        raise AccessError(description='User can''t remove the message')

def edit_exception_handling(token, message_id, uid_user):
    '''Checking for expcetion for the function edit'''
    
    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
    
    #Raise an AccessError, if the user asking for the request to
    # remove the message has not sent the message themselves

    if sent_message_user(uid_user, message_id) is False \
    and is_owner(message_id, uid_user) is False and \
    is_flockr_owner(uid_user) is False:
        raise AccessError(description="User can't edit the message")

def sendlater_exception(token, channel_id, message, time_sent):
    '''Checking for expcetion for the function sendlater '''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if len(message) > 1000:
        raise InputError(description='Message is too long')

    if not check_valid_channel_id(channel_id):
        raise InputError(description='Invalid channel_id')

    if check_time_sent(time_sent) is False:
        raise InputError(description='Time is not Valid')

    if not is_member(channel_id, get_uid(token)):
        raise AccessError(description='User Not a member of the Channel')


def react_exception_handling(token, message_id, react_id):
    '''Checking for the exeptions with message_react'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if not check_message_exsits(message_id):
        raise InputError(description='THis message was not sent on this channel.')

    if react_id != 1:
        raise InputError(description= 'There is no react matchign this id.')

    if check_react_exists(get_uid(token), message_id):
        raise InputError(description= 'The user has already reacted on the message.')

def unreact_exception_handling(token, message_id, react_id):
    '''Checking for the exeptions with message_react'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if not check_message_exsits(message_id):
        raise InputError(description='THis message was not sent on this channel.')

    if react_id != 1:
        raise InputError(description= 'There is no react matchign this id.')

    if check_react_exists(get_uid(token), message_id) is False:
        raise InputError(description= 'The user has already reacted on the message.')

def pin_exception_handling(token, message_id):
    '''Checking the exception for the pin function'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if check_message_exsits(message_id) is False:
        raise InputError(description='THis message was not sent on this channel.')

    if already_pinned(message_id):
        raise InputError(description='THis message is already pinned.')

    if is_member(get_channel_id(message_id), get_uid(token)) is False:
        raise AccessError(description='User Not a member of the Channel')

    if is_owner(get_channel_id(message_id), token) is False:
        raise AccessError(description='User Not a Owner of the Channel')

def unpin_exception_handling(token, message_id):
    '''Checking the exception for the pin function'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    if check_message_exsits(message_id) is False:
        raise InputError(description='THis message was not sent on this channel.')

    if is_member(get_channel_id(message_id), get_uid(token)) is False:
        raise AccessError(description='User Not a member of the Channel')

    if is_owner(get_channel_id(message_id), token) is False:
        raise AccessError(description='User Not a Owner of the Channel')

    if already_pinned(message_id) is False:
        raise InputError(description='This message is already unpinned.')
