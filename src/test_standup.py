'''
H15 Orange, Team 3

Tests for standup.py functions for
assignment 1 spec. Iteration 3
'''

import pytest
from other import clear
from time import sleep
from channels import channels_create
from auth import auth_register
from datetime import datetime
from threading import active_count
from error import InputError, AccessError
from standup import standup_start, standup_send, standup_active
from channel import channel_messages, channel_join

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

################################################################################
#                           standup_start()                                    #
################################################################################

def test_exception_standup_start(users, channels):
    """Testing for exception raises for standup start function"""

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['SENG1234'] + 30
    invalid_channel_id_c = channels['PHY5678'] + 40

    # Checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        standup_start(users['bob'][1], invalid_channel_id_a, '10')

    with pytest.raises(InputError):

        standup_start(users['marley'][1], invalid_channel_id_b, '10')

    with pytest.raises(InputError):

        standup_start(users['shubham'][1], invalid_channel_id_c, '20')

def test_standup_running_start(users, channels):
    """Testing for exception raises for standup start function"""

    # Starting a standup and capturing errors raises for running standup
    standup_start(users['bob'][1], channels['COMP1531'], '2')

    with pytest.raises(InputError):
        standup_start(users['bob'][1], channels['COMP1531'], '10')

def test_standup_two_channels(users, channels):
    '''Testing that two standups can be started simultaneously in two different channels'''

    sleep(3)

    # Starting first standup

    standup_start(users['bob'][1], channels['COMP1531'], '5')

    # Starting second standup without sleeping

    standup_start(users['marley'][1], channels['SENG1234'], '5')

def test_token_exception_standup_start(channels):
    """Testing for exception raises for standup start function"""

    # Invalid token errors in standup start function

    random_token_1 = """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowfQ.
                        vmWc4QFlgjc6PlMHz6HiO6ryabuzJMI1aISPP8twloA"""

    with pytest.raises(AccessError):
        standup_start(random_token_1, channels['COMP1531'], '10')

    with pytest.raises(AccessError):
        standup_start(random_token_1, channels['SENG1234'], '45')

def test_start_process(users, channels):
    """Testing that standup/start starts the standup proccess succesfully"""

    current_count = active_count()
    standup_start(users['bob'][1], channels['COMP1531'], '1')

    new_count = active_count()
    assert new_count == current_count + 1

def test_start_return_check(users, channels):
    """Testing that standup/start returns the appropriate return value"""

    sleep(2)

    time_finish = standup_start(users['bob'][1], channels['COMP1531'], '1')

    assert round(time_finish['time_finish']) == round(1 + datetime.now().timestamp())

################################################################################
#                     standup_active()                                         #
################################################################################

def test_active_invalid_token_handling(channels):
    '''Testing for invalid tokens in standup_active function'''

    # Invalid token errors in standup active function

    random_token_2 = """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowfQ.
                        vmwC4QFlgjc6PlMHz6HiO6ryabuzJMI1aIspp8twloA"""

    with pytest.raises(AccessError):
        standup_active(random_token_2, channels['COMP1531'])

    with pytest.raises(AccessError):
        standup_active(random_token_2, channels['SENG1234'])

def test_active_inavalid_channel(users, channels):
    """Testing for exception raises for standup start function"""

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['SENG1234'] + 30
    invalid_channel_id_c = channels['PHY5678'] + 40

    # Checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        standup_active(users['bob'][1], invalid_channel_id_a)

    with pytest.raises(InputError):

        standup_active(users['marley'][1], invalid_channel_id_b)

    with pytest.raises(InputError):

        standup_active(users['shubham'][1], invalid_channel_id_c)

def test_active_implementation(users, channels):
    """Testing for the functionality of the standup_active() function"""

    # Testing for correct return type before standup started
    result = standup_active(users['shubham'][1], channels['SENG1234'])

    assert result['is_active'] == False

    # Testing for correct return tupe after a standup has been started

    standup_start(users['shubham'][1], channels['SENG1234'], '5')

    result_1 = standup_active(users['shubham'][1], channels['SENG1234'])

    assert result_1['is_active'] == True

def test_active_finish_time_check(users, channels):
    """Testing that the standup_active() returns the correct finish_time and is_active value"""

    standup_start(users['shubham'][1], channels['SENG1234'], '5')

    time_finish = standup_active(users['shubham'][1], channels['SENG1234'])

    assert round(time_finish['time_finish']) == round(5 + datetime.now().timestamp())

    # Testing that the standup_active() function makes is_active false when standup finishes

    sleep(5)

    result_active = standup_active(users['shubham'][1], channels['SENG1234'])

    assert result_active['is_active'] == False

################################################################################
#                    standup_send()                                            #
################################################################################

