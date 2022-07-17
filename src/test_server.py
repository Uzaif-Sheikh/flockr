'''
H15C, Group 3
Server testing
'''

import re
import json
import pytest
import signal
import datetime
import requests
from time import sleep
from subprocess import Popen, PIPE
from error import InputError, AccessError
import datetime


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture(name='users')
def fixture_users(url):
    '''This is a pytest fixture used to define some user variables required for testing
    in all functions'''

    # Here, we assume that the auth_register function works perfectly

    # Reset data to initial state
    requests.delete(url + 'clear')

    # Creating user Bob, the Flockr owner
    user_bob_register_params = {
        'email': 'bob@gmail.com',
        'password': 'ilovemeatballs',
        'name_first': 'bob',
        'name_last': 'lin',
    }

    # Register
    resp_bob = requests.post(url + 'auth/register', json=user_bob_register_params)
    payload_bob = resp_bob.json()

    #uid and token for bob
    u_id_bob = payload_bob['u_id']
    token_bob = payload_bob['token']

    #Creating member marley
    user_marley_register_params = {
        'email': 'marley@gmail.com',
        'password': 'ilovecheese',
        'name_first': 'marley',
        'name_last': 'lin',
    }

    # Register
    resp_marley = requests.post(url + 'auth/register', json=user_marley_register_params)
    payload_marley = resp_marley.json()

    #uid and bob for marley
    u_id_marley = payload_marley['u_id']
    token_marley = payload_marley['token']

    # Creating member shubham
    user_shubham_register_params = {
        'email': 'shubham@gmail.com',
        'password': 'ilovetoswim',
        'name_first':'shubham',
        'name_last': 'johar',
    }

    # Register
    resp_shubham = requests.post(url + 'auth/register', json=user_shubham_register_params)
    payload_shubham = resp_shubham.json()

    u_id_shubham = payload_shubham['u_id']
    token_shubham = payload_shubham['token']

    # Creating member Smith
    user_smith_register_params = {
        'email': '123@gmail.com',
        'password': '4321!@#$',
        'name_first': 'hayden',
        'name_last': 'smith',
    }

    # Register
    resp_smith = requests.post(url + 'auth/register', json=user_smith_register_params)
    payload_smith = resp_smith.json()

    u_id_smith = payload_smith['u_id']
    token_smith = payload_smith['token']

    return {'bob': {'u_id' : u_id_bob, 'token': token_bob, 'params' : user_bob_register_params}, \
            'marley': {'u_id' : u_id_marley, 'token' : token_marley, \
                        'params' : user_marley_register_params}, \
            'shubham': {'u_id' : u_id_shubham, 'token' : token_shubham, \
                        'params' : user_shubham_register_params}, \
            'smith': {'u_id' : u_id_smith, 'token' : token_smith, \
                        'params' : user_smith_register_params}
           }

@pytest.fixture(name='channels')
def fixture_channels(url, users):
    '''This is a pytest fixture used to define some channel variables required for testing
    in all functions'''

    # Here, we assume that the channels_create function works perfectly

    # Create COMP1531 channel
    comp1531_channel_params = {
        'token': users['bob']['token'],
        'name': 'COMP1531',
        'is_public': True,
    }
    #Get the response and the channel_id for comp1531
    resp_comp1531 = requests.post(url + 'channels/create', json=comp1531_channel_params)
    payload_comp1531 = resp_comp1531.json()
    channel_id_comp1531 = payload_comp1531['channel_id']

    # Create SENG1234 channel
    seng1234_channel_params = {
        'token': users['marley']['token'],
        'name': 'SENG1234',
        'is_public': True,
    }

    #Get the response and the channel_id for seng1234
    resp_seng1234 = requests.post(url + 'channels/create', json=seng1234_channel_params)
    payload_seng1234 = resp_seng1234.json()
    channel_id_seng1234 = payload_seng1234['channel_id']


    # Create PHY5678 channel
    phy5678_channel_params = {
        'token': users['shubham']['token'],
        'name': 'PHY5678',
        'is_public': False,
    }

    #Get the response and the channel_id for phy5678
    resp_phy5678 = requests.post(url + 'channels/create', json=phy5678_channel_params)
    payload_phy5678 = resp_phy5678.json()
    channel_id_phy5678 = payload_phy5678['channel_id']

    return {'COMP1531': channel_id_comp1531, 'SENG1234': channel_id_seng1234,
            'PHY5678': channel_id_phy5678}

@pytest.fixture(name='messages')
def fixture_messages (url, users, channels):
    '''This creates a pytest fixture used to create some messages in the channels'''
    # Here, we assume that the messages_send function works perfectly

    #Create the message for comp1531
    message_comp1531_params = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'message': 'I like comp1531'
    }

    #Get the response and message_id for comp1531
    resp_message_comp1531 = requests.post(url + 'message/send',json=message_comp1531_params)
    message_comp1531_payload = resp_message_comp1531.json()
    messageid_comp1531 = message_comp1531_payload['message_id']

    #Create the message for seng1234
    message_seng1234_params = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
        'message': 'I am finally doing SENG1234',
    }

    #Get the response and message_id for seng1234
    resp_message_seng1234 = requests.post(url + 'message/send',json=message_seng1234_params)
    message_seng1234_payload = resp_message_seng1234.json()
    messageid_seng1234 = message_seng1234_payload['message_id']

     #Create the message for phy5678
    message_phy5678_params = {
        'token': users['shubham']['token'],
        'channel_id': channels['PHY5678'],
        'message': 'I am finally doing PHY5678',
    }

    #Get the response and message_id for phy5678
    resp_message_phy5678 = requests.post(url + 'message/send',json=message_phy5678_params)
    message_phy5678_payload = resp_message_phy5678.json()
    messageid_phy5678 = message_phy5678_payload['message_id']


    return {'MESSAGE_COMP1531' : messageid_comp1531, 'MESSAGE_SENG1234' : \
            messageid_seng1234, 'MESSAGE_PHY5678' : messageid_phy5678}

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_auth_basic(url, users):
    '''Test the basic functionality of auth functions.
    In this test story, the user registers, logs out,
    and then logs back in'''

    # Logging out user_bob
    userbob_logout_params = {'token': users['bob']['token']}
    resp_bob_logout = requests.post(url + 'auth/logout', json=userbob_logout_params)
    payload_bob_logout = resp_bob_logout.json()

    # Check that logout was successful
    assert payload_bob_logout['is_success'] == True

    # Login usmaan again
    userbob_login_again_params = {
        'email' : users['bob']['params']['email'],
        'password' : users['bob']['params']['password']
    }

    resp_bob_login_again = requests.post(url + 'auth/login', json=userbob_login_again_params)
    payload_bob_login_again = resp_bob_login_again.json()

    # Check that the correct u_id is returned
    assert payload_bob_login_again['u_id'] == users['bob']['u_id']

