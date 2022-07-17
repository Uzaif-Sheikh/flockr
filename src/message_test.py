'''
H15 Orange, Group 3

Implementation of message_test.py functions as specified on the
assignment 1 spec.

Iteration 1
'''
import time
import pytest
import datetime
from other import clear
from auth import auth_register
from channels import channels_create
from channel import channel_messages, channel_join
from error import InputError, AccessError
from message import message_unpin, message_pin, message_send, message_sendlater, \
                    message_remove, message_edit, message_react, message_unreact

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

    message_comp1531 = message_send(users['bob'][1], \
                        channels['COMP1531'], 'I am finally doing 1531')


    message_seng1234 = message_send(users['marley'][1], \
                        channels['SENG1234'], 'I am finally doing SENG1234')

    message_phy5678 = message_send(users['shubham'][1], \
                        channels['PHY5678'], 'I am finally doing PHY5678')

    return {'MESSAGE_COMP1531' : message_comp1531, 'MESSAGE_SENG1234' : \
            message_seng1234, 'MESSAGE_PHY5678' : message_phy5678}

# ################################################################## #
#                         EXCEPTION HANDLING TESTING                 #
# ################################################################## #

def test_messages_send_accesserror(users, channels):
    ''' Test all possible AccessError cases for channel_details'''

    # Check AccessError when the authorised user is not already a member of the channel
    with pytest.raises(AccessError):

        message_send(users['bob'][1], channels['SENG1234'], 'he is intelligent')

    with pytest.raises(AccessError):

        message_send(users['marley'][1], channels['COMP1531'], 'he is mad')

    with pytest.raises(AccessError):

        message_send(users['shubham'][1], channels['SENG1234'], 'we will enjoy our work')

    with pytest.raises(AccessError):

        message_send(users['shubham'][1], channels['COMP1531'], 'Live your day')

