'''
H15 Orange, Group 3

Implementation of test_channels.py functions as specified on the
assignment 1 spec. Iteration 1
'''
import pytest
from channels import channels_create, channels_list, channels_listall
from auth import auth_login, auth_register, auth_logout
from other import clear, InputError, AccessError
from channel import channel_invite, channel_details, channel_messages, \
                channel_leave, channel_join, channel_addowner, channel_removeowner

@pytest.fixture(name='users')
def fixture_users():
    '''A pytest fixture which is useful for all other functions,
    it is used to clear() the already existing data structure and then populate it with
    3 different users and returns the (uid,token) pair of these users which can be
    used by other functions for testing'''
    clear()

    # Here, we assume that the auth_register function works perfectly

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

    return {'bob': [u_id_bob, token_bob], 'marley': [u_id_marley, token_marley], \
    'shubham': [u_id_shubham, token_shubham], 'smith': [u_id_smith, token_smith]}

@pytest.fixture(name='channel_users')
def fixture_channel_users(users):
    '''A pytest fixture which is useful for all other functions,
    it is used to clear() the already existing data structure and then populate it with
    3 different channels and returns their channel ids and the users in each channel pair
    and then the channels details list all of which can be used by other functions for testing'''
    # Here, we assume that the channels_create function works perfectly

    # Create COMP1531 channel
    channel_comp1531 = channels_create(users['bob'][1], 'COMP1531', False)
    channel_id_comp1531 = channel_comp1531['channel_id']
    channel_comp1531_details = channel_details(users['bob'][1], channel_id_comp1531)
    channel_comp1531_details['id'] = channel_id_comp1531
    # Create SENG1234 channel
    channel_seng1234 = channels_create(users['marley'][1], 'SENG1234', True)
    channel_id_seng1234 = channel_seng1234['channel_id']
    channel_seng1234_details = channel_details(users['marley'][1], channel_id_seng1234)
    channel_seng1234_details['id'] = channel_id_seng1234

    # Create PHY5678 channel
    channel_phy5678 = channels_create(users['shubham'][1], 'PHY5678', False)
    channel_id_phy5678 = channel_phy5678['channel_id']
    channel_phy5678_details = channel_details(users['shubham'][1], channel_id_phy5678)
    channel_phy5678_details['id'] = channel_id_phy5678
    return {'COMP1531': {'channel_id' :channel_id_comp1531, 'users' : users['bob']}, \
    'SENG1234': {'channel_id' : channel_id_seng1234, 'users' : users['marley']}, \
    'PHY5678': {'channel_id' : channel_id_phy5678, 'users' : users['shubham']}, \
    'all_channels' : [channel_comp1531_details, channel_seng1234_details, channel_phy5678_details]}

def test_channels_listall(users, channel_users):

    '''Tests for channel_listall() using the pytest_fixtures, consists of all possible
    cominations of tests with the channel functions to check whether the listall()
    works perfectly or not'''
    # Testing when channels has the list of the channels which were created by the fixtures
    list_channels = channels_listall(users['marley'][1])
    list_channels_existing = list_channels['channels']

    assert len(list_channels_existing) == len(channel_users['all_channels'])

    assert list_channels_existing[0]['name'] == channel_users['all_channels'][0]['name']
    assert list_channels_existing[0]['channel_id'] == channel_users['all_channels'][0]['id']

    assert list_channels_existing[1]['name'] == channel_users['all_channels'][1]['name']
    assert list_channels_existing[1]['channel_id'] == channel_users['all_channels'][1]['id']

    assert list_channels_existing[2]['name'] == channel_users['all_channels'][2]['name']
    assert list_channels_existing[2]['channel_id'] == channel_users['all_channels'][2]['id']

def test_channels_listall_create(users, channel_users):
    '''Basic test for listall with channels_create(), checks
     that the channel created gets in the list of all channels needed'''
    #testing after adding a new channel
    channel_team3 = channels_create(users['marley'][1], 'team3', True)
    channel_team3_id = channel_team3['channel_id']
    channel_team3_details = channel_details(users['marley'][1], channel_team3_id)

    list_new_channel = channels_listall(users['marley'][1])
    list_after_adding_channel = list_new_channel['channels']

    assert len(list_after_adding_channel) == len(channel_users['all_channels']) + 1
    new_channel_index = len(list_after_adding_channel) - 1
    assert list_after_adding_channel[new_channel_index]['name'] == channel_team3_details['name']
    assert list_after_adding_channel[new_channel_index]['channel_id'] == channel_team3_id

