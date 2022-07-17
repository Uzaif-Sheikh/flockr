'''
Defines a 'DATA' data structure which stores all information
to be stored throughout the use of the Flockr application
'''

import re
import os
import sys
import time
import random
import string
import pickle
import hashlib
import requests
from PIL import Image
import urllib.request
from flask import request, Flask
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from threading import Lock, Timer, active_count
from token_secret import token_generate, token_get_uid

REGEX = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'

DATA = {
    'users': [],
    'channels': [],
    'messages' : [],
    'tokens' : [],
    'authenticate_reset': [],
    'standups': [],
    'message_send_later_id': 0,
}

# #################################################################### #
#                KEY HELPER FUNCTIONS (USED IN ALL FILES)              #
# #################################################################### #

def get_handle(token):
    '''Given a token returns the handle of the user'''
    for user in DATA['users']:
        if user['id'] == get_uid(token):
            return user['handle']

    return -1

def check_valid_channel_id(channel_id):
    '''Check if channel_id refers to a valid channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            return True

    return False

def check_valid_user_id(u_id):
    '''Check if user_id refers to a valid user'''

    for registered_user in DATA['users']:
        if registered_user['id'] == u_id:
            return True

    return False

def check_valid_token(token):
    '''Check if token refers to a valid user'''

    for registered_user in DATA['tokens']:
        if registered_user['token'] == token:
            return True

    return False

def is_member(channel_id, u_id):
    '''Check if authorised user is a member of the channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            for members in channels['members']:
                if members == u_id:
                    return True
    return False

def is_owner(channel_id, token):
    '''Check if authorised user is an Owner of the channel'''

    u_id = get_uid(token)
    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            for owner in channels['owner_members']:
                if owner == u_id:
                    return True

    return False

def get_uid(token):
    '''Given a token, get the u_id'''

    try:
        return token_get_uid(token)
    except:
        return -1

def get_token(u_id):
    '''Given a u_id, get the token'''

    try:
        return token_generate(u_id)
    except:
        return -1

def is_public(channel_id):
    '''Checks if channel is private or public
    Must always be called AFTER check_valid_channel_id function
    to make sure channel refers to valid channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            return channels['is_public']
    return False

def is_flockr_owner(token):
    '''Checks if token refers to the owner of Flockr'''

    # Owner of Flockr will be indexed at 1 in our dictionary
    for registered_user in DATA['users']:
        if registered_user['id'] == get_uid(token):
            if registered_user['global_permissions'] == 1:
                return True

    return False

def hash_password(password):
    '''Hash provided password'''
    return hashlib.sha256(password.encode()).hexdigest()

def check_time_sent(time_sent):
    '''Check if the time_sent is from the past
        or the future'''

    now_date = datetime.now()
    date = datetime.fromtimestamp(time_sent)

    if(date > now_date):
        return True

    return False

def already_pinned(message_id):
    '''Check if the given message is already pinned or not'''

    for message in DATA['messages']:
        if message['message_id'] == message_id and message['is_pinned'] == True:
            return True

    return False

# #################################################################### #
#                   CHANNEL-SPECIFIC HELPER FUNCTIONS                  #
# #################################################################### #

def add_member(channel_id, u_id):
    '''Add member to channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            channels['members'].append(u_id)

def get_channel_details(channel_id):
    '''Get details of a channel'''

    owner_members = []
    members = []

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            needed_channel = channels

    for member in needed_channel['members']:
        for user in DATA['users']:
            if user['id'] == member:
                member_info = {
                    'u_id' : member,
                    'name_first' : user['first_name'],
                    'name_last' : user['last_name'],
                    'profile_img_url' : user['profile_photo']
                }

                members.append(member_info)

    for owner_member in needed_channel['owner_members']:
        for user in DATA['users']:
            if user['id'] == owner_member:
                owner_member_info = {
                    'u_id' : owner_member,
                    'name_first' : user['first_name'],
                    'name_last' : user['last_name'],
                    'profile_img_url' : user['profile_photo']
                }

                owner_members.append(owner_member_info)


    return {
        'name': needed_channel['name'],
        'owner_members': owner_members,
        'all_members': members
    }


