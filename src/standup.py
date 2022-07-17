'''
H15 Orange, Team 3

Implementation of standup.py functions for
assignment 1 spec. Iteration 3
'''

from error import InputError, AccessError
from data import check_valid_channel_id, is_member, get_uid, check_valid_token, \
                get_handle, start_standup, active_standup, send_standup

def standup_start(token, channel_id, length):
    '''Starts the standup period'''

    channel_id = int(channel_id)
    length = int(length)

    start_exception_handling(token, channel_id)

    return start_standup(token, channel_id, length)

def standup_active(token, channel_id):
    '''Checks and returns whether a standup is active or not'''

    #count_thread = active_count()

    channel_id = int(channel_id)

    active_exception_handling(token, channel_id)

    return active_standup(channel_id)

def standup_send(token, channel_id, message):
    """Sends a message to get buffered in the standup queue"""

    channel_id = int(channel_id)

    send_exception_handling(token, channel_id, message)

    return send_standup(token, channel_id, message)

# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def start_exception_handling(token, channel_id):
    '''Handles error exeptions for standup start function'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
   
    # InputError when channel_id doesn't refer to a valid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Invalid Channel ID')

    # InputError when an active standup is currently running in this channel
    if standup_active(token, channel_id)['is_active']:
        raise InputError(description='A standup is already running in this channel')

def active_exception_handling(token, channel_id):
    '''Handles error exeptions for standup active function'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when channel_id doesn't refer to a valid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Invalid Channel ID')

def send_exception_handling(token, channel_id, message):
    '''Handles error exeptions for standup send function'''

    # AccessError when token doesn't refer to a valid user
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
        
    # InputError when channel_id doesn't refer to a valid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description='Invalid Channel ID')

    # InputError when message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='Message too long.')

    # InputError if an active standup is still not running
    active_status = standup_active(token, channel_id)
    if active_status['is_active'] == False:
        raise InputError(description='No active standup running in this channel')

    # AccesError if authorised user is not part of the channel
    u_id = get_uid(token)
    if not is_member(channel_id, u_id):
        raise AccessError(description='User Not a member of the Channel')

    