def test_channels_listall_invite(channel_users):
    '''Basic test for listall with channels_invite(), checks
     that the user invited gets added in the channel and has no affect ot the listall.'''
    # Testing with channel_invite

    channel_details_comp1531_before = channel_details(channel_users['COMP1531']
                                                              ['users'][1],
                                                              channel_users['COMP1531']
                                                              ['channel_id'])
    num_members_before = len(channel_details_comp1531_before['all_members'])

    auth_register('usmaanismad@gmail.com', 'iammad123', 'usmaan', 'chandhok')
    login_det_usmaan = auth_login('usmaanismad@gmail.com', 'iammad123')
    uid_usmaan = login_det_usmaan['u_id']

    channel_invite(channel_users['COMP1531']['users'][1], \
    channel_users['COMP1531']['channel_id'], uid_usmaan)

    list_channel_new = channels_listall(channel_users['COMP1531']['users'][1])
    list_after_channel_invite = list_channel_new['channels']

    channel_details_comp1531_invited = channel_details(login_det_usmaan['token'],
                                                               channel_users['COMP1531']
                                                               ['channel_id'])

    assert len(list_after_channel_invite) == 3
    assert list_channel_new['channels'][0]['name'] == channel_users['all_channels'][0]['name']
    assert list_channel_new['channels'][0]['channel_id'] == \
            channel_users['all_channels'][0]['id']

    assert list_channel_new['channels'][1]['name'] == channel_users['all_channels'][1]['name']
    assert list_channel_new['channels'][1]['channel_id'] == \
            channel_users['all_channels'][1]['id']

    assert list_channel_new['channels'][2]['name'] == \
            channel_users['all_channels'][2]['name']
    assert list_channel_new['channels'][2]['channel_id'] == channel_users['all_channels'][2]['id']

    num_members_after = len(channel_details_comp1531_invited['all_members'])
    assert num_members_after == num_members_before + 1