def get_messages(u_id, channel_id, start):
    '''Get a certain number of messages, return
    index of first and last message'''

    messages_channel = []
    for messages in DATA['messages']:
        if messages['channel_id'] == channel_id:
            messages_channel.insert(0, messages)

    messages_needed = [messages for index_message,
                    messages in enumerate(messages_channel)
                    if (index_message >= start and index_message < start + 50)]

    final_messages = [{k: v for k, v in d.items() if k != 'channel_id'} for d in messages_needed]

    for message in final_messages:
        if u_id not in message['reacts'][0]['u_ids']:
            message['reacts'][0]['is_this_user_reacted'] = False

    if len(final_messages) < 50:
        end = -1
    else:
        end = start + 50

    return {'messages': final_messages, 'start': start, 'end': end}

def leave(token, channel_id):
    '''Allow authorised user to leave'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            channels['members'].remove(get_uid(token))
            if is_owner(channel_id, token):
                channels['owner_members'].remove(get_uid(token))
                break

def join(token, channel_id):
    '''Allow authorised user to join'''

    # Allow authorised user to join the channel
    add_member(channel_id, get_uid(token))

def remove_owner(channel_id, u_id):
    '''Remove authorised user as an owner of a channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            channels['owner_members'].remove(u_id)
            break

