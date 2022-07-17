'''
H15 Orange, Group 3

Implementation of test_channel.py functions as specified on the
assignment 1 spec.

Iteration 1
'''

import pytest
from other import clear
from message import message_send
from auth import auth_register
from channels import channels_create
from error import InputError, AccessError
from channel import channel_invite, channel_details, channel_messages, channel_leave, \
                    channel_join, channel_addowner, channel_removeowner

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
    channel_comp1531_details = channels_create(users['bob'][1], 'COMP1531', False)
    channel_id_comp1531 = channel_comp1531_details['channel_id']

    # Create SENG1234 channel
    channel_seng1234_details = channels_create(users['marley'][1], 'SENG1234', True)
    channel_id_seng1234 = channel_seng1234_details['channel_id']

    # Create PHY5678 channel
    channel_phy5678_details = channels_create(users['shubham'][1], 'PHY5678', False)
    channel_id_phy5678 = channel_phy5678_details['channel_id']

    return {'COMP1531': channel_id_comp1531, 'SENG1234': channel_id_seng1234,
            'PHY5678': channel_id_phy5678}

@pytest.fixture(name='messages')
def fixture_messages(users, channels):
    '''This creates a pytest fixture used to create some messages in the channels'''
    # Here, we assume that the messages_send function works perfectly
    sent_messages = 0
    while sent_messages <= 50:
        message_send(users['bob'][1], \
                        channels['COMP1531'], 'I am finally doing 1531')
        message_send(users['marley'][1], \
                        channels['SENG1234'], 'I am finally doing SENG1234')
        message_send(users['shubham'][1], \
                        channels['PHY5678'], 'I am finally doing PHY5678')
        sent_messages = sent_messages + 1

    message_comp1531 = message_send(users['bob'][1], \
                        channels['COMP1531'], 'I have done 1531 50 times, when will  \
                        get rid of it')
    message_seng1234 = message_send(users['marley'][1], \
                        channels['SENG1234'], 'I have done seng1234 50 times, when will i \
                        get rid of it')
    message_phy5678 = message_send(users['shubham'][1], \
                        channels['PHY5678'], 'I have done seng1234 50 times, when will i \
                        get rid of it')

    return {'MESSAGE_COMP1531' : message_comp1531, 'MESSAGE_SENG1234' : \
            message_seng1234, 'MESSAGE_PHY5678' : message_phy5678}

def test_channel_invite_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_invite'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['COMP1531'] + 30
    invalid_channel_id_c = channels['COMP1531'] + 40

    # Generate invalid u_id by adding arbitrary numbers to the only valid u_id available
    invalid_u_id_a = users['shubham'][0] + 20
    invalid_u_id_b = users['shubham'][0] + 30
    invalid_u_id_c = users['shubham'][0] + 40

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_invite(users['bob'][1], invalid_channel_id_a, users['shubham'][0])

    with pytest.raises(InputError):

        channel_invite(users['bob'][1], invalid_channel_id_b, users['shubham'][0])

    with pytest.raises(InputError):

        channel_invite(users['bob'][1], invalid_channel_id_c, users['shubham'][0])

    # checking for InputError with u_id that does not refer to a valid user
    with pytest.raises(InputError):

        channel_invite(users['bob'][1], channels['COMP1531'], invalid_u_id_a)

    with pytest.raises(InputError):

        channel_invite(users['bob'][1], channels['COMP1531'], invalid_u_id_b)

    with pytest.raises(InputError):

        channel_invite(users['bob'][1], channels['COMP1531'], invalid_u_id_c)