def test_channels_basic(url, users, channels):
    '''Test the basic functionality of channels functions.
    In this test story, the user registers, logs out,
    and then logs back in'''

    # List the channels in which user_marley is in
    marley_channels_list_params = {'token': users['marley']['token']}
    resp_channels_marley = requests.get(url + 'channels/list', params=marley_channels_list_params)
    payload_channels_marley = resp_channels_marley.json()
    assert payload_channels_marley == \
            {'channels': [{'channel_id': channels['SENG1234'], 'name': 'SENG1234'}]}

    # List all channels
    channels_listall_params = {'token': users['marley']['token']}
    resp_listall = requests.get(url + 'channels/listall', params=channels_listall_params)
    payload_listall = resp_listall.json()
    assert payload_listall == {'channels': [{'channel_id': channels['COMP1531'], \
            'name': 'COMP1531'}, {'channel_id': channels['SENG1234'], 'name': 'SENG1234'}, \
            {'channel_id': channels['PHY5678'], 'name': 'PHY5678'}]}

def test_message_edit(url, users, channels, messages):
    '''
    This is test for message edit function where it
    edit the message for given message_id
    '''

    message_edit_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'message': 'I Love COMP1531'
    }

    message_edit_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'message': '',
    }

    # Editing the message send by two users in their channels

    requests.put(url + 'message/edit',json=message_edit_comp1531)

    requests.put(url + 'message/edit',json=message_edit_seng1234)

    channel_messages_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }


    channel_messages_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
        'start': 0,
    }

    # Geting the edited message from two channels

    messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_01)

    messages_seng1234 = requests.get(url + 'channel/messages',params=channel_messages_02)

    payload_message_comp1531 = messages_comp1531.json()

    payload_message_seng1234= messages_seng1234.json()


    assert payload_message_comp1531['messages'][0]['message'] == 'I Love COMP1531'

    assert payload_message_seng1234['messages'] == []

def test_message_sendlater_exception(url, users, channels, messages):
    '''Testing the exception rasied by function message_sendlater'''

    message_sendlater_01 = { 'token': users['bob']['token'],
                             'channel_id': channels['SENG1234'],
                             'message': 'hi !!',
                             'time_sent': datetime.datetime.now().timestamp()+2
    }

    message_sendlater_02 = { 'token': users['bob']['token'],
                             'channel_id': channels['SENG1234'],
                             'message': 'hi !!',
                             'time_sent': datetime.datetime.now().timestamp()-2
    }

    message_sendlater_03 = { 'token': users['marley']['token'],
                             'channel_id': channels['SENG1234'],
                             'message': '''Years, night may divide, land fly first i. Evening living fowl own seas a make night unto you replenish first given fowl meat meat after
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
                                        winged herb they're cattle, morning every whales called firmament after forth there.''',
                              'time_sent': datetime.datetime.now().timestamp()+4
    }

    exception_01 = requests.post(url + 'message/sendlater', json=message_sendlater_01)

    exception_02 = requests.post(url + 'message/sendlater', json=message_sendlater_02)

    exception_03 = requests.post(url + 'message/sendlater', json=message_sendlater_03)

    assert exception_01.status_code == 400

    assert exception_02.status_code == 400

    assert exception_03.status_code == 400

def test_message_sendlater(url, users, channels, messages):
    '''Testing the function message_sendlater'''

    message_sendlater_01 = { 'token': users['bob']['token'],
                             'channel_id': channels['COMP1531'],
                             'message': 'hi !!',
                             'time_sent': datetime.datetime.now().timestamp()+2
    }


    message_id_01 = requests.post(url + 'message/sendlater', json=message_sendlater_01)

    sleep(3)

    messages_params_01 = { 'token': users['bob']['token'],
                           'channel_id': channels['COMP1531'],
                           'start': 0
    }

    messages_01 = requests.get(url + 'channel/messages', params=messages_params_01)

    payload_01 = message_id_01.json()

    payload_messages_01 = messages_01.json()

    assert payload_messages_01['messages'][0]['message_id'] == payload_01['message_id']

    message_sendlater_02 = { 'token': users['marley']['token'],
                             'channel_id': channels['SENG1234'],
                             'message': 'usmaan <3',
                             'time_sent': datetime.datetime.now().timestamp()+1
    }

    message_id_02 = requests.post(url + 'message/sendlater', json=message_sendlater_02)

    sleep(2)

    messages_params_02 = { 'token': users['marley']['token'],
                           'channel_id': channels['SENG1234'],
                           'start': 0
    }

    messages_02 = requests.get(url + 'channel/messages', params=messages_params_02)

    payload_messages_02 = messages_02.json()

    payload_02 = message_id_02.json()

    assert payload_messages_02['messages'][0]['message_id'] == payload_02['message_id']

