'''
H15 Orange, Group 3

Implementation of channel.py functions as specified on the
assignment 1 spec.

Iteration 1
'''
from error import InputError, AccessError
from data import add_member, get_channel_details, get_messages, leave, join, \
                remove_owner, check_valid_channel_id, check_valid_user_id, \
                is_member, is_owner, get_uid, get_token, add_owner, is_public, \
                is_flockr_owner, add_flockr_owner, check_start_greater, \
                check_valid_token


def channel_invite(token, channel_id, u_id):
    '''Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately'''

    u_id = int(u_id)
    channel_id = int(channel_id)

    # Check exception errors
    invite_exception_handling(token, channel_id, u_id)

    join(get_token(u_id), channel_id)

def channel_details(token, channel_id):
    '''Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel'''

    channel_id = int(channel_id)

    # Check exception errors
    details_exception_handling(get_uid(token), channel_id)

    return get_channel_details(channel_id)


def channel_messages(token, channel_id, start):
    '''Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".'''

    channel_id = int(channel_id)
    start = int(start)

    # Check exception errors
    messages_exception_handling(get_uid(token), channel_id, start)

    return get_messages(get_uid(token), channel_id, start)

def channel_leave(token, channel_id):
    '''Given a channel ID, the user removed as a member of this channel'''

    channel_id = int(channel_id)

    # Check exception errors
    leave_exception_handling(token, channel_id)

    # Allow user to leave
    leave(token, channel_id)

def channel_join(token, channel_id):
    '''Given a channel_id of a channel that the authorised user can join,
    adds them to that channel'''

    channel_id = int(channel_id)

    # Check exception errors
    join_exception_handling(token, channel_id)

    join(token, channel_id)

def channel_addowner(token, channel_id, u_id):
    '''Make user with user id u_id an owner of this channel'''

    u_id = int(u_id)
    channel_id = int(channel_id)

    # Check exception errors
    addowner_exception_handling(token, channel_id, u_id)

    # Add authorised user as an owner (and, if needed, as a member of the
    # channel)
    add_owner(channel_id, u_id)

def channel_removeowner(token, channel_id, u_id):
    '''Remove user with user id u_id an owner of this channel'''

    u_id = int(u_id)
    channel_id = int(channel_id)

    #  Check exception errors
    removeowner_exception_check(token, channel_id, u_id)

    remove_owner(channel_id, u_id)

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def invite_exception_handling(token, channel_id, u_id):
    '''channel_invite exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when channel_id does not refer to a valid channel.
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # InputError when u_id does not refer to a valid user
    if not check_valid_user_id(u_id):
        raise InputError(description='User Not a member of the Channel')

    # AccessError when the authorised user is not already a member of the
    # channel
    if not is_member(channel_id, get_uid(token)):
        raise AccessError(description='Authorised inviter not member of channel')

    # AccessError when user is already a member
    if is_member(channel_id, u_id):
        raise AccessError(description='User is already a member')

def details_exception_handling(authorized_user, channel_id):
    '''channel_details exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(get_token(authorized_user)):
        raise AccessError(description='Invalid token passed')

    # InputError when Channel ID is not a valid channel
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # AccessError when Authorised user is not a member of channel with
    # channel_id
    if not is_member(channel_id, authorized_user):
        raise AccessError(description='User Not a member of the Channel')

def messages_exception_handling(authorized_user, channel_id, start):
    '''channel_messages exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(get_token(authorized_user)):
        raise AccessError(description='Invalid token passed')
    
    # InputError when Channel ID is not a valid channel
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # InputError when start is greater than the total number of messages in
    # the channel
    if not is_member(channel_id, authorized_user):
        raise AccessError(description='User Not a member of the Channel')

    # AccessError whenAuthorised user is not a member of channel with
    # channel_id
    if check_start_greater(start, channel_id):
        raise InputError(description='No more messages to show')

def leave_exception_handling(token, channel_id):
    '''channel_leave exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when channel_id is not a valid channel.
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # AccessError when Authorised user is not a member of channel with
    # channel_id
    if not is_member(channel_id, get_uid(token)):
        raise AccessError(description='User Not a member of the Channel')

def join_exception_handling(token, channel_id):
    '''channel_join exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
    
    # InputError when channel_id is not a valid channel.
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # AccessError if channel is private, and token doesn't
    # refer to the owner of Flockr
    if not is_public(channel_id):
        if not is_flockr_owner(token):
            raise AccessError(description='Channel is private!')

def addowner_exception_handling(token, channel_id, u_id):
    '''channel_addowner exception error handling'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when channel_id is not a valid channel,
    # or user with u_id is already an owner of the channel
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # InputError when user with u_id is already an owner of the channel
    if is_owner(channel_id, get_token(u_id)):
        raise InputError(description='Already an owner!')

    # AccessError when the authorised user is not an owner of the flockr,
    # or an owner of this channel
    if not is_owner(channel_id, token):
        if not is_flockr_owner(token):
            raise AccessError(description='Not a global or channel owner!')

def removeowner_exception_check(token, channel_id, u_id):
    '''channel_removeowner exception error handling'''
    
    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
        
    # InputError when channel_id is not a valid channel,
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel does not exist')

    # InputError when user with u_id is already an owner of the channel
    if not is_owner(channel_id, get_token(u_id)):
        raise InputError(description='User is not an owner')

    # AccessError when the authorised user is not an owner of the flockr,
    # or an owner of this channel
    if not is_owner(channel_id, token) and not is_flockr_owner(token):
            raise AccessError(description='Removal requires authorisation by an owner!')

    