def test_channel_invite_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_invite'''

    # Check AccessError when the authorised user is not already a member of the channel
    with pytest.raises(AccessError):

        channel_invite(users['bob'][1], channels['SENG1234'], users['shubham'][0])

    with pytest.raises(AccessError):

        channel_invite(users['marley'][1], channels['COMP1531'], users['shubham'][0])

    with pytest.raises(AccessError):

        channel_invite(users['shubham'][1], channels['SENG1234'], users['bob'][0])

    with pytest.raises(AccessError):

        channel_invite(users['shubham'][1], channels['COMP1531'], users['marley'][0])

def test_channel_invite_functionality(users, channels):
    ''' Test that channel_invite is working perfectly'''

    # Invites Marley to channel COMP1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['marley'][0])

    # If marley has been correctly added as a member, he should be able to invite
    # another user to the channel
    channel_invite(users['marley'][1], channels['COMP1531'], users['shubham'][0])

    # If marley has been correctly added as a member, he should be able to leave the channel, with
    # no AccessError raised.
    channel_leave(users['marley'][1], channels['COMP1531'])

def test_channel_details_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_details'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['COMP1531'] + 30
    invalid_channel_id_c = channels['COMP1531'] + 40

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_details(users['bob'][1], invalid_channel_id_a)

    with pytest.raises(InputError):

        channel_details(users['bob'][1], invalid_channel_id_b)

    with pytest.raises(InputError):

        channel_details(users['bob'][1], invalid_channel_id_c)

def test_channel_details_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_details'''

    # Check AccessError when the authorised user is not already a member of the channel
    with pytest.raises(AccessError):

        channel_details(users['marley'][1], channels['COMP1531'])

    with pytest.raises(AccessError):

        channel_details(users['shubham'][1], channels['SENG1234'])

    with pytest.raises(AccessError):

        channel_details(users['shubham'][1], channels['COMP1531'])

def test_channel_details_functionality(users, channels):
    '''Test that channel_details works as it is supposed to'''

    #Creates a list of all existing members
    member_check = []
    member_check.append(users['bob'][0])
    member_check.append(users['shubham'][0])
    member_check.append(users['marley'][0])
    member_check.append(users['smith'][0])

    #Bob invites all other users to Channel COMP1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])
    channel_invite(users['bob'][1], channels['COMP1531'], users['marley'][0])
    channel_invite(users['bob'][1], channels['COMP1531'], users['smith'][0])

    #Using Channel details to check that the list of
    details_1531 = channel_details(users['bob'][1], channels['COMP1531'])
    assert len(details_1531['all_members']) == len(member_check)

    channel_leave(users['bob'][1], channels['COMP1531'])
    details_1531_after_removal = channel_details(users['shubham'][1], channels['COMP1531'])

    assert len(details_1531_after_removal['all_members']) == len(member_check) - 1
    assert details_1531_after_removal['owner_members'] == []

def test_channel_messages_inputerror(users, channels, messages):
    ''' Test all possible InputError cases for channel_messages'''
    channel_invite(users['bob'][1], channels['COMP1531'], users['marley'][0])
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 10
    invalid_channel_id_b = channels['COMP1531'] + 20
    invalid_channel_id_c = channels['COMP1531'] + 30

    start = 0

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_messages(users['bob'][1], invalid_channel_id_a, start)

    with pytest.raises(InputError):

        channel_messages(users['marley'][1], invalid_channel_id_b, start)

    with pytest.raises(InputError):

        channel_messages(users['shubham'][1], invalid_channel_id_c, start)

    # checking for start value greater than the number of messages already in the structure.
    with pytest.raises(InputError):

        invalid_start_a = start + 1000
        channel_messages(users['bob'][1], channels['COMP1531'], invalid_start_a)

    with pytest.raises(InputError):

        invalid_start_b = start + 2000
        channel_messages(users['bob'][1], channels['COMP1531'], invalid_start_b)

    with pytest.raises(InputError):

        invalid_start_c = start + 3000
        channel_messages(users['bob'][1], channels['COMP1531'], invalid_start_c)