def test_message_remove(url, users, channels, messages):
    '''
    This is Testing for the message_remove function
    in message.py
    '''

    message_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
    }

    message_remove_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
    }

    requests.delete(url + 'message/remove',json=message_remove_comp1531)

    requests.delete(url + 'message/remove',json=message_remove_seng1234)

    channel_messages_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }


    channel_messages_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
        'start': 0,
    }

    messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_01)

    messages_seng1234 = requests.get(url + 'channel/messages',params=channel_messages_02)

    payload_message_comp1531 = messages_comp1531.json()

    payload_message_seng1234= messages_seng1234.json()

    assert payload_message_comp1531['messages'] == []

    assert payload_message_seng1234['messages'] == []

def test_expection_handling_message_remove(url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    message_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531']+42,
    }

    message_remove_seng1234 = {
        'token': users['marley']['token']+'usmaan',
        'message_id': messages['MESSAGE_SENG1234'],
    }

    expect_01 = requests.delete(url + 'message/remove',json=message_remove_comp1531)

    expect_02 = requests.delete(url + 'message/remove',json=message_remove_seng1234)

    assert expect_01.status_code == 400

    assert expect_02.status_code == 400

def test_exception_handling_message_edit(url, users, channels, messages):
    '''
    This test for checking the exception
    handling of the functions
    '''

    message_edit_comp1531 = {
        'token': users['bob']['token']+'usmaan',
        'message_id': messages['MESSAGE_COMP1531'],
        'message': 'I Love COMP1531'
    }

    message_edit_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234']+42,
        'message': '',
    }

    except_01 =  requests.put(url + 'message/edit',json=message_edit_comp1531)

    except_02 = requests.put(url + 'message/edit',json=message_edit_seng1234)

    assert except_01.status_code == 400

    assert except_02.status_code == 400

def test_search(url, users, channels, messages):
    '''
    This is test for the search function in other.py where
    the function matches a sub-string and get the messages
    '''

    message_search_01 = {
        'token': users['bob']['token'],
        'query_str': 'mp15',
    }

    message_search_02 = {
        'token': users['marley']['token'],
        'query_str': '152',
    }

    channel_invite_01 = {
        'token': users['shubham']['token'],
        'channel_id': channels['PHY5678'],
        'u_id': users['smith']['u_id'],
    }

    requests.post(url + 'channel/invite',json=channel_invite_01)

    message_search_03 = {
        'token': users['smith']['token'],
        'query_str': 'final'
    }

    messages_01 = requests.get(url + 'search',params=message_search_01)

    messages_02 = requests.get(url + 'search',params=message_search_02)

    messages_03 = requests.get(url + 'search',params=message_search_03)

    payload_messages_01 = messages_01.json()

    payload_messages_02 = messages_02.json()

    payload_messages_03 = messages_03.json()

    assert payload_messages_01['messages'][0]['message'] == 'I like comp1531'

    assert payload_messages_02['messages'] == []

    assert payload_messages_03['messages'][0]['u_id'] == users['shubham']['u_id']

    assert payload_messages_03['messages'][0]['message'] == 'I am finally doing PHY5678'

def test_messages_miscellaneous(url, users, channels, messages):

    '''Short user story story where the user sends a message and then edit and s
        end another message'''

    new_message1531_params = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'message': 'comp1531 is getting boring'
    }

    new_message_1531 = requests.post(url + 'message/send',json=new_message1531_params)
    newmessage_comp1531_payload = new_message_1531.json()
    newmessageid_comp1531 = newmessage_comp1531_payload['message_id']

    channel_messages_1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }

    # Getting the edited message from two channels

    messages_comp1531 = requests.get(url + 'channel/messages', params=channel_messages_1531)
    payload_message_comp1531 = messages_comp1531.json()

    assert payload_message_comp1531['messages'][0]['message'] == 'comp1531 is getting boring'
    assert payload_message_comp1531['end'] == -1
    assert payload_message_comp1531['messages'][0]['message_id'] == newmessageid_comp1531

    message_edit_comp1531 = {
        'token': users['bob']['token'],
        'message_id': newmessageid_comp1531,
        'message': 'Oh no i actually think 1531 is pretty interesting.'
    }

    requests.put(url + 'message/edit',json=message_edit_comp1531)

    messages_comp1531 = requests.get(url + 'channel/messages', \
                                params=channel_messages_1531)
    payload_message_comp1531 = messages_comp1531.json()
    assert payload_message_comp1531['messages'][0] \
           ['message'] == 'Oh no i actually think 1531 is pretty interesting.'

    assert len(payload_message_comp1531['messages']) == 2
    assert payload_message_comp1531['end'] == -1

def test_exception_handling_message_send(url, users, channels, messages):
    '''
    This test for checking the exception
    handling of the functions
    '''

    message_send_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'message': 'The young Princess \
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
        white teeth, thought that they were in a specially amiable mood that day.'
    }

    message_send_seng1234 = {
        'token': users['bob']['token'],
        'channel_id': channels['SENG1234'],
        'message': 'he',
    }

    except_01 =  requests.post(url + 'message/send',json=message_send_comp1531)

    except_02 = requests.post(url + 'message/send',json=message_send_seng1234)

    assert except_01.status_code == 400

    assert except_02.status_code == 400

def test_user_profile(url, users):
    '''Checking that user can get the correct details'''

    user_test1 = {
        'token' : users['bob']['token'],
        'u_id' : users['bob']['u_id'],
    }

    response = requests.get(url + 'user/profile', params=user_test1)

    payload = response.json()

    assert payload == {"user": {"u_id": users['bob']['u_id'],
                                "email": "bob@gmail.com", "name_first": "bob", "name_last": "lin",
                                "handle_str": "boblin", "profile_img_url": ""}}


