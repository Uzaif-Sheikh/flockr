'''
H15C, Group 3
Authentication Token file
'''

import jwt

SECRET = "COMP1531"

def token_generate(u_id):
    '''Generate token'''
    global SECRET
    encoded = jwt.encode({"u_id":u_id}, SECRET, algorithm='HS256').decode('utf-8')
    return str(encoded)

def token_get_uid(token):
    '''Get token id'''
    global SECRET
    uid = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
    return uid["u_id"]