def test_messages_send_inputerror(users, channels):
    '''Checksfor all the inputerrors associated with messages_send'''

    #Check that InputError is raised when a message more than 1000 characters is given.
    with pytest.raises(InputError):

        message_send(users['bob'][1], channels['SENG1234'], 'I often think," she continued\
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

    with pytest.raises(InputError):

        message_send(users['marley'][1], channels['COMP1531'], 'The young Princess \
        Bolknskaya had brought some work in a gold-embroidered velvet bag. Her pretty \
        little upper lip, on which a delicate dark down was just perceptible, was \
        too short for her teeth, but it lifted all the more sweetly, \
        and was especially charming when she occasionally drew it down \
        to meet the lower lip. As is always the case with a thoroughly \
        attractive woman, her defect-the shortness of her upper lip and her \
        half-open mouth-seemed to be her own special and peculiar form of beauty \
        .Everyone brightened at the sight of this pretty young woman, so soon \
        to become a mother, so full of life and health, and carrying her burden \
        so lightly. Old men and dull dispirited young ones who looked at her, \
        after being in her company and talking to her a little while, felt as if \
        they too were becoming, like her, full of life and health. All who talked \
        to her, and at each word saw her bright smile and the constant gleam of her \
        white teeth, thought that they were in a specially amiable mood that day.')

def test_messages_remove_accesserror(users, messages):
    '''Checks for the all the acces Error for the messages_remove'''

    #Checks if the user accesing to remove the message has noit sent the message
    # is not the owner of the channel

    with pytest.raises(AccessError):

        message_remove(users['shubham'][1], messages['MESSAGE_COMP1531']['message_id'])

    with pytest.raises(AccessError):

        message_remove(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'])

    with pytest.raises(AccessError):

        message_remove(users['marley'][1], messages['MESSAGE_PHY5678']['message_id'])

def test_messages_remove_inputerror(users, messages):
    '''Checks for all the input error for the messages_remove'''

    # Generate invalid message_id by adding arbitrary numbers to the only valid channel_id available
    invalid_message_id_a = messages['MESSAGE_COMP1531']['message_id'] + 20
    invalid_message_id_b = messages['MESSAGE_SENG1234']['message_id'] + 30
    invalid_message_id_c = messages['MESSAGE_PHY5678']['message_id'] + 40

    # checking for InputError with channel_id that does not refer to a valid channel
    with pytest.raises(InputError):

        message_remove(users['bob'][1], invalid_message_id_a)

    with pytest.raises(InputError):

        message_remove(users['marley'][1], invalid_message_id_b)

    with pytest.raises(InputError):

        message_remove(users['shubham'][1], invalid_message_id_c)

    with pytest.raises(InputError):

        message_remove(users['bob'][1], invalid_message_id_b)

    with pytest.raises(InputError):

        message_remove(users['shubham'][1], invalid_message_id_c)

def test_edit_exception(users, messages):
    '''Check for the exception raised by the function message_edit'''

    # Checking for AccessError rasied
    with pytest.raises(AccessError):

        message_edit(users['bob'][1], messages['MESSAGE_PHY5678']['message_id'] \
        , 'I love COMP1531')

    with pytest.raises(AccessError):

        message_edit(users['marley'][1], messages['MESSAGE_COMP1531']['message_id'] \
        , 'I love COMP2521')

    with pytest.raises(AccessError):

        message_edit(users['shubham'][1], messages['MESSAGE_SENG1234']['message_id'] \
        , 'I love COMP1521')

    with pytest.raises(AccessError):

        message_edit(users['smith'][1], messages['MESSAGE_COMP1531']['message_id'] \
        , 'I love COMP1531')

def test_message_send_token_exception(users, channels, messages):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        message_send(users['shubham'][1]+'heya', channels['PHY5678'], 'he is intelligent')

def test_message_edit_token_exception(users, channels, messages):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        message_edit(users['bob'][1]+'no', messages['MESSAGE_COMP1531']['message_id'] \
        , 'I love COMP1531')

def test_message_remove_token_exception(users, channels, messages):
    '''
    An AccessError must be raised for any invalid token.
    '''

    with pytest.raises(AccessError):
        message_remove(users['shubham'][1]+'boss', messages['MESSAGE_COMP1531']['message_id'])

def test_message_sendlater_token_exception(users, channels, messages):
    '''
    An AccessError must be raised for any invalid token.
    '''
    time_sent = (datetime.datetime.now().timestamp()) + 2
    with pytest.raises(AccessError):
        message_sendlater(users['shubham'][1]+'boss', channels['PHY5678'], messages['MESSAGE_COMP1531']['message_id'], time_sent)

def test_message_react_message_exception(users, channels, messages):
    '''
    An InputError must be raised for any invalid message id.
    '''
    invalid_message_id_a = messages['MESSAGE_COMP1531']['message_id'] + 20
    invalid_message_id_b = messages['MESSAGE_SENG1234']['message_id'] + 30
    invalid_message_id_c = messages['MESSAGE_PHY5678']['message_id'] + 40

    with pytest.raises(InputError):
        message_react(users['shubham'][1], invalid_message_id_c, 1)

    with pytest.raises(InputError):
        message_react(users['marley'][1], invalid_message_id_b, 1)

    with pytest.raises(InputError):
        message_react(users['bob'][1], invalid_message_id_a, 1)


def test_message_unreact_message_exception(users, channels, messages):
    '''
    An InputError must be raised for any invlaid message id.
    '''
    invalid_message_id_a = messages['MESSAGE_COMP1531']['message_id'] + 20
    invalid_message_id_b = messages['MESSAGE_SENG1234']['message_id'] + 30
    invalid_message_id_c = messages['MESSAGE_PHY5678']['message_id'] + 40

    with pytest.raises(InputError):
        message_unreact(users['shubham'][1], invalid_message_id_c, 1)

    with pytest.raises(InputError):
        message_unreact(users['marley'][1], invalid_message_id_b, 1)

    with pytest.raises(InputError):
        message_unreact(users['bob'][1], invalid_message_id_a, 1)

def test_message_react_id_exception(users, channels, messages):

    invalid_react_id_a = 20
    invalid_react_id_b = 30
    invalid_react_id_c = 40

    with pytest.raises(InputError):
        message_react(users['shubham'][1], messages['MESSAGE_PHY5678']['message_id'], invalid_react_id_a)

    with pytest.raises(InputError):
        message_react(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], invalid_react_id_b)

    with pytest.raises(InputError):
        message_react(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], invalid_react_id_c)