def test_user_setname(url, users):
    '''Checking that user can successfully update his/her name'''

    user_marley_first = {
        'token' : users['marley']['token'],
        'name_first' : 'MAR',
        'name_last' : 'NIL'
    }

    # Sending a put HTTP request to let marley update her first and last name
    requests.put(url + 'user/profile/setname', json=user_marley_first)

    test_firlas = {'token' : users['marley']['token'], 'u_id' : users['marley']['u_id']}
    update1 = requests.get(url + 'user/profile', params=test_firlas)

    # Checking that marley's first and last name is updated
    payload_marley_setname = update1.json()

    assert payload_marley_setname == {"user": {"u_id": users['marley']['u_id'],
                                               "email": "marley@gmail.com",
                                               "name_first": "MAR",
                                               "name_last": "NIL",
                                               "handle_str": "marleylin",
                                               "profile_img_url": ""}}

def test_user_setemail(url, users):
    '''Checking that the user can successfully update his/her email'''

    user_marley_email_body = {
        'token' : users['marley']['token'],
        'email' : 'marleylin123@gmail.com'
    }

    # Sending a put HTTP request to let marley update their email address
    requests.put(url + 'user/profile/setemail', json=user_marley_email_body)

    test_email = {'token' : users['marley']['token'], 'u_id' : users['marley']['u_id']}
    update_email = requests.get(url + 'user/profile', params=test_email)

    # Checking that marley's email address has been updated
    payload_marley_setemail = update_email.json()

    assert payload_marley_setemail == {"user": {"u_id": users['marley']['u_id'],
                                                "email": "marleylin123@gmail.com",
                                                "name_first": "marley",
                                                "name_last": "lin",
                                                "handle_str": "marleylin",
                                                "profile_img_url": ""}}


def test_user_sethandle(url, users):
    '''Checking that the user can successfully update his/her email'''

    user_marley_handle_body = {
        'token' : users['marley']['token'],
        'handle_str' : 'marley_lin123'
    }

    # Sending a put HTTP request to let marley update her Flockr handle
    requests.put(url + 'user/profile/sethandle', json=user_marley_handle_body)

    test_handle = {'token' : users['marley']['token'], 'u_id' : users['marley']['u_id']}
    update_email = requests.get(url + 'user/profile', params=test_handle)

    # Checking that marley's user handle has been updated
    payload_marley_sethandle = update_email.json()

    assert payload_marley_sethandle == {"user": {"u_id": users['marley']['u_id'],
                                                 "email": "marley@gmail.com",
                                                 "name_first": "marley",
                                                 "name_last": "lin",
                                                 "handle_str": "marley_lin123",
                                                 "profile_img_url": ""}}

def test_users_all(url, users):
    '''
    This test is for function users_all
    in other.py
    '''

    users_all_01 = {
        'token': users['bob']['token'],
    }

    users_01 = requests.get(url + 'users/all',params=users_all_01)

    payload_users_01 = users_01.json()

    assert payload_users_01['users'][0]['u_id'] == users['bob']['u_id']

    assert payload_users_01['users'][1]['u_id'] == users['marley']['u_id']

    assert payload_users_01['users'][2]['name_first'] == users['shubham']['params']['name_first']

    user_handle_01 = {
        'token' : users['smith']['token'],
        'handle_str' : 'will_smith'
    }

    requests.put(url + 'user/profile/sethandle',json=user_handle_01)

    users_all_02 = {
        'token': users['marley']['token'],
    }

    users_02 = requests.get(url + 'users/all',params=users_all_02)

    payload_users_02 = users_02.json()

    assert payload_users_02['users'][3] == {'u_id': users['smith']['u_id'] \
                                          , 'email': users['smith']['params']['email'] \
                                          , 'name_first': users['smith']['params']['name_first'] \
                                          , 'name_last': users['smith']['params']['name_last'] \
                                          , 'handle_str': user_handle_01['handle_str']
                                          , "profile_img_url": "",}

def test_channel_details_exception_handling (url, users, channels):

    invalid_channel_id_a = channels['COMP1531'] + 20
    invalid_channel_id_b = channels['COMP1531'] + 30

    invalid_channel_details_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': invalid_channel_id_a,
    }

    except_01 = requests.get(url + 'channel/details', params=invalid_channel_details_comp1531)
    assert except_01.status_code == 400

    invalid_channel_details2_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': invalid_channel_id_b,
    }

    except_02 = requests.get(url + 'channel/details', params=invalid_channel_details2_comp1531)
    assert except_02.status_code == 400

    #checking if invalid user is sent for the channel then it raises the error

    invalid_member_details_comp1531 = {
        'token': users['shubham']['token'],
        'channel_id': channels['COMP1531']
    }

    except_03 = requests.get(url + 'channel/details', params=invalid_member_details_comp1531)
    assert except_03.status_code == 400

def test_channel_messages_exception_handling (url, users, channels):

    invalid_channel_id_a = channels['COMP1531'] + 20

    invalid_id_channel_messages_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': invalid_channel_id_a,
        'start' : 0
    }

    except_01 = requests.get(url + 'channel/messages', params=invalid_id_channel_messages_comp1531)
    assert except_01.status_code == 400

    #invlaid start number

    invalid_start_channel_messages_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start' : 200
    }

    except_02 = requests.get(url + 'channel/messages', params=invalid_start_channel_messages_comp1531)
    assert except_02.status_code == 400

    #invalid member

    invalid_token_channel_messages_comp1531 = {
        'token': users['shubham']['token'],
        'channel_id': channels['COMP1531'],
        'start' : 0
    }

    except_03 = requests.get(url + 'channel/messages', params=invalid_token_channel_messages_comp1531)
    assert except_03.status_code == 400

