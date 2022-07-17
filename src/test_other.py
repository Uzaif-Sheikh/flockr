'''
H15C, Group 3
Testing functions of other.py .
'''

import pytest
from auth import auth_register
from message import message_send
from other import clear, admin_userpermission_change, users_all, search
from channel import channel_addowner, channel_invite, channel_messages
from channels import channels_create
from error import InputError, AccessError

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

    return {'bob': [u_id_bob, token_bob], 'marley': [u_id_marley, token_marley],
            'shubham': [u_id_shubham, token_shubham], 'smith': [u_id_smith, token_smith]}

@pytest.fixture(name='channels')
def fixture_channels(users):
    '''This is a pytest fixture used to define some channel variables required for testing
    in all functions'''

    # Here, we assume that the channels_create function works perfectly

    # Create COMP1531 channel
    channel_comp1531_details = channels_create(users['bob'][1], 'COMP1531', True)
    channel_id_comp1531 = channel_comp1531_details['channel_id']

    # Create SENG1234 channel
    channel_seng1234_details = channels_create(users['marley'][1], 'SENG1234', True)
    channel_id_seng1234 = channel_seng1234_details['channel_id']

    # Create PHY5678 channel
    channel_phy5678_details = channels_create(users['shubham'][1], 'PHY5678', True)
    channel_id_phy5678 = channel_phy5678_details['channel_id']

    return {'COMP1531': channel_id_comp1531, 'SENG1234': channel_id_seng1234,
            'PHY5678': channel_id_phy5678}

def test_userpermission_change_inputerror(users):
    ''' Test all possible InputError cases for user permission changes'''

    # Generate invalid u_id by adding arbitrary numbers to the only valid u_id available
    invalid_u_id = users['shubham'][0] + 20

    # Checking for InputError with u_id that does not refer to a valid user
    with pytest.raises(InputError):
        admin_userpermission_change(users['bob'][1], invalid_u_id, 1)

    # Checking for InputError with non-value permission_id
    with pytest.raises(InputError):
        admin_userpermission_change(users['bob'][1], users['shubham'][0], 3)

    with pytest.raises(InputError):
        admin_userpermission_change(users['bob'][1], users['shubham'][0], 20.1)

def test_userpermission_change_accesserror(users):
    ''' Test all possible AccessError cases for user permission changes'''

    # Checking for InputError with u_id that does not refer to a valid user
    with pytest.raises(AccessError):
        admin_userpermission_change(users['marley'][1], users['shubham'][0], 1)

def test_userpermission_change_functionality(users, channels):
    '''
    Make sure the userpermission_change works correctly
    If we make Marley a Global owner, he should be able to add shubham
    to a group in which Marley is not a channel owner
    '''

    # Invite Shubham to COMP1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Initially Marley can NOT add Shubham to COMP1531
    with pytest.raises(AccessError):
        channel_addowner(users['marley'][1], channels['COMP1531'], users['shubham'][0])

    # Make Marley a Flockr Owner
    admin_userpermission_change(users['bob'][1], users['marley'][0], 1)

    # Now Marley CAN add Shubham to COMP1531
    channel_addowner(users['marley'][1], channels['COMP1531'], users['shubham'][0])

def test_search_functionality(users,channels):
    '''
    Checking if for the given token and query_str messages found it
    should return the list of messages in the channel the user is a
    member
    '''

    # inviting the user_shubham to the channel comp1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])


    # Sending a message in channel comp1531 by the user bob
    message_send(users['bob'][1], channels['COMP1531'], \
    'I LOVE COMP1531')

    # Searching for the sub-string "OVE" in the channel comp1531
    messages_01 = search(users['shubham'][1],'OVE')
    messages_check = channel_messages(users['shubham'][1], channels['COMP1531'], 0)

    assert messages_check['messages'] == messages_01['messages']

    # Searching for the sub-string in the channel comp1531 where
    # smith is not a member
    messages_02 = search(users['smith'][1], '1531')
    assert messages_02['messages'] == []

    # Searching for the sub-string "PMOC" which is not in the
    # channel comp 1531
    messages_03 = search(users['bob'][1], 'PMOC')
    assert messages_03['messages'] == []

    # Sending a message to the channel SENG1234 with user marley
    message_send(users['marley'][1],channels['SENG1234'], \
    'I LOVE SENG1234')

    # Searching for the sub-string "23" in the channel SENG1234
    messages_04 = search(users['marley'][1],'23')
    messages_check01 = channel_messages(users['marley'][1], channels['SENG1234'], 0)

    assert messages_check01['messages'] == messages_04['messages']

def test_users_all_functionality(users, channels):
    '''Test that the users_all function returns the right details'''

    assert users_all(users['marley'][1]) == {
        'users': [
            {
                'u_id': users['bob'][0],
                'email': 'bob@gmail.com',
                'name_first': 'bob',
                'name_last': 'lin',
                'handle_str': 'boblin',
                'profile_img_url': '',

            },
            {
                'u_id': users['marley'][0],
                'email': 'marley@gmail.com',
                'name_first': 'marley',
                'name_last': 'lin',
                'handle_str': 'marleylin',
                'profile_img_url': '',

            },
            {
                'u_id': users['shubham'][0],
                'email': 'shubham@gmail.com',
                'name_first': 'shubham',
                'name_last': 'johar',
                'handle_str': 'shubhamjohar',
                'profile_img_url': '',

            },
            {
                'u_id': users['smith'][0],
                'email': '123@gmail.com',
                'name_first': 'hayden',
                'name_last': 'smith',
                'handle_str': 'haydensmith',
                'profile_img_url': '',

            },
        ]
    }

def test_admin_userpermission_change_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        admin_userpermission_change(users['shubham'][1]+'heya', users['shubham'][0], 1)

def test_users_all_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        users_all(users['shubham'][1]+'boiss')

def test_search_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        search(users['shubham'][1]+'boss', 'hello')