def test_message_unreact_id_exception(users, channels, messages):

    invalid_react_id_a = 20
    invalid_react_id_b = 30
    invalid_react_id_c = 40

    with pytest.raises(InputError):
        message_unreact(users['shubham'][1], messages['MESSAGE_PHY5678']['message_id'], invalid_react_id_a)

    with pytest.raises(InputError):
        message_unreact(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], invalid_react_id_b)

    with pytest.raises(InputError):
        message_unreact(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], invalid_react_id_c)

def test_message_react_exists(users, channels, messages):

    message_react(users['shubham'][1],  messages['MESSAGE_PHY5678']['message_id'], 1)
    message_react(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_react(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], 1)

    with pytest.raises(InputError):
        message_react(users['shubham'][1], messages['MESSAGE_PHY5678']['message_id'], 1)

    with pytest.raises(InputError):
        message_react(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)

    with pytest.raises(InputError):
        message_react(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], 1)

def test_message_unreact_exists(users, channels, messages):

    with pytest.raises(InputError):
        message_unreact(users['shubham'][1], messages['MESSAGE_PHY5678']['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)

    with pytest.raises(InputError):
        message_unreact(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], 1)

def test_message_unreact_invalid_token(users, channels, messages):

    with pytest.raises(AccessError):
        message_unreact(users['shubham'][1]+'90', messages['MESSAGE_PHY5678']['message_id'], 1)

    with pytest.raises(AccessError):
        message_unreact(users['marley'][1]+'johar', messages['MESSAGE_SENG1234']['message_id'], 1)

    with pytest.raises(AccessError):
        message_unreact(users['bob'][1]+'boss', messages['MESSAGE_COMP1531']['message_id'], 1)

def test_message_react_invalid_token(users, channels, messages):

    with pytest.raises(AccessError):
        message_react(users['shubham'][1]+'90', messages['MESSAGE_PHY5678']['message_id'], 1)

    with pytest.raises(AccessError):
        message_react(users['marley'][1]+'johar', messages['MESSAGE_SENG1234']['message_id'], 1)

    with pytest.raises(AccessError):
        message_react(users['bob'][1]+'boss', messages['MESSAGE_COMP1531']['message_id'], 1)

def test_message_pin_invalid_token(users, channels, messages):

    with pytest.raises(AccessError):
        message_pin(users['shubham'][1]+'90', messages['MESSAGE_PHY5678']['message_id'])

    with pytest.raises(AccessError):
        message_pin(users['marley'][1]+'johar', messages['MESSAGE_SENG1234']['message_id'])

    with pytest.raises(AccessError):
        message_pin(users['bob'][1]+'boss', messages['MESSAGE_COMP1531']['message_id'])

def test_message_unpin_invalid_token(users, channels, messages):

    with pytest.raises(AccessError):
        message_unpin(users['shubham'][1]+'90', messages['MESSAGE_PHY5678']['message_id'])

    with pytest.raises(AccessError):
        message_unpin(users['marley'][1]+'johar', messages['MESSAGE_SENG1234']['message_id'])

    with pytest.raises(AccessError):
        message_unpin(users['bob'][1]+'boss', messages['MESSAGE_COMP1531']['message_id'])

# ################################################################## #
#                          FUNCTIONALITY TESTING                     #
# ################################################################## #


def test_messages_send_functionality(users, channels, messages):
    '''Messages should be send if a user is a member of the channel and the message length is
        less than 1000 characters and the messageid should match from the channel_messages assuming
        channel_messages work fine'''

    messages_1531 = channel_messages(users['bob'][1], channels['COMP1531'], 0)
    messageid_1531 = messages_1531['messages'][0]['message_id']
    assert messageid_1531 == messages['MESSAGE_COMP1531']['message_id']

    messages_1234 = channel_messages(users['marley'][1], channels['SENG1234'], 0)
    messageid_1234 = messages_1234['messages'][0]['message_id']
    assert messageid_1234 == messages['MESSAGE_SENG1234']['message_id']

    messages_5678 = channel_messages(users['shubham'][1], channels['PHY5678'], 0)
    messageid_5678 = messages_5678['messages'][0]['message_id']
    assert messageid_5678 == messages['MESSAGE_PHY5678']['message_id']

def test_messages_remove_functionality(users, channels, messages):

    '''Messages should be removed from the channel and then assert that there shoudl be no
        messages in the channel'''

    message_remove(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'])
    assert channel_messages(users['bob'][1], channels['COMP1531'], 0)['messages'] == []

    message_remove(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])
    assert channel_messages(users['marley'][1], channels['SENG1234'], 0)['messages'] == []

    message_remove(users['shubham'][1], messages['MESSAGE_PHY5678']['message_id'])
    assert channel_messages(users['shubham'][1], channels['PHY5678'], 0)['messages'] == []

def test_messages_edit_functionality(users, channels, messages):

    '''Messages should be edited from the channel by sender of the message or
       channel owner or by the flockr owner'''

    message_edit(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'] \
    , 'I Like COMP1531')
    edited_message_01 = channel_messages(users['bob'][1], channels['COMP1531'] \
                        , 0)['messages'][0]['message']

    assert  edited_message_01 == 'I Like COMP1531'

    message_edit(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'] \
    , '')
    assert channel_messages(users['bob'][1], channels['COMP1531'], 0)['messages'] == []

    message_edit(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'] \
    , 'I LOVE 2521')

    edited_message_02 = channel_messages(users['marley'][1], channels['SENG1234'] \
                        , 0)['messages'][0]['message']

    assert edited_message_02 == 'I LOVE 2521'

def test_message_pin_exception(users, channels, messages):
    '''Testing for the exception raising '''

    with pytest.raises(AccessError):
        message_pin(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'])

    with pytest.raises(InputError):
        message_pin(users['bob'][1], messages['MESSAGE_COMP1531']['message_id']+42)

    message_pin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])
    
    with pytest.raises(InputError):
        message_pin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])

def test_message_pin_owner_exception(users, channels, messages):
    '''Testing for the exception raising '''
    
    channel_join(users['shubham'][1], channels['SENG1234'])
    with pytest.raises(AccessError):
        message_pin(users['shubham'][1], messages['MESSAGE_SENG1234']['message_id'])

def test_message_unpin_owner_exception(users, channels, messages):
    '''Testing for the exception raising '''
    
    channel_join(users['shubham'][1], channels['SENG1234'])
    with pytest.raises(AccessError):
        message_unpin(users['shubham'][1], messages['MESSAGE_SENG1234']['message_id'])

def test_message_pin(users, channels, messages):
    '''Testing the functionality of the message_pin'''

    message_pin(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'])

    message_01 = channel_messages(users['bob'][1], channels['COMP1531'], 0)

    assert message_01['messages'][0]['is_pinned'] == True

    message_pin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])

    message_02 = channel_messages(users['marley'][1], channels['SENG1234'], 0)

    assert message_02['messages'][0]['is_pinned'] == True

