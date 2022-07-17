'''
H15 Orange, Group 3

Implementation of errors.py functions as specificed on the
assignment 1 spec.

Iteration 1
'''

from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'
