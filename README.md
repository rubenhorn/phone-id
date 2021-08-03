# PhoneID microservice

## Environment variables
### General
* _JWT_SECRET_  
Secret used by backend to sign and verify JWTs (required)
* _USE_OPENAPI_  
Exposes interactive documentation at /docs if set to `true`
* _USE_POSTGRESQL_DIALECT_  
Use PostgreSQL specific language dialect (requires PostgreSQL database server being used)
### Database (PostgreSQL)
If not all of these variables are set, an in memory SQLite database will be used as fallback.
* _POSTGRESQL_USER_  
PostreSQL username
* _POSTGRESQL_PASS_  
PostgreSQL password
* _POSTGRESQL_HOST_  
PostgreSQL hostname, IP address or FQDN
* _POSTGRESQL_PORT_  
PostgreSQL port
* _POSTGRESQL_DB_  
PostgreSQL database name
### Verification service (Vonage)
If not all of these variables are set, an offline service mock will be used.
* _VONAGE_API_KEY_  
API key for [Vonage Verify](https://www.vonage.com/communications-apis/verify/)
* _VONAGE_API_SECRET_  
API secret for [Vonage Verify](https://www.vonage.com/communications-apis/verify/)

## Run locally
1. Install requirements with `pip3 install -r requirements.txt`
2. Create .env file from template
3. Run app with `uvicorn --env-file ./.env --app-dir ./app/ main:app`
4. Explore API at http://127.0.0.1:8000/docs

## Run tests
Run `pytest` from the root folder.

## Deployment
The application can be run inside a docker container.  
Environment variables must be provided by compose or kubernetes.