def add_owner(channel_id, u_id):
    '''Add authorised user as an owner of a channel'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            channels['owner_members'].append(u_id)

def add_flockr_owner(channel_id, u_id):
    '''Add Flockr Owner to channel
    Adds both as owner and as member'''

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            channels['members'].append(u_id)
            channels['owner_members'].append(u_id)

# Check if start is greater than the total length
# of messages in a channel
def check_start_greater(start, channel_id):
    '''Check if number of messages are less than start'''
    channel_messages = []
    for message in DATA['messages']:
        if message['channel_id'] == channel_id:
            channel_messages.append(message)

    if start > len(channel_messages):
        return True

    return False

# #################################################################### #
#                     AUTH-SPECIFIC HELPER FUNCTIONS                   #
# #################################################################### #

def login(email, password):
    ''' Log the user in'''
    user_uid = find_user_id(email)
    user_token = get_token(user_uid)

    update_token_user(user_uid, user_token)

    return {
        'u_id' : user_uid,
        'token' : user_token,
    }

def logout(token):
    ''' Log the user out '''

    for valid_uid_tokens in DATA['tokens']:
        if valid_uid_tokens['token'] == token:
            valid_uid_tokens['token'] = None
            return True

    return False

def register(email, password, name_first, name_last):
    ''' Register a user '''

    # Set global permissions to MEMBER
    global_permissions = 2

    # Assess whether or not this is the first user (flockr owner)
    # If they are the first user, global permissions must be changed to
    # OWNER
    if len(DATA['tokens']) == 0:
        global_permissions = 1

    # Initialise user ID
    user_id = len(DATA['tokens'])

    # Create handle string
    handle = name_first.lower() + name_last.lower()
    handle = handle.replace(' ', '')

    # Handle must be at most 20 characters
    if len(handle) > 20:
        handle = handle[:19]

    # If handle string is already token, generate a unique handle
    if handle_search(handle) == True:
        changed_mail = email.split('@')[0]
        handle = changed_mail + name_last

    # Account details
    account = {
        'id' : user_id,
        'first_name' : name_first,
        'last_name': name_last,
        'email' : email,
        'password' : hash_password(password),
        'handle' : handle,
        'global_permissions' : global_permissions,
        'profile_photo': '',
    }

    DATA['users'].append(account)

    unique_token = token_generate(user_id)

    registered_details = {
        'u_id': user_id,
        'token': unique_token,
    }

    DATA['tokens'].append(registered_details)

    return registered_details

def handle_search(handle):

    '''
    This functions takes a handle of a user and sereach in the DATA //
    and return True if found or else False.
    '''

    for registered_user in DATA['users']:
        if registered_user['handle'] == handle:
            return True

    return False

def check_email(email):

    '''
    This function takes an email and check //
    if the email is a vail email or not.
    '''

    if re.search(REGEX, email):
        return True

    return False

def used_email(email):

    '''
    This function checks from the DATA that //
    the email is not already in use.
    '''

    for registered_user in DATA['users']:
        if registered_user['email'] == email:
            return True

    return False

def find_user_id(email):

    '''
    This function finds the user_id for the given //
    email for the user.
    '''

    for registered_user in DATA['users']:
        if registered_user['email'] == email:
            return registered_user['id']

    return None

def find_password_registered(email, password):

    '''
    This function checks for the password stored in the DATA //
    is same as the given password.
    '''

    for registered_user in DATA['users']:
        if registered_user['email'] == email and registered_user['password'] == hash_password(password):
            return True

    return False

def update_token_user(user_uid, user_token):
    '''
    This function take user_id and token and //
    updates the user token.
    '''

    for registered_user in DATA['tokens']:
        if registered_user['u_id'] == user_uid:
            registered_user['token'] = user_token

def passwordreset_request(email):
    '''
    Request reset of password

    Reference: https://pythonbasics.org/flask-mail/
    '''
    # set up email settings
    app = Flask(__name__)

    mail_settings = {
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 465,
        'MAIL_USE_TLS': False,
        'MAIL_USE_SSL': True,
        'MAIL_USERNAME': 'group3h15c@gmail.com',
        'MAIL_PASSWORD': 'hakunamatata123!',
    }

    app.config.update(mail_settings)
    mail = Mail(app)

    # Given that the email exists in user_emails, generate key code
    letters_and_digits = string.ascii_letters + string.digits
    reset_length = 6	# Length of the reset code
    reset_code = ''.join(random.choice(letters_and_digits) for i in range(reset_length))

    # send email
    with app.app_context():
        msg = Message(subject='FLOCKR RESET CODE',
                      sender=app.config.get('MAIL_USERNAME'),
                      recipients=[email], # replace with your email for testing
                      body='Hello '+ str(data_get_user_name(email)) +',\n\nYour reset token is: '
                      + str(reset_code)+
                      '\n\nPlease note this link will only be available for 24 hours.')
        mail.send(msg)

    # add to reset list
    data_add_reset_pair(email, str(reset_code))
    return {}

def passwordreset_reset(reset_code, new_password):
    '''Auth password reset, validates reset code and reset password'''

    email = data_get_reset_email(reset_code)

    # get user id
    u_id = find_user_id(email)

    # remove reset request for email from list
    data_remove_reset_request(email)

    # set new password
    data_set_password(u_id, new_password)

    return {}

def data_get_user_name(email):
    '''Get user name from email'''

    for user in DATA['users']:
        if user['email'] == email:
            return user['first_name']

    return ''

def data_add_reset_pair(email, reset_code):
    '''Add a reset code email pair'''

    for entry in DATA['authenticate_reset']:
        if entry['email'] == email:
            entry['reset_code'] = reset_code
            entry['time_created'] = datetime.now()
            return

    DATA['authenticate_reset'].append({
        'email': email,
        'reset_code': reset_code,
        'time_created': datetime.now()
    })

def data_get_reset_email(reset_code):
    '''Check if reset code is valid'''
    for entry in DATA['authenticate_reset']:
        if reset_code == entry['reset_code']:
            return entry['email']

    return None

def data_remove_reset_request(email):
    '''Remove reset request'''
    index = 0
    counter = 0

    for entry in DATA['authenticate_reset']:
        if entry['email'] == email:
            index = counter
        else:
            counter += 1

    del DATA['authenticate_reset'][index]

def data_set_password(u_id, new_password):
    '''Change password'''
    for user in DATA['users']:
        if user['id'] == u_id:
            user['password'] = hash_password(new_password)

    return -1

# #################################################################### #
#                    OTHER-SPECIFIC HELPER FUNCTIONS                   #
# #################################################################### #

def data_reset():
    '''Reset data'''

    global DATA
    DATA = {
        'users': [],
        'channels': [],
        'messages' : [],
        'tokens' : [],
        'authenticate_reset': [],
        'standups': [],
        'message_send_later_id': '',
    }

def get_all_users(token):
    '''Get information about all the users on the app'''

    all_users = {'users': []}
    for user in DATA['users']:
        details = {
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first_name'],
            'name_last': user['last_name'],
            'handle_str': user['handle'],
            'profile_img_url': user['profile_photo'],
        }

        all_users['users'].append(details)

    return all_users

def get_related_messages(token, query_str):
    '''Get the messages which relate to the query_str'''

    list_messages = []
    for message in DATA['messages']:
        channel_id = message['channel_id']
        if message['message'].find(query_str) != -1:
            if is_member(channel_id, get_uid(token)):
                new_messages = {
                    'message_id': message['message_id'],
                    'u_id' : message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created'],
                    'reacts': message['reacts'],
                    'is_pinned': message['is_pinned'],
                }

                list_messages.append(new_messages)

    return list_messages

def validate_permission_id(permission_id):
    '''Validate that the permission_id is either 1 or 2'''

    if permission_id in (1, 2):
        return True

    return False

def change_permissions(u_id, permission_id):
    '''Alter the permissions of a user'''

    for registered_user in DATA['users']:
        if registered_user['id'] == u_id:
            registered_user['global_permissions'] = permission_id

# #################################################################### #
#                  MESSAGE-SPECIFIC HELPER FUNCTIONS                   #
# #################################################################### #

def send_message(token, channel_id, message, user_uid):
    '''Send a message and assess associated details'''

    message_id = len(DATA['messages'])

    timestamp = datetime.now().timestamp()
    new_message = {
        'message_id' : message_id,
        'u_id' : user_uid,
        'message' : message,
        'time_created' : timestamp,
        'channel_id' : channel_id,
        'reacts' : [{'react_id' : 1, 'u_ids' : [], 'is_this_user_reacted' : False}],
        'is_pinned' : False,
    }

    DATA['messages'].append(new_message)

    return message_id

def remove_message(token, message_id):
    '''Delete a message'''

    for message in DATA['messages']:
        if message['message_id'] == message_id:
            DATA['messages'].remove(message)

def edit_message(token, message_id, message):
    '''Edit a message'''

    if len(message) == 0:
        remove_message(token, message_id)
    else:
        for messages in DATA['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message

def send_message_thread(token, channel_id, message, user_uid, lock):
    '''
    Use threading to send a message using a timer
    '''
    message_id = len(DATA['messages'])

    with lock:
        DATA['message_send_later_id'] = message_id

        timestamp = datetime.now().timestamp()
        new_message = {
            'message_id' : message_id,
            'u_id' : user_uid,
            'message' : message,
            'time_created' : timestamp,
            'channel_id' : channel_id,
            'reacts' : [{'react_id' : 1, 'u_ids' : [], 'is_this_user_reacted' : False}],
            'is_pinned' : False,
        }

        DATA['messages'].append(new_message)
        time.sleep(1)

def send_later(token, channel_id, message, time_sent):
    '''Send a message on the given time'''

    timestamp_now = datetime.now().timestamp()
    send_time = time_sent - timestamp_now

    lock = Lock()

    t = Timer(send_time, send_message_thread, [token, channel_id, message, get_uid(token),lock])

    t.start()

    t.join()

    return DATA['message_send_later_id']

def add_react_message(token, message_id, react_id):
    ''' Adds the user in the reacted members list of the message and then,
    sets the is_this_user_reacted field to true'''

    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            u_id = get_uid(token)
            if u_id not in messages['reacts'][0]['u_ids']:
                messages['reacts'][0]['is_this_user_reacted'] = True
            messages['reacts'][0]['u_ids'].append(u_id)


def add_unreact_message(token, message_id, react_id):
    ''' Adds the user in the reacted members list of the message and then,
    sets the is_this_user_reacted field to true'''

    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            messages['reacts'][0]['u_ids'].remove(get_uid(token))
            messages['reacts'][0]['is_this_user_reacted'] = False


def check_message_exsits(message_id):
    '''Finds the associated message id with the message if the message exsits in the DATA structure
    otherwise retuns -1, showing that the message does't exists'''

    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            return True

    return False