def test_channel_messages_functionality(users, channels, messages):
    '''Tests to check whetehr channel_messages behaves as supposed'''

    start = 0
    #Get the first fifty messages from channel_messages and check they are returned properly an check
    #end is returned as supposed.
    message_1531 = channel_messages(users['bob'][1], channels['COMP1531'], start)
    assert message_1531['end'] == 50
    assert len(message_1531['messages']) == 50

    #testing the last message sent appears as the first message in the list of channel_messages.
    assert message_1531['messages'][0]['message_id'] == \
            messages['MESSAGE_COMP1531']['message_id']

    #Start from the end of already read messages and read more messages and check end becomes -1.
    new_start = message_1531['end']
    next_messages_1531 = channel_messages(users['bob'][1], channels['COMP1531'], new_start)

    assert len(next_messages_1531['messages']) == 2
    assert next_messages_1531['end'] == -1

    message_1234 = channel_messages(users['marley'][1], channels['SENG1234'], start)
    assert message_1234['end'] == 50
    assert len(message_1234['messages']) == 50

    #testing the last message sent appears as the first message in the list of channel_messages.
    assert message_1234['messages'][0]['message_id'] == \
            messages['MESSAGE_SENG1234']['message_id']

    new_start = message_1234['end']

    next_messages_1234 = channel_messages(users['marley'][1], \
                            channels['SENG1234'], new_start)

    assert len(next_messages_1234['messages']) == 2
    assert next_messages_1234['end'] == -1

    message_5678 = channel_messages(users['shubham'][1], channels['PHY5678'], start)

    assert message_5678['end'] == 50
    assert len(message_5678['messages']) == 50

    #testing the last message sent appears as the first message in the list of channel_messages.
    assert message_5678['messages'][0]['message_id'] == \
            messages['MESSAGE_PHY5678']['message_id']

    new_start = message_5678['end']
    next_messages_5678 = channel_messages(users['shubham'][1], \
                            channels['PHY5678'], new_start)
    assert len(next_messages_5678['messages']) == 2
    assert next_messages_5678['end'] == -1


def test_channel_messages_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_messages'''

    start = 0

    # Check AccessError when the authorised user is not already a member of the channel
    with pytest.raises(AccessError):

        channel_messages(users['bob'][1], channels['SENG1234'], start)

    with pytest.raises(AccessError):

        channel_messages(users['marley'][1], channels['COMP1531'], start)

    with pytest.raises(AccessError):

        channel_messages(users['shubham'][1], channels['SENG1234'], start)

    with pytest.raises(AccessError):

        channel_messages(users['shubham'][1], channels['COMP1531'], start)

def test_channel_leave_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_leave'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 10
    invalid_channel_id_b = channels['COMP1531'] + 20
    invalid_channel_id_c = channels['COMP1531'] + 30

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_leave(users['bob'][1], invalid_channel_id_a)

    with pytest.raises(InputError):

        channel_leave(users['shubham'][1], invalid_channel_id_b)

    with pytest.raises(InputError):

        channel_leave(users['marley'][1], invalid_channel_id_c)

def test_channel_leave_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_leave'''

    # Check AccessError when the authorised user is not already a member of the channel
    with pytest.raises(AccessError):

        channel_leave(users['bob'][1], channels['SENG1234'])

    with pytest.raises(AccessError):

        channel_leave(users['marley'][1], channels['COMP1531'])

    with pytest.raises(AccessError):

        channel_leave(users['shubham'][1], channels['SENG1234'])

    with pytest.raises(AccessError):

        channel_leave(users['shubham'][1], channels['COMP1531'])

def test_channel_leave_functionality(users, channels):
    '''Test to make sure channel_leave works as it is supposed to'''

    # Remove Bob from COMP1531
    channel_leave(users['bob'][1], channels['COMP1531'])
    # Remove Marley from SENG1234
    channel_leave(users['marley'][1], channels['SENG1234'])

    # Only a member of a channel (or an owner) may invite someone to the channel.
    # Hence an AccessError should be raised when Bob and Marley attempt to issue invites
    with pytest.raises(AccessError):

        channel_invite(users['marley'][1], channels['SENG1234'], users['bob'][0])

    with pytest.raises(AccessError):

        channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])

def test_owner_leave(users, channels):
    '''If an owner leaves a channel, they must also
    be removed as an owner, not just as a member'''

    # Add Marley to PHY5678
    channel_invite(users['shubham'][1], channels['PHY5678'], users['marley'][0])

    # Let Shubham leave the channel he is a part of
    channel_leave(users['shubham'][1], channels['PHY5678'])

    # If an owner is not a member of a channel they can't add another owner
    with pytest.raises(AccessError):

        channel_addowner(users['shubham'][1], channels['PHY5678'], users['marley'][0])

