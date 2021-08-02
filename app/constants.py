# HTTP routes
ROUTE_REGISTER = '/register'
ROUTE_LOGIN = '/token'
ROUTE_REFRESH = '/refresh'

# FastAPI operation ids
OP_ID_AUTHORIZE = 'authorize'
OP_ID_MAY_AUTHORIZE = 'may_authorize'

# HTTP status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500

# Environment variable / configuration names
KEY_USE_OPENAPI = 'USE_OPENAPI'
KEY_USE_POSTGRESQL_DIALECT = 'USE_POSTGRESQL_DIALECT'
KEY_JWT_SECRET = 'JWT_SECRET'
KEY_POSTGRESQL_USER = 'POSTGRESQL_USER'
KEY_POSTGRESQL_PASS = 'POSTGRESQL_PASS'
KEY_POSTGRESQL_HOST = 'POSTGRESQL_HOST'
KEY_POSTGRESQL_PORT = 'POSTGRESQL_PORT'
KEY_POSTGRESQL_DB = 'POSTGRESQL_DB'