def check_react_exists(u_id, message_id):
    '''
    Returns true if react already exists
    and false otherwise
    '''
    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            for users in messages['reacts'][0]['u_ids']:
                if users == u_id:
                    return True

    messages['reacts'][0]['is_this_user_reacted'] = True
    return False

def get_channel_id(message_id):
    '''From the given message, it finds out the channel it is associated with,
        otherwise return -1'''

    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            return messages['channel_id']

    return -1

def sent_message_user(user_uid, message_id):
    '''Finds the assocaited user_id for the given message_id and if the user who created the message
    is the same as authorised user then return true else False'''

    for messages in DATA['messages']:
        if messages['message_id'] == message_id:
            if messages['u_id'] == user_uid:
                return True

    return False

def pin_message(message_id):
    '''Pin the given message by the user'''

    for message in DATA['messages']:
        if message['message_id'] == message_id:
            message['is_pinned'] = True

def unpin_message(message_id):
    '''Unpin the given message by the user'''

    for message in DATA['messages']:
        if message['message_id'] == message_id:
            message['is_pinned'] = False

# #################################################################### #
#                     USER-SPECIFIC HELPER FUNCTIONS                   #
# #################################################################### #

def setname(token, name_first, name_last):
    '''Change the name of a user'''

    u_id = get_uid(token)
    for user in DATA['users']:
        if user['id'] == u_id:
            user['first_name'] = name_first
            user['last_name'] = name_last