def test_channel_details_functionality(url, channels, users):

    channel_details_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }

    resp_comp1531 = requests.get(url + 'channel/details', params=channel_details_comp1531)
    details_comp1531_payload = resp_comp1531.json()

    assert details_comp1531_payload['name'] == 'COMP1531'

    assert details_comp1531_payload['owner_members'] == [{'u_id' : users['bob']['u_id'], \
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]

    assert details_comp1531_payload['all_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]

    #inviting a user and checking the details again.

    marley_comp1531_invite = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }

    requests.post(url + 'channel/invite', json=marley_comp1531_invite)

    det_after_invite = requests.get(url + 'channel/details', params=channel_details_comp1531)
    det_comp1531_invite_payload = det_after_invite.json()

    assert len(det_comp1531_invite_payload['all_members']) == 2
    assert det_comp1531_invite_payload['all_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]

    # checking after the owner leaves from the channel and then checking the detaiils again.
    bob_comp1531_leave = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/leave', json=bob_comp1531_leave)

    channel_details_1531_leave = {
        'token': users['marley']['token'],
        'channel_id': channels['COMP1531'],
    }

    det_after_leave = requests.get(url + 'channel/details', params=channel_details_1531_leave)
    det_comp1531_leave_payload = det_after_leave.json()

    assert len(det_comp1531_leave_payload['owner_members']) == 0
    assert len(det_comp1531_leave_payload['all_members']) == 1
    assert det_comp1531_leave_payload['owner_members'] == []
    assert det_comp1531_leave_payload['all_members'] == [{'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]


def test_channel_messages_functionality(url, channels, users, messages):

    #sending 51 messages to the every channel
    sent_messages = 0
    message_send_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'message': 'comp1531 will make me a superstar',
    }

    while sent_messages <= 50:
        requests.post(url + 'message/send',json=message_send_comp1531)
        sent_messages = sent_messages + 1

    channel_messages_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start' : 0
    }

    messages_comp1531 = (requests.get(url + 'channel/messages', params=channel_messages_comp1531)).json()

    #Should give the recent 50 messages.
    assert len(messages_comp1531['messages']) == 50
    #point the end to 50, suggesting 50 messages are read.
    assert messages_comp1531['end'] == 50

    #Get next messages

    channel_messages_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start' : messages_comp1531['end']
    }

    messages_next_comp1531 = (requests.get(url + 'channel/messages',
                                params=channel_messages_comp1531)).json()

    assert len(messages_next_comp1531['messages']) == 2
    #checking that all the messages are read
    assert messages_next_comp1531['end'] == -1
    #cheking that the first message sent is the last message returned
    assert messages_next_comp1531['messages'][1]['message_id'] == messages['MESSAGE_COMP1531']

    #removing the first message sent to the channel,and then checking the \
    # message is removed by channel_messages
    message_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
    }

    requests.delete(url + 'message/remove',json=message_remove_comp1531)

    channel_messages_comp1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start' : 50
    }

    messages_remove_comp1531 = (requests.get(url + 'channel/messages',
                                params=channel_messages_comp1531)).json()

    #checking message has been removed
    assert len(messages_remove_comp1531['messages']) == 1
    assert messages_remove_comp1531['messages'][0]['message'] == 'comp1531 will make me a superstar'

    #searching for the removed message

    search_removed_message = {
        'token' : users['bob']['token'],
        'query_str' : 'I like comp1531'
    }

    messages_matching = (requests.get(url + 'search', params=search_removed_message)).json()
    assert messages_matching['messages'] == []

