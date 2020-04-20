class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class LeaveAlreadyExistsError(Exception):
    pass

class UpdatingLeaveError(Exception):
    pass

class DeletingLeaveError(Exception):
    pass

class LeaveNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "LeaveAlreadyExistsError": {
         "message": "Leave with given name already exists",
         "status": 400
     },
     "UpdatingLeaveError": {
         "message": "Updating leave added by other is forbidden",
         "status": 403
     },
     "DeletingLeaveError": {
         "message": "Deleting leave added by other is forbidden",
         "status": 403
     },
     "LeaveNotExistsError": {
         "message": "Leave with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "EmailDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
     }
}