def setemail(token, email):
    '''Change the email of a user'''

    u_id = get_uid(token)
    for user in DATA['users']:
        if u_id == user['id']:
            user['email'] = email

def sethandle(token, handle_str):
    '''Change the nickname of a user'''

    u_id = get_uid(token)
    for user in DATA['users']:
        if user['id'] == u_id:
            user['handle'] = handle_str

def check_email_in_use(email):
    '''Returns True if the email is already in use'''

    for user in DATA['users']:
        if email == user['email']:
            return True
    return False

def check_valid_email(email):
    '''Check whether the email is valid using regex'''

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True
    return False

def check_valid_first_last_name(name):
    '''Checking the validity of the passed name (first / last)'''

    if len(name) >= 50 or len(name) <= 1:
        return False
    return True

def get_profile(u_id):
    '''Get the profile information for user with u_id'''

    user = {}
    user_info = {}
    for registered_user in DATA['users']:
        if registered_user['id'] == u_id:
            user['u_id'] = registered_user['id']
            user['email'] = registered_user['email']
            user['name_first'] = registered_user['first_name']
            user['name_last'] = registered_user['last_name']
            user['handle_str'] = registered_user['handle']
            user['profile_img_url'] = registered_user['profile_photo']

    user_info['user'] = user

    return user_info

def generate_url(string_length):
    '''Generate a random string of letters and digits '''
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))

def set_profile_url(token, image_name):
    '''Set profile url'''
    u_id = get_uid(token)
    filename = image_name + '.jpg'
    new_img_url = request.url_root + 'static/' + filename

    for user in DATA['users']:
        if user['id'] == u_id:
            user['profile_photo'] = new_img_url