def test_channel_join_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_join'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['COMP1531'] + 30
    invalid_channel_id_c = channels['COMP1531'] + 40

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_join(users['bob'][1], invalid_channel_id_a)

    with pytest.raises(InputError):

        channel_join(users['bob'][1], invalid_channel_id_b)

    with pytest.raises(InputError):

        channel_join(users['bob'][1], invalid_channel_id_c)

def test_channel_join_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_join'''

    # Check AccessError when the authorised user is not an owner, and channel is private
    with pytest.raises(AccessError):

        channel_join(users['shubham'][1], channels['COMP1531'])

    with pytest.raises(AccessError):

        channel_join(users['marley'][1], channels['COMP1531'])

def test_channel_join_functionality(users, channels):
    '''If a user is NOT correctly added to a channel then the leave function
    would raise an AccessError if it was called upon this user.
    Hence, a key error must not be raised if we call channel_leave()
    on a user who is already added.'''

    # Let Bob join two channels
    channel_join(users['bob'][1], channels['PHY5678'])
    channel_join(users['bob'][1], channels['SENG1234'])

    # Let Bob leave two channels, if he is correctly added
    channel_leave(users['bob'][1], channels['PHY5678'])
    channel_leave(users['bob'][1], channels['SENG1234'])

def test_channel_addowner_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_addowner'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['SENG1234'] + 30
    invalid_channel_id_c = channels['PHY5678'] + 40

    # Add Shubham to COMP1531 channel
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])
    # Add Shubham to SENG1234 channel
    channel_join(users['shubham'][1], channels['SENG1234'])
    # Add Bob to SENG1234 channel
    channel_join(users['bob'][1], channels['SENG1234'])
    # Add BOB to PHY5678 channel
    channel_join(users['bob'][1], channels['PHY5678'])

    # Make Shubham an owner of channel COMP1531
    channel_addowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_addowner(users['bob'][1], invalid_channel_id_a, users['marley'][0])

    with pytest.raises(InputError):

        channel_addowner(users['marley'][1], invalid_channel_id_b, users['shubham'][0])

    with pytest.raises(InputError):

        channel_addowner(users['shubham'][1], invalid_channel_id_c, users['bob'][0])

        # Check whether user is already an owner of the channel
        # or an Owner of flockr who has joined the channel and is therefore automatically
        # an owner of the channel

    with pytest.raises(InputError):

        channel_addowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    with pytest.raises(InputError):

        channel_addowner(users['shubham'][1], channels['PHY5678'], users['shubham'][0])

def test_channel_addowner_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_addowner.
    We assume addowner will only be called on members of the group'''

    # Add Shubham to COMP1531 channel
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])
    # Add Shubham to SENG1234 channel
    channel_join(users['shubham'][1], channels['SENG1234'])
    # Add Bob to SENG1234 channel
    channel_join(users['bob'][1], channels['SENG1234'])
    # Add BOB to PHY5678 channel
    channel_join(users['bob'][1], channels['PHY5678'])

    # Check AccessError when the authorised user is not an owner of Flockr
    # nor an owner of the channel
    with pytest.raises(AccessError):

        channel_addowner(users['marley'][1], channels['COMP1531'], users['shubham'][0])

    with pytest.raises(AccessError):

        channel_addowner(users['shubham'][1], channels['COMP1531'], users['marley'][0])

def test_check_add_owner_functionality(users, channels):
    '''Make Shubham an owner of SENG1234; Bob (flokr owner) should
    be able to add shubham as an owner of SENG1234
    despite not being an owner himself. Hence, an AccessError should not be raised'''

    channel_invite(users['marley'][1], channels['SENG1234'], users['shubham'][0])
    channel_addowner(users['bob'][1], channels['SENG1234'], users['shubham'][0])

    # Add Smith to SENG1234
    channel_invite(users['marley'][1], channels['SENG1234'], users['smith'][0])

    # If Shubam is correctly added as an owner, he should be able to add smith as an owner
    # of SENG1234 with no AccesError raised. Note that we invite marley as a member first.
    channel_addowner(users['shubham'][1], channels['SENG1234'], users['smith'][0])