def test_send_exception_channel_id(users, channels):
    """Testing for exception raises in standup_send() function when invalid channel id is passed"""

    # Generate invalid channel_id by adding arbitrary numbers to the only valid channel_id available
    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['SENG1234'] + 30
    invalid_channel_id_c = channels['PHY5678'] + 40

    # Checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        standup_send(users['bob'][1], invalid_channel_id_a, "Hello")

    with pytest.raises(InputError):

        standup_send(users['marley'][1], invalid_channel_id_b, "World")

    with pytest.raises(InputError):

        standup_send(users['shubham'][1], invalid_channel_id_c, "COMP1531")

def test_send_exception_member(users, channels):
    """Testing for exception raises in send() function when user is not a member of the channel"""

    # Checking for access errors when and unauthorized user sends the message

    standup_start(users['bob'][1], channels['COMP1531'], '5')

    with pytest.raises(AccessError):

        standup_send(users['shubham'][1], channels['COMP1531'], "Hello")

def test_send_exception_message_length(users, channels):
    """Testing for exception raises in send() function when message length is more than limit"""

    # Checking for input errors when user sends a long message

    with pytest.raises(InputError):

        standup_send(users['shubham'][1], channels['COMP1531'], 'I often think," she continued\
        after a short pause, drawing neare to the prince and smiling amiably at him as if to show \
        that political and social topics were ended and the time had come for intimate \
        conversation-"I often think how unfairly sometimes the joys of life are distributed. \
        Why has fate given you two such splendid children? I don''t speak of Anatole, your \
        youngest. I don''t like him," she added in a tone admitting of no rejoinder and raising \
        her eyebrows."Two such charming children. And really you appreciate them less than anyone,\
        and so you don''t deserve to have them." And she smiled her ecstatic smile."I can''t help\
        it," said the prince. "Lavater would have said ,I lack the bump of paternity.""Don''t\
        joke; I mean to have a serious talk with you. Do you know I am dissatisfied with your\
        younger son? Between ourselves" (and herface assumed its melancholy expression),\
        "he was mentioned at Her Majesty''s and you were pitied...."The prince\
        answered nothing, but she looked at him significantly"')

def test_send_exception_invalid_token(channels):
    """Testing for exception raises in send() function when unauthorized user joins in"""

    # Checking for input errors when invalid token is passed

    random_token_2 = """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI2Mij9.eyJ1X2lkIjowfQ.
                        vmwC4QFlgjc6PlMHz6HiO6ryabuzJMI1aIspp8twloA"""

    with pytest.raises(AccessError):
        standup_send(random_token_2, channels['PHY5678'], "hi")

    with pytest.raises(AccessError):
        standup_send(random_token_2, channels['SENG1234'], "this is comp1531")

def test_send_exception_no_standup_running(users, channels):
    '''Testing for input errors when no standup is running and
        an attempt to send a message is made'''
    sleep(5)

    with pytest.raises(InputError):
        standup_send(users['marley'][1], channels['SENG1234'], "hello world!")

    with pytest.raises(InputError):
        standup_send(users['bob'][1], channels['PHY5678'], "COMP1531")

def test_send_implementation(users, channels):
    '''Testing for implementation of standup send function'''

    standup_start(users['bob'][1], channels['COMP1531'], '5')
    standup_send(users['bob'][1], channels['COMP1531'], "hello")
    standup_send(users['bob'][1], channels['COMP1531'], "This is a standup")

    sleep(5)

    result_standup = "boblin : " + "hello\n"
    result_standup = result_standup + "boblin : " + "This is a standup\n"
    standup_messages = channel_messages(users['bob'][1], channels['COMP1531'], 0)
    assert standup_messages['messages'][0]['message'] == result_standup

def test_send_implementation_2(users, channels):
    '''Testing for implementation of standup send function Test 2'''

    standup_start(users['marley'][1], channels['SENG1234'], '5')
    
    standup_send(users['marley'][1], channels['SENG1234'], "This is standup number 2")
    standup_send(users['marley'][1], channels['SENG1234'], "1")

    # Second user joins the channel and tries to send a message

    channel_join(users['shubham'][1], channels['SENG1234'])

    standup_send(users['shubham'][1], channels['SENG1234'], "Have I joined the standup ?")
    standup_send(users['marley'][1], channels['SENG1234'], "yes")

    result_standup = "marleylin : This is standup number 2\n" + "marleylin : 1\n"
    result_standup = result_standup + "shubhamjohar : Have I joined the standup ?\n"
    result_standup = result_standup + "marleylin : yes\n"

    sleep(5)
    standup_messages = channel_messages(users['marley'][1], channels['SENG1234'], 0)

    assert standup_messages['messages'][0]['message'] == result_standup