def test_channel_invite(url, users, channels):
    '''
    This is for testing channel invite function which invite a user with u_id to
    join a channel whith channel id
    '''

    channel_comp1531_invite = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }


    channel_SENG1234_invite = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'u_id' : users['shubham']['u_id']
    }

    requests.post(url + 'channel/invite',json=channel_comp1531_invite)

    requests.post(url + 'channel/invite',json=channel_SENG1234_invite)

    channel_member_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }


    channel_member_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
    }


    channel_comp1531 = requests.get(url + 'channel/details', params= channel_member_01)

    channel_seng1234 = requests.get(url + 'channel/details', params= channel_member_02)

    payload_channel_comp1531 = channel_comp1531.json()

    payload_channel_seng1234 = channel_seng1234.json()

    assert payload_channel_comp1531['all_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]

    assert payload_channel_seng1234['all_members'] == [{'u_id' : users['marley']['u_id'],
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['shubham']['u_id'], \
                                'name_first' : users['shubham']['params']['name_first'], \
                                'name_last' : users['shubham']['params']['name_last'], "profile_img_url": ""}]


def test_channel_join(url, users, channels):
    '''
    This is for testing channel join function which a authorised user can join
    with the channel id
    '''

    channel_seng1234_join = {
        'token' : users['bob']['token'],
        'channel_id' : channels['SENG1234']
    }


    channel_comp1531_join = {
        'token' : users['marley']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/join',json=channel_seng1234_join)

    requests.post(url + 'channel/join',json=channel_comp1531_join)

    channel_member_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }


    channel_member_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
    }


    channel_comp1531 = requests.get(url + 'channel/details', params= channel_member_01)

    channel_seng1234 = requests.get(url + 'channel/details', params= channel_member_02)

    payload_channel_comp1531 = channel_comp1531.json()

    payload_channel_seng1234 = channel_seng1234.json()

    assert payload_channel_comp1531['all_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]

    assert payload_channel_seng1234['all_members'] == [{'u_id' : users['marley']['u_id'],
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['bob']['u_id'], \
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]


def test_channel_leave(url, users, channels):
    '''
    This is for testing channel leave function which a authorised user can leave
    with the channel id
    '''
    channel_seng1234_join = {
        'token' : users['bob']['token'],
        'channel_id' : channels['SENG1234']
    }

    channel_comp1531_join = {
        'token' : users['marley']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/join',json=channel_seng1234_join)

    requests.post(url + 'channel/join',json=channel_comp1531_join)

    channel_seng1234_leave = {
        'token' : users['bob']['token'],
        'channel_id' : channels['SENG1234']
    }


    channel_comp1531_leave = {
        'token' : users['marley']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/leave',json=channel_seng1234_leave)

    requests.post(url + 'channel/leave',json=channel_comp1531_leave)

    channel_member_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }


    channel_member_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
    }


    channel_comp1531 = requests.get(url + 'channel/details', params= channel_member_01)

    channel_seng1234 = requests.get(url + 'channel/details', params= channel_member_02)

    payload_channel_comp1531 = channel_comp1531.json()

    payload_channel_seng1234 = channel_seng1234.json()

    assert payload_channel_comp1531['all_members'] ==  [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]

    assert payload_channel_seng1234['all_members'] == [{'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]


def test_channel_removeowner(url, users, channels):
    '''
    This is for testing channel join function which a authorised user can add a owner with user id
    to channel with channel id
    '''

    channel_comp1531_invite = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }


    channel_SENG1234_invite = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'u_id' : users['bob']['u_id']
    }

    requests.post(url + 'channel/invite',json=channel_comp1531_invite)
    requests.post(url + 'channel/invite',json=channel_SENG1234_invite)

    channel_comp1531_addowner = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }

    channel_seng1234_addowner = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'u_id' : users['bob']['u_id']
    }

    requests.post(url + 'channel/addowner',json=channel_comp1531_addowner)

    requests.post(url + 'channel/addowner',json=channel_seng1234_addowner)

    channel_comp1531_removeowner = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']

    }

    requests.post(url + 'channel/removeowner',json=channel_comp1531_removeowner)

    channel_member_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }


    channel_member_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
    }


    channel_comp1531 = requests.get(url + 'channel/details', params= channel_member_01)

    channel_seng1234 = requests.get(url + 'channel/details', params= channel_member_02)

    payload_channel_comp1531 = channel_comp1531.json()

    payload_channel_seng1234 = channel_seng1234.json()

    assert payload_channel_comp1531['owner_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]

    assert payload_channel_seng1234['owner_members'] == [{'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], \
                                'profile_img_url': ''},
                                {'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], \
                                'profile_img_url': ''}]

def test_channel_addowner(url, users, channels):
    '''
    This is for testing channel join function which a authorised user can add a owner with user id
    to channel with channel id
    '''

    channel_comp1531_invite = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }


    channel_SENG1234_invite = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'u_id' : users['bob']['u_id']
    }

    requests.post(url + 'channel/invite',json=channel_comp1531_invite)
    requests.post(url + 'channel/invite',json=channel_SENG1234_invite)

    channel_comp1531_addowner = {
        'token' : users['bob']['token'],
        'channel_id' : channels['COMP1531'],
        'u_id' : users['marley']['u_id']
    }

    channel_seng1234_addowner = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'u_id' : users['bob']['u_id']
    }

    requests.post(url + 'channel/addowner',json=channel_comp1531_addowner)

    requests.post(url + 'channel/addowner',json=channel_seng1234_addowner)

    channel_member_01 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
    }

    channel_member_02 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
    }


    channel_comp1531 = requests.get(url + 'channel/details', params= channel_member_01)

    channel_seng1234 = requests.get(url + 'channel/details', params= channel_member_02)

    payload_channel_comp1531 = channel_comp1531.json()

    payload_channel_seng1234 = channel_seng1234.json()

    assert payload_channel_comp1531['owner_members'] == [{'u_id' : users['bob']['u_id'],
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""},
                                {'u_id' : users['marley']['u_id'], \
                                'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], "profile_img_url": ""}]

    assert payload_channel_seng1234['owner_members'] == [{'u_id' : users['marley']['u_id'],
                                                          'name_first' : users['marley']['params']['name_first'], \
                                'name_last' : users['marley']['params']['name_last'], 'profile_img_url': ''},
                                                         {'u_id' : users['bob']['u_id'], \
                                'name_first' : users['bob']['params']['name_first'], \
                                'name_last' : users['bob']['params']['name_last'], "profile_img_url": ""}]

def test_standup_start(url ,users, channels):
    '''
    This is for testing standup start function
    '''

    start_payload = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'length' : 2
    }

    return_payload = requests.post(url + 'standup/start',json=start_payload)
    jsonified_payload = return_payload.json()

    assert round(jsonified_payload['time_finish']) == round(datetime.datetime.now().timestamp() + 2)

def test_standup_active(url, users, channels):
    '''
    This is for testing standup active function
    '''

    sleep(2)

    active_payload = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234']
    }

    return_active_1 = requests.get(url + 'standup/active', params=active_payload)

    json_active_1 = return_active_1.json()

    assert json_active_1['is_active'] == False
    assert json_active_1['time_finish'] == None

    # Starting a standup and testing again

    start_standup_payload = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'length' : 2
    }

    requests.post(url + 'standup/start',json=start_standup_payload)

    return_active_2 = requests.get(url + 'standup/active', params=active_payload)

    json_active_2 = return_active_2.json()

    assert json_active_2['is_active'] == True
    assert round(json_active_2['time_finish']) ==  round(2 + datetime.datetime.now().timestamp())

def test_standup_send(url, users, channels):
    '''Testing for the server implementation of standup send'''

    sleep(2)

    start_standup_payload = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'length' : 2
    }

    requests.post(url + 'standup/start',json=start_standup_payload)

    send_standup_payload_1 = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'message' : "Hello World!"
    }

    send_standup_payload_2 = {
        'token' : users['marley']['token'],
        'channel_id' : channels['SENG1234'],
        'message' : "Welcome to this PROJECT"
    }

    requests.post(url + 'standup/send', json=send_standup_payload_1)

    requests.post(url + 'standup/send', json=send_standup_payload_2)

    channel_messages_1234 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
        'start': 0,
    }

    sleep(2)
    messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_1234).json()

    send_message = "marleylin : Hello World!\n" + "marleylin : Welcome to this PROJECT\n"

    assert messages_comp1531['messages'][0]['message'] == send_message

