class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class IdAlreadyExistsError(Exception):
    pass

class UpdatingError(Exception):
    pass

class DeletingError(Exception):
    pass

class NotExistsError(Exception):
    pass

class UnauthorizedError(Exception):
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
     "IdAlreadyExistsError": {
         "message": "Movie with given name already exists",
         "status": 400
     },
     "UpdatingError": {
         "message": "Updating movie added by other is forbidden",
         "status": 403
     },
     "DeletingError": {
         "message": "Deleting movie added by other is forbidden",
         "status": 403
     },
     "NotExistsError": {
         "message": "Movie with given id doesn't exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     }
}