def test_channel_removeowner_inputerror(users, channels):
    ''' Test all possible InputError cases for channel_removeowner'''

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['SENG1234'] + 30
    invalid_channel_id_c = channels['PHY5678'] + 40

    # Checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        channel_removeowner(users['bob'][1], invalid_channel_id_a, users['marley'][0])

    with pytest.raises(InputError):

        channel_removeowner(users['marley'][1], invalid_channel_id_b, users['shubham'][0])

    with pytest.raises(InputError):

        channel_removeowner(users['shubham'][1], invalid_channel_id_c, users['bob'][0])

    # Input error when user with user id u_id is not an owner of the channel
    with pytest.raises(InputError):

        channel_removeowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    with pytest.raises(InputError):

        channel_removeowner(users['shubham'][1], channels['PHY5678'], users['marley'][0])

def test_channel_removeowner_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_removeowner'''

    # Add Shubham to COMP1531 channel and make him an owner
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])
    channel_addowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Add Shubham to SENG1234
    channel_join(users['shubham'][1], channels['SENG1234'])

    # Check AccessError when the authorised user is not an owner of Flockr
    # nor an owner of the channel
    with pytest.raises(AccessError):

        channel_removeowner(users['marley'][1], channels['COMP1531'], users['shubham'][0])

    with pytest.raises(AccessError):

        channel_removeowner(users['shubham'][1], channels['SENG1234'], users['marley'][0])

def test_channel_removeowner_functionality(users, channels):
    '''if the removeowner function is working properly, then
    upon removing an owner we should be able to add them back as an
    owner again. If the removeowner function doesn't work proerly,
    then upon calling the addowner function (immediately after the
    removeowner function) an InputError would be raised.'''

    # Add Marley to COMP1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['marley'][0])
    # Add Shubham to COMP1531
    channel_invite(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Add marley and shubham to the owner of channel of channel_id_COMP1531
    channel_addowner(users['bob'][1], channels['COMP1531'], users['marley'][0])
    channel_addowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Remove owner marley and shubham
    channel_removeowner(users['bob'][1], channels['COMP1531'], users['marley'][0])
    channel_removeowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

    # Add marley and shubham to the owner of channel of channel_id_COMP1531
    # Should not raise an InputError
    channel_addowner(users['bob'][1], channels['COMP1531'], users['marley'][0])
    channel_addowner(users['bob'][1], channels['COMP1531'], users['shubham'][0])

def test_removeowner_not_member(users, channels):
    '''removeowner function should not be called on non-members'''

    with pytest.raises(InputError):
        channel_removeowner(users['shubham'][1], channels['PHY5678'], users['bob'][0])

def test_channel_invite_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_invite(users['shubham'][1]+'boss', channels['COMP1531'], users['bob'][0])

def test_channel_details_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_details(users['bob'][1]+'heya', channels['COMP1531'])

def test_channel_messages_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_messages(users['bob'][1]+'see ya', channels['SENG1234'], 0)

def test_channel_leave_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_leave(users['shubham'][1]+'real boss', channels['SENG1234'])

def test_channel_join_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_join(users['bob'][1]+'heya', channels['SENG1234'])

def test_channel_addowner_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''
    channel_invite(users['marley'][1], channels['SENG1234'], users['shubham'][0])

    with pytest.raises(AccessError):
        channel_addowner(users['marley'][1]+'bss', channels['SENG1234'], users['shubham'][0])

def test_channel_removeowner_token_exception(users, channels):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channel_removeowner(users['bob'][1]+'hero', channels['SENG1234'], users['marley'][0])

def test_channel_invite_already_member_exception(users, channels):

    with pytest.raises(AccessError):
        channel_invite(users['bob'][1], channels['COMP1531'], users['bob'][0])