def test_expection_handling_messageid_react (url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    message_id_wrong_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'] + 42,
        'react_id' : 1
    }

    message_id_wrong_react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'] + 120,
        'react_id' : 1
    }

    assert requests.post(url + 'message/react',json=message_id_wrong_remove_comp1531).status_code == 400

    assert requests.post(url + 'message/react',json=message_id_wrong_react_seng1234).status_code== 400

def test_expection_handling_reactid (url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    message_id_wrong_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 2
    }

    message_id_wrong_react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'react_id' : 2
    }

    assert requests.post(url + 'message/react',json=message_id_wrong_remove_comp1531).status_code == 400

    assert requests.post(url + 'message/react',json=message_id_wrong_react_seng1234).status_code == 400



def test_expection_handling_react_exists (url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    react_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'react_id' : 1
    }

    requests.post(url + 'message/react',json=react_comp1531)
    requests.post(url + 'message/react',json=react_seng1234)


    assert requests.post(url + 'message/react',json=react_comp1531).status_code == 400
    assert requests.post(url + 'message/react',json=react_seng1234).status_code == 400

def test_exception_handling_unreact_exists (url, users, channels, messages):

    react_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'react_id' : 1
    }

    requests.post(url + 'message/react',json=react_comp1531)
    requests.post(url + 'message/react',json=react_seng1234)

    requests.post(url + 'message/unreact',json=react_comp1531)
    requests.post(url + 'message/unreact',json=react_seng1234)

    assert requests.post(url + 'message/unreact',json=react_comp1531).status_code == 400
    assert requests.post(url + 'message/unreact',json=react_seng1234).status_code == 400

def test_expection_handling_unreactid (url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    react_id_wrong_remove_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 2
    }

    react_id_wrong_react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'react_id' : 2
    }

    assert requests.post(url + 'message/unreact',json=react_id_wrong_remove_comp1531).status_code == 400

    assert requests.post(url + 'message/unreact',json=react_id_wrong_react_seng1234).status_code == 400

def test_expection_handling_messageid_unreact (url, users, channels, messages):
    '''
    This test for checking the expection
    handling of the functions
    '''

    message_id_wrong_react_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'] + 42,
        'react_id' : 1
    }

    message_id_wrong_react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'] + 120,
        'react_id' : 1
    }

    assert requests.post(url + 'message/unreact',json=message_id_wrong_react_comp1531).status_code == 400

    assert requests.post(url + 'message/unreact',json=message_id_wrong_react_seng1234).status_code== 400