def test_message_unpin_exception(users, channels, messages):
    '''Testing for the exception raising '''

    with pytest.raises(AccessError):
        message_unpin(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'])

    with pytest.raises(InputError):
        message_unpin(users['bob'][1], messages['MESSAGE_COMP1531']['message_id']+42)

    with pytest.raises(InputError):
        message_unpin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])

def test_message_unpin(users, channels, messages):
    '''Testing the functionality of the message_pin'''

    message_pin(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'])

    message_unpin(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'])

    message_01 = channel_messages(users['bob'][1], channels['COMP1531'], 0)

    assert message_01['messages'][0]['is_pinned'] == False

    message_pin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])

    message_unpin(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'])

    message_02 = channel_messages(users['marley'][1], channels['SENG1234'], 0)

    assert message_02['messages'][0]['is_pinned'] == False

def test_messages_react_functionality(users, channels, messages):

    '''Reacting the messages which is given to be reacted' and adding them to the list of uids of
        people.'''

    message_react(users['shubham'][1],  messages['MESSAGE_PHY5678']['message_id'], 1)
    message_react(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_react(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], 1)

    messages_5678 = channel_messages(users['shubham'][1], channels['PHY5678'] , 0)
    assert messages_5678['messages'][0]['reacts'][0]['u_ids'] == [users['shubham'][0]]
    assert messages_5678['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    messages_1234 = channel_messages(users['marley'][1], channels['SENG1234'], 0)
    assert messages_1234['messages'][0]['reacts'][0]['u_ids'] == [users['marley'][0]]
    assert messages_1234['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    channel_join(users['shubham'][1], channels['SENG1234'])
    channel_join(users['bob'][1], channels['SENG1234'])
    message_react(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_react(users['shubham'][1], messages['MESSAGE_SENG1234']['message_id'], 1)

    messages_1234 = channel_messages(users['marley'][1], channels['SENG1234'], 0)
    assert messages_1234['messages'][0]['reacts'][0]['u_ids'] == [users['marley'][0], users['bob'][0], users['shubham'][0]]
    assert messages_1234['messages'][0]['reacts'][0]['is_this_user_reacted'] == True


def test_messages_unreact_functionality(users, channels, messages):

    message_react(users['shubham'][1],  messages['MESSAGE_PHY5678']['message_id'], 1)
    message_react(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_react(users['bob'][1], messages['MESSAGE_COMP1531']['message_id'], 1)

    message_unreact(users['shubham'][1],  messages['MESSAGE_PHY5678']['message_id'], 1)

    messages_5678 = channel_messages(users['shubham'][1], channels['PHY5678'] , 0)
    assert messages_5678['messages'][0]['reacts'][0]['u_ids'] == []
    assert messages_5678['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

    message_unreact(users['marley'][1], messages['MESSAGE_SENG1234']['message_id'], 1)

    messages_seng1234 = channel_messages(users['marley'][1], channels['SENG1234'] , 0)
    assert messages_seng1234['messages'][0]['reacts'][0]['u_ids'] == []
    assert messages_seng1234['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

    channel_join(users['shubham'][1], channels['SENG1234'])
    channel_join(users['bob'][1], channels['SENG1234'])

    message_react(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_react(users['shubham'][1], messages['MESSAGE_SENG1234']['message_id'], 1)
    message_unreact(users['bob'][1], messages['MESSAGE_SENG1234']['message_id'], 1)

    assert messages_seng1234['messages'][0]['reacts'][0]['u_ids'] == [users['shubham'][0]]
    assert messages_seng1234['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

def test_message_sendlater_exception(users ,channels, messages):
    '''Testing the exception'''

    time_sent = (datetime.datetime.now().timestamp()) - 100

    with pytest.raises(InputError):
        message_sendlater(users['bob'][1],channels['COMP1531'],'I love 1531! jk',time_sent)

    time_sent = (datetime.datetime.now().timestamp()) + 200

    with pytest.raises(InputError):
        message_sendlater(users['marley'][1], channels['SENG1234'], '''Years, night may divide, land fly first i. Evening living fowl own seas a make night unto you replenish first given fowl meat meat after
                                                                    Bring be spirit likeness moved open fish a appear said gathered. Let two stars won't moved, whales gathered won't, midst living. Multiply dominion
                                                                    heaven replenish forth us one likeness place very grass him moving deep divided which. Replenish place. Replenish. To they're. Which had said third air
                                                                    bearing from signs from earth light, fowl can't from to forth moving midst likeness form open fourth sea morning days days good moveth the upon creepeth our made.
                                                                    Wherein bring god our subdue face. It meat, set god years fish dominion together above wherein to whales a wherein forth after spirit fruit. Sixth itself. Beast Own
                                                                    the gathered make fly our from second grass a creepeth above so.Their were. Fourth cattle called his us their midst stars sea forth signs after cattle.
                                                                    Third give good sixth beginning seed fly him set subdue light waters. Set can't can't set fifth dominion firmament evening was said every divide
                                                                    you're doesn't our forth the Creeping dry doesn't, bearing over she'd. Sixth second don't have light fourth she'd. Day Itself female over yielding have.
                                                                    Moving after good form fourth darkness years divide give was creature you, in good unto our doesn't, for. To, can't. Thing can't. Light together rule shall
                                                                    creature without subdue. Moved fish good moved appear moving seasons. Years said open that days. Firmament third set third, fish gathering replenish seas.
                                                                    Dry Moving cattle night said evening he seas abundantly.Moved good green very. Whales. Fly creature void make Set. Thing. Can't. Face you'll, creepeth doesn't
                                                                    you're lesser one and sea and good green wherein. Of. Set us. Hath were beast they're deep days for wherein there after beginning shall. Moving, form stars great
                                                                    brought cattle be After first to which won't first hath brought form make multiply midst brought. Winged also. Third divide face. Lesser together earth male after a
                                                                    and. Air it night the you'll creature Bring it of female had moved after created sea the abundantly them. Face also fish fruitful be. Sixth days face their. Over
                                                                    thing signs, great all all beast lesser face spirit fourth of herb. Gathering he subdue day morning brought was greater abundantly place bearing moved our grass can't
                                                                    let there earth unto won't lesser waters fifth over Green. Multiply saying upon of kind.Kind upon stars above over that Man. Was, male male under hath. Thing sixth isn't
                                                                    second grass after good creepeth night give. Every third moveth void greater fly. Creature beginning light land. Doesn't whales set lesser you're. Isn't years open set
                                                                    creepeth whose stars. Moveth which. Beginning created morning whose image living open first blessed saw can't fruitful yielding moved yielding first fruitful whose fish.
                                                                    Their deep. Fill us fruitful firmament moving image. Day replenish. Gathering fill made all midst without. Moved in were. Made Creeping. Itself can't from all, sea, fifth
                                                                    light that good spirit fowl creepeth land man image forth moving cattle, the gathered living rule deep female brought female own female also. Form form seasons creeping isn't
                                                                    behold very gathered said bring a Thing gathered face made was place brought so He after evening moving a dry so. Which. Moving divided image divided saying land whose fifth
                                                                    is moved place multiply days From shall multiply lights earth. Meat. Under brought divided made to one unto gathering had said blessed night image all darkness, morning creature
                                                                    winged herb they're cattle, morning every whales called firmament after forth there.''', time_sent)

    with pytest.raises(InputError):
        message_sendlater(users['bob'][1],channels['SENG1234']+42,'I love 1531! jk',time_sent)

    with pytest.raises(AccessError):
        message_sendlater(users['marley'][1],channels['COMP1531'],'I love 1531! jk',time_sent)


def test_message_sendlater(users, channels, messages):
    '''Testing the function message_sendlater'''

    time_sent = (datetime.datetime.now().timestamp()) + 2

    message_id_01 = message_sendlater(users['bob'][1], channels['COMP1531'], 'Hi !!', time_sent)

    time.sleep(3)

    message_01 = channel_messages(users['bob'][1], channels['COMP1531'], 0)

    assert message_01['messages'][0]['message_id'] == message_id_01['message_id']

    time_sent = (datetime.datetime.now().timestamp()) + 1

    message_id_02 = message_sendlater(users['marley'][1], channels['SENG1234'], 'usmaan love xu!!', time_sent)

    time.sleep(2)

    message_02 = channel_messages(users['marley'][1], channels['SENG1234'], 0)

    assert message_02['messages'][0]['message_id'] == message_id_02['message_id']