def crop_image(img_url, x_start, y_start, x_end, y_end):
    '''
    Set profile photo size
    '''

    # Create Random URL
    image_name = generate_url(20)
    # Get image
    filepath = './src/static/' + image_name + '.jpg'
    urllib.request.urlretrieve(img_url, filepath)

    # crop this image
    uncropped_profile_photo = Image.open(filepath)
    cropped_profile_photo = uncropped_profile_photo.crop((x_start, y_start, x_end, y_end))
    # save this cropped image back into your image file
    cropped_profile_photo.save(filepath)

    return image_name


# #################################################################### #
#                  CHANNELS-SPECIFIC HELPER FUNCTIONS                  #
# #################################################################### #

def get_list(token):
    '''Get the list of channels specific to the user
    with token value'''

    channels = []
    for channel in DATA['channels']:
        for members in channel['members']:
            if members == get_uid(token):
                channels.append({
                    'channel_id':channel['channel_id'],
                    'name':channel['name'],
                })

    return channels

def get_listall(token):
    '''Get list of all channels'''

    list_all_channels = []
    for channel in DATA['channels']:
        list_all_channels.append({
            'channel_id': channel['channel_id'],
            'name':channel['name'],
        })

    return list_all_channels

def create_channel(token, name, is_public):
    '''Create a channel'''

    channel_id = len(DATA['channels'])

    DATA['channels'].append({
        'channel_id':channel_id,
        'name':name, 'is_public':is_public,
        'owner_members':[get_uid(token)],
        'members':[get_uid(token)],
    })

    return channel_id

# #################################################################### #
#                              STANDUPS                                #
# #################################################################### #

def start_standup(token, channel_id, length):
    '''
    Creates a standup and returns the finish
    time of the standup
    '''
    start = datetime.now()

    finish = start + timedelta(seconds=length)
    finish_time = finish.timestamp()

    DATA['standups'].append({
        'messages' : [],
        'channel_id' : channel_id,
        'time_finish' : finish_time,
        'is_active': False
    })

    Timer(length, standup_end, (token, channel_id)).start()

    for standup in DATA['standups']:
        if standup['channel_id'] == channel_id:
            standup['is_active'] = True

    pickle_data()

    return {'time_finish' : finish_time}

def active_standup(channel_id):
    '''
    Check whether a standup is active
    Return the finish time if one does exist
    '''
    for standup in DATA['standups']:
        if standup['channel_id'] == channel_id:
            if standup['is_active'] == True:
                return {
                    'is_active' : True,
                    'time_finish' : standup['time_finish']
                }

    return {
        'is_active' : False,
        'time_finish' : None
    }

def send_standup(token, channel_id, message):
    '''
    Add message to a standup list
    '''
    for standup in DATA['standups']:
        if standup['channel_id'] == channel_id:
            standup_message = {
                'message' : message,
                'handle' : get_handle(token)
            }

            standup['messages'].append(standup_message)

    pickle_data()

    return {}

def standup_end (token, channel_id):
    '''Returns the final message and removes the standup from the list'''
    full_message = ''
    for standup in DATA['standups']:
        if standup['channel_id'] == channel_id:
            standup['is_active'] = False
            for messages in standup['messages']:
                full_message += messages['handle'] + ' : ' + messages['message'] + '\n'
        send_message(token, channel_id, full_message, get_uid(token))
        DATA['standups'].remove(standup)

    pickle_data()

# #################################################################### #
#                                PICKLE                                #
# #################################################################### #

def pickle_data():
    '''Pickle data'''
    global DATA
    with open('database.p', 'wb') as FILE:
        pickle.dump(DATA, FILE)

def unpickle_data():
    '''Unpickle data'''
    global DATA
    if os.path.exists('database.p'):
        DATA = pickle.load(open('database.p', 'rb'))