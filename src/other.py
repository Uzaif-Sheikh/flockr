'''
H15C, Group3
Implementation of functions which conform to individual
features of their own
'''
from error import InputError, AccessError
from data import get_uid, get_token, check_valid_user_id, is_flockr_owner, \
                is_member, validate_permission_id, change_permissions, data_reset, \
                get_all_users, get_related_messages, check_valid_token

def clear():
    '''Clear function used to the clear the entire data structure - the data dictionary
    and tokens to get to the initital state before testing for teh other features,
    very useful function for testing'''

    data_reset()

    return {}

def users_all(token):
    '''
    Returns a list of all users and their associated details
    '''

    users_all_exception(token)

    all_users = get_all_users(token)

    return all_users

def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to
    new permissions described by permission_id
    '''

    u_id = int(u_id)
    permission_id = int(permission_id)

    # Check for valid input parameters
    admin_exception(token, u_id, permission_id)

    # Set new permissions
    change_permissions(u_id, permission_id)

    return {}

def search(token, query_str):

    '''Given a query_str and token the function search for
       the message contained in the query_str'''

    search_exception(token)

    related_messages = get_related_messages(token, query_str)

    return {
        'messages': related_messages
    }


# ################################################################## #
#                         EXCEPTION HANDLING                         #
# ################################################################## #

def admin_exception(token, u_id, permission_id):
    '''Raise Errors when invalid parameters are passed in'''
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

    # InputError when u_id does not refer to a valid user
    if not check_valid_user_id(u_id):
        raise InputError(description="Invalid User ID")

    # InputError when permission_id does not refer to a value permission
    if not validate_permission_id(permission_id):
        raise InputError(description="Invalid Permission ID")

    # Raise InputError if authorised user is invalid
    if not is_flockr_owner(token):
        raise AccessError(description="Not an Authorised Owner of Flockr")

def search_exception(token):
    '''Search exceptions: invalid token'''

    # AccessError if invalid token is passed
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')

def users_all_exception(token):
    '''UsersAll exceptions: invalid token'''

    # AccessError if invalid token is passed
    if not check_valid_token(token):
        raise AccessError(description='Invalid token passed')