def test_channels_listall_owner(users, channel_users):
    '''Basic test for listall with channels_addowner() and channels_removeowner(), checks
     that the user added as owner and removed as owner has its effect in the channel details,
     but it does'nt aaffect the channel listall'''
    ## Testing for removing/adding owner ##

    # Test 1 Adding user that is not part of the channel as an owner of that channel
    channel_details_seng1234_before = channel_details(channel_users['SENG1234']
                                                              ['users'][1],
                                                              channel_users['SENG1234']
                                                              ['channel_id'])
    num_owners_before = len(channel_details_seng1234_before['owner_members'])

    channel_invite(channel_users['SENG1234']['users'][1],
                           channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_addowner(channel_users['SENG1234']['users'][1],
                             channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_list_shubham = channels_listall(users['shubham'][1])

    channel_details_seng1234_shubham = channel_details(users['shubham'][1],
                                                               channel_users['SENG1234']
                                                               ['channel_id'])

    assert len(channel_list_shubham['channels']) == 3
    assert channel_list_shubham['channels'][0]['name'] == channel_users['all_channels'][0]['name']
    assert channel_list_shubham['channels'][0]['channel_id'] == \
            channel_users['all_channels'][0]['id']

    assert channel_list_shubham['channels'][1]['name'] == channel_users['all_channels'][1]['name']
    assert channel_list_shubham['channels'][1]['channel_id'] == \
            channel_users['all_channels'][1]['id']

    assert channel_list_shubham['channels'][2]['name'] == \
            channel_users['all_channels'][2]['name']
    assert channel_list_shubham['channels'][2]['channel_id'] == \
            channel_users['all_channels'][2]['id']

    num_owners_after = len(channel_details_seng1234_shubham['owner_members'])
    assert num_owners_after == num_owners_before + 1

    # Test 2 Removing an user as an existing owner ##

    # User 1 is removed as an owner of team 4 (channel_id4) by User 4

    num_owners_before_rem = len(channel_details_seng1234_shubham['owner_members'])

    channel_removeowner(channel_users['SENG1234']['users'][1], \
    channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_list_shubham_rem = channels_listall(users['shubham'][1])

    channel_details_seng1234_shubham_rem = channel_details(users['shubham'][1], \
    channel_users['SENG1234']['channel_id'])
    assert len(channel_list_shubham_rem['channels']) == 3

    #The listall still shows the same list of name and
    # channel id's it is unaffected by the channel add or remove owner.
    assert channel_list_shubham_rem['channels'][0]['name'] == \
            channel_users['all_channels'][0]['name']
    assert channel_list_shubham_rem['channels'][0]['channel_id'] == \
            channel_users['all_channels'][0]['id']

    assert channel_list_shubham_rem['channels'][1]['name'] == \
            channel_users['all_channels'][1]['name']
    assert channel_list_shubham_rem['channels'][1]['channel_id'] == \
            channel_users['all_channels'][1]['id']

    assert channel_list_shubham_rem['channels'][2]['name'] == \
            channel_users['all_channels'][2]['name']
    assert channel_list_shubham_rem['channels'][2]['channel_id'] == \
            channel_users['all_channels'][2]['id']

    num_owners_after_rem = len(channel_details_seng1234_shubham_rem['owner_members'])
    assert num_owners_after_rem == num_owners_before_rem - 1

def test_channels_list_empty():
    '''Tests for channel_list() using the pytest_fixtures, consists of all possible
    cominations of tests with the channel functions to check whether the list()
    works perfectly or not'''
    ## Testing Empty list ##
    clear()

    user_xu = auth_register('xugao@gmail.com', 'ilovecomp1531', 'Xu', 'Gao')
    channels_xu = channels_list(user_xu['token'])
    assert channels_xu['channels'] == []

def test_channels_list_user_belonging(channel_users):
    '''Basic test for channels_list which checks if a user belongs to a channel using
        channel list'''
    ## Testing User belonging to a particular is listed by channel_list or not
    # Test 1
    channels_user_1531 = channels_list(channel_users['COMP1531']['users'][1])
    channel_details_user_1531 = channel_details(channel_users['COMP1531']['users'][1], \
    channel_users['COMP1531']['channel_id'])

    assert len(channels_user_1531['channels']) == 1
    assert channels_user_1531['channels'][0]['name'] == channel_details_user_1531['name']
    assert channels_user_1531['channels'][0]['channel_id'] == \
            channel_users['COMP1531']['channel_id']

    # Test 2
    channels_user_seng1234 = channels_list(channel_users['SENG1234']['users'][1])
    channel_details_user_seng1234 = channel_details(channel_users['SENG1234']['users'][1],\
                                    channel_users['SENG1234']['channel_id'])

    assert len(channels_user_seng1234['channels']) == 1
    assert channels_user_seng1234['channels'][0]['name'] == channel_details_user_seng1234['name']
    assert channels_user_seng1234['channels'][0]['channel_id'] == \
            channel_users['SENG1234']['channel_id']

def test_channels_list_user_join(users, channel_users):
    '''Test for channels list which checks that if the user joins a channel
    then then the details for those channels should be reflected in channel list for that
    user'''
    ## Testing for channel join ##

    # Test 1 Joining as a New member of already existing channel
    auth_register('uzisheikh@gmail.com', 'ilovekabab', 'uzaif', 'ogboss')
    loggedin_uzaif = auth_login('uzisheikh@gmail.com', 'ilovekabab')

    channel_join(loggedin_uzaif['token'], channel_users['SENG1234']['channel_id'])
    channel_list_uzaif = channels_list(loggedin_uzaif['token'])

    channel_det_after_adding = channel_details(loggedin_uzaif['token'], \
                                channel_users['SENG1234']['channel_id'])

    assert len(channel_list_uzaif['channels']) == 1
    assert channel_list_uzaif['channels'][0]['channel_id'] == \
            channel_users['SENG1234']['channel_id']
    assert channel_list_uzaif['channels'][0]['name'] == channel_det_after_adding['name']


    # Test 2 Existing User joins another channel

    channel_join(users['bob'][1], channel_users['SENG1234']['channel_id'])

    channel_list_bob = channels_list(users['bob'][1])

    assert len(channel_list_bob['channels']) == 2
    assert channel_list_bob['channels'][0]['channel_id'] == \
            channel_users['COMP1531']['channel_id']
    assert channel_list_bob['channels'][1]['channel_id'] == \
            channel_users['SENG1234']['channel_id']

def test_channels_list_user_leave(users, channel_users):
    '''Basic test to see that if a user leaves a channel then it should be
    reflected in users channels list'''
    ## Testing for channel leave ##

    # Test 1

    channel_leave(users['bob'][1], channel_users['COMP1531']['channel_id'])
    channel_list_bob_leave = channels_list(users['bob'][1])

    assert len(channel_list_bob_leave['channels']) == 0
    assert channel_list_bob_leave['channels'] == []

    #test2

    channel_leave(users['shubham'][1], channel_users['PHY5678']['channel_id'])
    channel_list_shubham_leave = channels_list(users['shubham'][1])

    assert len(channel_list_shubham_leave['channels']) == 0
    #num_channels_shubham = len(channel_list_shubham_leave['channels'])
    assert channel_list_shubham_leave['channels'] == []

def test_channels_list_remadd_owner(users, channel_users):
    '''Test to check that using channel remove and addowner does not
    affect the channel list but brings the changes in channel details'''
    ## Testing for removing/adding owner ##

    # Test 1 Adding user that is not part of the channel as an owner of that channel
    channel_details_seng1234_before = channel_details(channel_users['SENG1234']
                                                              ['users'][1],
                                                              channel_users['SENG1234']
                                                              ['channel_id'])
    num_owners_before = len(channel_details_seng1234_before['owner_members'])

    channel_invite(channel_users['SENG1234']['users'][1],
                           channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_addowner(channel_users['SENG1234']['users'][1],
                             channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_list_shubham = channels_list(users['shubham'][1])

    channel_details_seng1234_shubham = channel_details(users['shubham'][1],
                                                               channel_users['SENG1234']
                                                               ['channel_id'])

    assert len(channel_list_shubham['channels']) == 2
    assert channel_list_shubham['channels'][0]['channel_id'] == \
            channel_users['SENG1234']['channel_id']
    assert channel_list_shubham['channels'][0]['name'] == \
            channel_details_seng1234_shubham['name']

    num_owners_after = len(channel_details_seng1234_shubham['owner_members'])
    assert num_owners_after == num_owners_before + 1

    # Test 2 Removing an user as an existing owner ##

    # User 1 is removed as an owner of team 4 (channel_id4) by User 4

    num_owners_before_rem = len(channel_details_seng1234_shubham['owner_members'])

    channel_removeowner(channel_users['SENG1234']['users'][1], \
    channel_users['SENG1234']['channel_id'], users['shubham'][0])
    channel_list_shubham_rem = channels_list(users['shubham'][1])

    channel_details_seng1234_shubham_rem = channel_details(users['shubham'][1], \
    channel_users['SENG1234']['channel_id'])
    assert len(channel_list_shubham_rem['channels']) == 2

    assert channel_list_shubham_rem['channels'][0]['channel_id'] == \
            channel_users['SENG1234']['channel_id']
    assert channel_list_shubham_rem['channels'][0]['name'] == \
            channel_details_seng1234_shubham_rem['name']

    num_owners_after_rem = len(channel_details_seng1234_shubham_rem['owner_members'])
    assert num_owners_after_rem == num_owners_before_rem - 1



#basic test for channel_list and channeL_listall(), independent of fixtures.
def test_all_functions():
    '''Basic test independent of fixtures to test for the newly registered user and the list
    of channels he is a part of'''
    # Test 01
    clear()

    auth_register('usmaanboss@gmail.com', 'ilovexu', 'usmaan', 'chandhok')
    logged_in_boss = auth_login('usmaanboss@gmail.com', 'ilovexu')

    channel_id_team01 = channels_create(logged_in_boss['token'], 'team01', True)

    get_list = channels_list(logged_in_boss['token'])

    auth_register('xugao@gmail.com', 'iloveusmaan', 'xu', 'gao')
    loggedin_xu = auth_login('xugao@gmail.com', 'iloveusmaan')

    channel_join(loggedin_xu['token'], channel_id_team01['channel_id'])

    assert channels_list(loggedin_xu['token']) == get_list


# ################################################################## #
#                    EXCEPTION HANDLING  TESTING                     #
# ################################################################## #

#checking for exception handling while creating the channels
def test_channels_exception_error():
    '''Covers the Exception Handling for Channels_create function with raising InputError'''
    clear()

    user_usmaan = auth_register('usmaan123@gmail.com', 'ilovekabab', 'usmaan', 'boss')
    login_usmaan = auth_login('usmaan123@gmail.com', 'ilovekabab')
    token_usmaan = login_usmaan['token']

    assert user_usmaan == login_usmaan

    with pytest.raises(InputError):

        channels_create(token_usmaan, '', True)

    with pytest.raises(InputError):

        channels_create(token_usmaan, 'iiiiiiiiiiiiiaaaaaaaaaaaammmmboss', True)

    with pytest.raises(InputError):

        channels_create(token_usmaan, 'comp1531channelname11234567', True)

    with pytest.raises(InputError):

        channels_create(token_usmaan, \
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', True)

    with pytest.raises(InputError):

        channels_create(token_usmaan, \
        'jhkafanananabshinayskjijdsnjhanvharatvhargauacudfharahvbfhssguajratnaaratgaajfbv', True)

    auth_logout(token_usmaan)

    login_usmaan_again = auth_login('usmaan123@gmail.com', 'ilovekabab')
    token_new_usmaan = login_usmaan_again['token']

    with pytest.raises(InputError):
        channels_create(token_new_usmaan, 'channeldoesnotexistandweshouldnotcreaterandomchanne', \
                        True)

def test_channels_create_token_exception(users, channel_users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channels_create(users['shubham'][1]+'boss', 'COMP2321', True)

def test_channels_list_token_exception(users, channel_users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channels_list(users['bob'][1]+'zero')

def test_channels_listall_token_exception(users, channel_users):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        channels_listall(users['marley'][1]+'real boss')

