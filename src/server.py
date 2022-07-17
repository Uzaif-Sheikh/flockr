'''
H15C, Group 3
Server Implementation
'''

import sys
from json import dumps
from flask_cors import CORS
from error import InputError, AccessError
from data import pickle_data, unpickle_data
from flask import Flask, request, send_from_directory
from standup import standup_active, standup_send, standup_start
from channels import channels_create, channels_list, channels_listall
from other import admin_userpermission_change, users_all, clear, search
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
from user import user_profile, user_profile_setemail, user_profile_setname, user_profile_sethandle, user_profile_uploadphoto
from channel import channel_addowner, channel_details, channel_invite, channel_join, channel_leave, channel_messages, channel_removeowner
from message import message_send, message_remove, message_edit, message_pin, message_unpin, message_react, message_unreact, message_sendlater

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# ################################################################## #
#                         AUTH FUNCTIONS                             #
# ################################################################## #

@APP.route('/auth/login', methods=['POST'])
def server_auth_login():
    unpickle_data()
    data = request.get_json()
    ret = auth_login(data['email'], data['password'])
    pickle_data()

    return dumps(ret)

@APP.route('/auth/logout', methods=['POST'])
def server_auth_logout():
    unpickle_data()
    data = request.get_json()
    ret = auth_logout(data['token'])
    pickle_data()

    return dumps(ret)

@APP.route("/auth/register", methods=['POST'])
def server_auth_register():
    unpickle_data()
    data = request.get_json()
    ret = auth_register(data['email'], \
    data['password'], data['name_first'], data['name_last'])
    pickle_data()

    return dumps(ret)

# ################################################################## #
#                         CHANNELS FUNCTIONS                         #
# ################################################################## #

@APP.route('/channels/list', methods=['GET'])
def server_channels_list():
    """ list user channels """
    ret = channels_list(request.args.get('token'))

    return dumps(ret)

@APP.route('/channels/listall', methods=['GET'])
def server_channels_listall():
    """ list all channels """
    ret = channels_listall(request.args.get('token'))

    return dumps(ret)

@APP.route('/channels/create', methods=['POST'])
def server_channels_create():
    """ create channel """
    unpickle_data()
    data = request.get_json()
    ret = channels_create(data['token'],
                          data['name'], data['is_public'])
    pickle_data()

    return dumps(ret)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def server_auth_passwordreset_request():
    '''send a secret code to a email'''
    unpickle_data()
    data = request.get_json()
    auth_passwordreset_request(data['email'])
    pickle_data()

    return dumps({})

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def server_auth_passwordreset_reset():
    '''send a secret code to a email'''
    unpickle_data()
    data = request.get_json()
    auth_passwordreset_reset(data['reset_code'], data['new_password'])
    pickle_data()

    return dumps({})
# ################################################################## #
#                         CHANNEL FUNCTIONS                          #
# ################################################################## #

@APP.route('/channel/invite', methods=['POST'])
def server_channel_invite():
    """ invite user to channel """
    unpickle_data()
    data = request.get_json()
    channel_invite(data['token'], data['channel_id'], data['u_id'])
    pickle_data()

    return dumps({})

@APP.route('/channel/details', methods=['GET'])
def server_channel_details():
    """ get channel details """

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    details = channel_details(token, channel_id)
    return dumps(details)

@APP.route('/channel/messages', methods=['GET'])
def server_channel_messages():
    """ get channel messages """

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    messages = channel_messages(token, channel_id, start)
    return dumps(messages)

@APP.route('/channel/leave', methods=['POST'])
def server_channel_leave():
    """ leave channel """
    unpickle_data()
    data = request.get_json()
    channel_leave(data['token'], data['channel_id'])
    pickle_data()

    return dumps({})

@APP.route('/channel/join', methods=['POST'])
def server_channel_join():
    """ join channel """
    unpickle_data()
    data = request.get_json()
    channel_join(data['token'], data['channel_id'])
    pickle_data()

    return dumps({})

@APP.route('/channel/addowner', methods=['POST'])
def server_channel_addowner():
    """ add owner """
    unpickle_data()
    data = request.get_json()
    channel_addowner(data['token'], data['channel_id'], data['u_id'])
    pickle_data()

    return dumps({})

@APP.route('/channel/removeowner', methods=['POST'])
def server_channel_removeowner():
    """ remove owner """
    unpickle_data()
    data = request.get_json()
    channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    pickle_data()

    return dumps({})

# ################################################################## #
#                         MESSAGE FUNCTIONS                          #
# ################################################################## #

@APP.route('/message/send', methods=['POST'])
def server_message_send():
    """ send message """

    unpickle_data()
    data = request.get_json()
    message_id = message_send(data['token'], data['channel_id'], data['message'])
    pickle_data()

    return dumps(message_id)