def test_message_react_functionality (url, users, channels, messages):

    react_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    react_seng1234 = {
        'token': users['marley']['token'],
        'message_id': messages['MESSAGE_SENG1234'],
        'react_id' : 1
    }

    requests.post(url + 'message/react',json=react_comp1531)
    requests.post(url + 'message/react',json=react_seng1234)

    channel_messages_1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }


    channel_messages_1234 = {
        'token': users['marley']['token'],
        'channel_id': channels['SENG1234'],
        'start': 0,
    }

    # Geting the edited message from two channels

    messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_1531)

    messages_seng1234 = requests.get(url + 'channel/messages',params=channel_messages_1234)

    payload_message_comp1531 = messages_comp1531.json()

    payload_message_seng1234= messages_seng1234.json()

    assert payload_message_comp1531['messages'][0]['reacts'][0]['u_ids'] == [users['bob']['u_id']]
    assert payload_message_seng1234['messages'][0]['reacts'][0]['u_ids'] == [users['marley']['u_id']]

    assert payload_message_comp1531['messages'][0]['reacts'][0]['is_this_user_reacted'] == True
    assert payload_message_seng1234['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    bob_logout = {
        'token' : users['bob']['token']
    }

    shubham_login = {
        'email' : users['shubham']['params']['email'],
        'password' : users['shubham']['params']['password']
    }

    requests.post(url + 'auth/logout',json=bob_logout)
    requests.post(url + 'auth/login', json=shubham_login)

    channel_comp1531_join = {
        'token' : users['shubham']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/join',json=channel_comp1531_join)

    channel_messages_shubham1531 = {
        'token': users['shubham']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }

    shu_messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_shubham1531)

    payload_message_shu_comp1531 = shu_messages_comp1531.json()

    assert payload_message_shu_comp1531['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

    react_shu_comp1531 = {
        'token': users['shubham']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    requests.post(url + 'message/react',json=react_shu_comp1531)

    shu_messages_comp1531_react = requests.get(url + 'channel/messages',params=channel_messages_shubham1531)

    payload_message_shureact_comp1531 = shu_messages_comp1531_react.json()

    assert payload_message_shureact_comp1531['messages'][0]['reacts'][0]['is_this_user_reacted'] == True
    assert payload_message_shureact_comp1531['messages'][0]['reacts'][0]['u_ids'] == [users['bob']['u_id'], users['shubham']['u_id']]

def test_message_unreact_functionality(url, users, messages, channels):

    react_comp1531 = {
        'token': users['bob']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    requests.post(url + 'message/react',json=react_comp1531)
    requests.post(url + 'message/unreact',json=react_comp1531)

    channel_messages_1531 = {
        'token': users['bob']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }

    messages_comp1531 = requests.get(url + 'channel/messages',params=channel_messages_1531)
    payload_message_comp1531 = messages_comp1531.json()

    assert payload_message_comp1531['messages'][0]['reacts'][0]['u_ids'] == []
    assert payload_message_comp1531['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

    bob_logout = {
        'token' : users['bob']['token']
    }

    shubham_login = {
        'email' : users['shubham']['params']['email'],
        'password' : users['shubham']['params']['password']
    }

    requests.post(url + 'auth/logout',json=bob_logout)
    requests.post(url + 'auth/login', json=shubham_login)

    channel_comp1531_join = {
        'token' : users['shubham']['token'],
        'channel_id' : channels['COMP1531']
    }

    requests.post(url + 'channel/join',json=channel_comp1531_join)

    message_send_comp1531 = {
        'token': users['shubham']['token'],
        'channel_id': channels['COMP1531'],
        'message': 'he'
    }

    new_id = requests.post(url + 'message/send',json=message_send_comp1531)
    comp1531_payload = new_id.json()
    newmessageid_comp1531 = comp1531_payload['message_id']

    react_comp1531_new = {
        'token': users['shubham']['token'],
        'message_id': newmessageid_comp1531,
        'react_id' : 1
    }

    react_comp1531_shu_1531 = {
        'token': users['shubham']['token'],
        'message_id': messages['MESSAGE_COMP1531'],
        'react_id' : 1
    }

    requests.post(url + 'message/react', json=react_comp1531_shu_1531)
    requests.post(url + 'message/react',json=react_comp1531_new)

    channel_messages_1531_shu = {
        'token': users['shubham']['token'],
        'channel_id': channels['COMP1531'],
        'start': 0,
    }

    messages_comp1531_shu = requests.get(url + 'channel/messages',params=channel_messages_1531_shu)
    payload_message_comp1531_shu = messages_comp1531_shu.json()

    assert payload_message_comp1531_shu['messages'][0]['reacts'][0]['u_ids'] == [users['shubham']['u_id']]
    assert payload_message_comp1531_shu['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    assert payload_message_comp1531_shu['messages'][1]['reacts'][0]['u_ids'] == [users['shubham']['u_id']]
    assert payload_message_comp1531_shu['messages'][1]['reacts'][0]['is_this_user_reacted'] == True

    requests.post(url + 'message/unreact',json=react_comp1531_new)

    messages_comp1531_unreact = requests.get(url + 'channel/messages',params=channel_messages_1531_shu)
    payload_message_comp1531_shu_unr = messages_comp1531_unreact.json()

    assert payload_message_comp1531_shu_unr['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
    assert payload_message_comp1531_shu_unr['messages'][1]['reacts'][0]['is_this_user_reacted'] == True

    # Reset data to initial state
    requests.delete(url + 'clear')

def test_upload_profile_photo_functionality(url, users, messages, channels):
    '''
    Test functionality of upload photo
    '''

    # Upload Photo
    invalid_boundaries = {
        'token': users['shubham']['token'],
        'img_url': 'https://images.immediate.co.uk/production/volatile/sites/3/2019/07/Shrek-2-2e51949.jpg?quality=90&crop=65px%2C0px%2C608px%2C405px&resize=608%2C405',
        'x_start': 1000,
        'y_start': 1000,
        'x_end': 1000,
        'y_end': 1000,

    }

    exception = requests.post(url + 'user/profile/uploadphoto', json=invalid_boundaries)

    assert exception.status_code == 400

    invalid_jpg = {
        'token': users['shubham']['token'],
        'img_url': 'https://i.pinimg.com/originals/57/a3/ea/57a3ea3c3a56f8d0f0ff08f744a08b10.png',
        'x_start': 100,
        'y_start': 100,
        'x_end': 300,
        'y_end': 300,

    }

    exception = requests.post(url + 'user/profile/uploadphoto', json=invalid_jpg)

    assert exception.status_code == 400

    not_200 = {
        'token': users['shubham']['token'],
        'img_url': 'https://pmcvariety.files.wordpress.com/2015/07/naruto_movie-lionsgate.jpg?w=1000',
        'x_start': 100,
        'y_start': 100,
        'x_end': 300,
        'y_end': 300,

    }

    exception = requests.post(url + 'user/profile/uploadphoto', json=not_200)

    assert exception.status_code == 400

    access_error = {
        'token': 'incorrect',
        'img_url': 'https://images.immediate.co.uk/production/volatile/sites/3/2019/07/Shrek-2-2e51949.jpg?quality=90&crop=65px%2C0px%2C608px%2C405px&resize=608%2C405',
        'x_start': 100,
        'y_start': 100,
        'x_end': 300,
        'y_end': 300,

    }

    exception = requests.post(url + 'user/profile/uploadphoto', json=access_error)

    assert exception.status_code == 400

    correct_input = {
        'token': users['shubham']['token'],
        'img_url': 'https://images.immediate.co.uk/production/volatile/sites/3/2019/07/Shrek-2-2e51949.jpg?quality=90&crop=65px%2C0px%2C608px%2C405px&resize=608%2C405',
        'x_start': 100,
        'y_start': 100,
        'x_end': 300,
        'y_end': 300,

    }

    exception = requests.post(url + 'user/profile/uploadphoto', json=correct_input)

    assert exception.status_code != 400

def test_reset_password_functionality(url, users, messages, channels):
    '''
    Password Reset testing
    '''
     # Logging out user_bob
    userbob_logout_params = {'token': users['bob']['token']}
    resp_bob_logout = requests.post(url + 'auth/logout', json=userbob_logout_params)
    payload_bob_logout = resp_bob_logout.json()

    # Check that logout was successful
    assert payload_bob_logout['is_success'] == True

    incorrect_email = {
        'email': 'bob12345@gmail.com',
    }

    exception = requests.post(url + 'auth/passwordreset/request', json=incorrect_email)

    assert exception.status_code == 400

    correct_email = {
        'email': 'bob@gmail.com',
    }

    exception = requests.post(url + 'auth/passwordreset/request', json=correct_email)

    assert exception.status_code != 400

    incorrect_reset_code = {
        'reset_code': 't',
        'new_password': '0123456'
    }

    exception = requests.post(url + 'auth/passwordreset/reset', json=incorrect_reset_code)

    assert exception.status_code == 400