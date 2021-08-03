from constants import OP_ID_AUTHORIZE, OP_ID_MAY_AUTHORIZE
from fastapi.applications import FastAPI
from fastapi.openapi.utils import get_openapi

# Add authentication header for jwt to api documentation
def get_custom_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title, version=app.version, routes=app.routes)

        router_authorize = [route for route in app.routes[3:]
                            if route.operation_id in [OP_ID_AUTHORIZE, OP_ID_MAY_AUTHORIZE]]
        for route in router_authorize:
            method = list(route.methods)[0].lower()
            additional_header = {'name': 'Authorization', 'in': 'header', 'schema': {
                'title': 'Authorization', 'type': 'string'}, 'required': route.operation_id == OP_ID_AUTHORIZE}
            try:
                openapi_schema['paths'][route.path][method]['parameters'].append(
                    additional_header)
            except Exception:
                openapi_schema['paths'][route.path][method].update(
                    {'parameters': [additional_header]})

        app.openapi_schema = openapi_schema
        return app.openapi_schema
    return custom_openapi