@APP.route('/message/remove', methods=['DELETE'])
def server_message_remove():
    """ remove message """

    unpickle_data()
    data = request.get_json()
    message_remove(data['token'], data['message_id'])
    pickle_data()

    return dumps({})

@APP.route('/message/edit', methods=['PUT'])
def server_message_edit():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_edit(data['token'], data['message_id'], data['message'])
    pickle_data()

    return dumps({})

@APP.route('/message/sendlater', methods=['POST'])
def server_message_sendlater():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_id = message_sendlater(data['token'], data['channel_id'], data['message'], data['time_sent'])
    pickle_data()

    return dumps(message_id)

@APP.route('/message/react', methods=['POST'])
def server_message_react():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_react(data['token'], data['message_id'], data['react_id'])
    pickle_data()

    return dumps({})

@APP.route('/message/unreact', methods=['POST'])
def server_message_unreact():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_unreact(data['token'], data['message_id'], data['react_id'])
    pickle_data()

    return dumps({})

@APP.route('/message/pin', methods=['POST'])
def server_message_pin():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_pin(data['token'], data['message_id'])
    pickle_data()

    return dumps({})

@APP.route('/message/unpin', methods=['POST'])
def server_message_unpin():
    """ edit message """

    unpickle_data()
    data = request.get_json()
    message_unpin(data['token'], data['message_id'])
    pickle_data()

    return dumps({})

# ################################################################## #
#                      PERMISSION FUNCTIONS                          #
# ################################################################## #

@APP.route('/admin/userpermission/change', methods=['POST'])
def server_admin_up_change():
    """ admin rights change """

    unpickle_data()
    data = request.get_json()
    admin_userpermission_change(data['token'], data['u_id'], data['permission_id'])
    pickle_data()

    return dumps({})

# ################################################################## #
#                         SEARCH FUNCTIONS                           #
# ################################################################## #

@APP.route('/search', methods=['GET'])
def server_search():
    """ search """

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    needed_messages = search(token, query_str)

    return dumps(needed_messages)

# ################################################################## #
#                         USER FUNCTIONS                             #
# ################################################################## #

@APP.route('/user/profile', methods=['GET'])
def server_user_profile():
    """ user profile """

    user_res = user_profile(request.args.get('token'), request.args.get('u_id'))

    return dumps(user_res)

@APP.route('/user/profile/setname', methods=['PUT'])
def server_user_profile_setname():
    """ set user name """

    unpickle_data()
    data = request.get_json()

    user_profile_setname(data['token'], data['name_first'], data['name_last'])
    pickle_data()

    return dumps({})

@APP.route('/user/profile/setemail', methods=['PUT'])
def server_user_profile_setemail():
    """ set user email """

    unpickle_data()
    email_data = request.get_json()

    user_profile_setemail(email_data['token'], email_data['email'])
    pickle_data()

    return dumps({})

@APP.route('/user/profile/sethandle', methods=['PUT'])
def server_user_profile_sethandle():
    """ set user handle """

    unpickle_data()
    handle_data = request.get_json()

    user_profile_sethandle(handle_data['token'], handle_data['handle_str'])
    pickle_data()

    return dumps({})

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def server_user_profile_uploadphoto():
    """ admin rights change """

    unpickle_data()
    data = request.get_json()
    user_profile_uploadphoto(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end'])
    pickle_data()

    return dumps({})

@APP.route('/static/<path:path>')
def send_js(path):
    """send_js"""
    return send_from_directory(APP.static_url_path, path)

# ################################################################## #
#                       STANDUP FUNCTIONS                            #
# ################################################################## #

@APP.route('/standup/start', methods=['POST'])
def server_standup_start():
    '''starts the standup and then posts the final message'''

    unpickle_data()
    start_data = request.get_json()

    time = standup_start(start_data['token'], start_data['channel_id'], start_data['length'])
    pickle_data()

    return dumps(time)

@APP.route('/standup/active', methods=['GET'])
def server_standup_active():
    '''Returns whether a standup is currenly active'''

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    ret_active = standup_active(token, channel_id)

    return dumps(ret_active)

@APP.route('/standup/send', methods=['POST'])
def server_standup_send():
    '''Sends a message to the standup buffer'''

    unpickle_data()
    send_package = request.get_json()
    pickle_data()

    standup_send(send_package['token'], send_package['channel_id'], send_package['message'])

    return dumps({})

# ################################################################## #
#                         OTHER FUNCTIONS                            #
# ################################################################## #

@APP.route('/clear', methods=['DELETE'])
def server_clear():
    """ Restore data to initial state """
    unpickle_data()
    clear()
    pickle_data()

    return dumps({})

@APP.route('/users/all', methods=['GET'])
def server_users_all():
    """ get all users """

    token = request.args.get('token')

    users = users_all(token)

    return dumps(users)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
