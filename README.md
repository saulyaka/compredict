#Title: Django DRF COMPREDICT / Repositoriy: saulyaka/compredict
version: 0.0.1
Author: Alla Popova
#Framework: Django
Data base: Sqlite3
#Project status: working/dev
Django server expose on 0.0.0.0:8000

#API documentation:
    path:
        /doc/schema/docs/

paths:
  /api/deviation/:
    post:
      operationId: api_deviation_create
      tags:
      - api
      requestBody:
        content:
          application/json:
            schema:
            {
                "sensor1": [5.44, 3.22, 6.55, 8.54, 1.24],
                "sensor_2": [5444.44, 33.22, 622.55, 812.54, 123.24],
                "sensor3": [0.44, 0.22, 0.55, 0.54, 0.24]
            }
      security:
      - jwtAuth: []
      responses:
        '200':
          content:
            application/json:
              schema:
                {
                "success": true,
                "result": {
                    "sensor1": [
                    0.17354382198293136,
                    -0.6981016187458169,
                    0.6093665423473053,
                    1.3907063743519035,
                    -1.475515119936322
                    ],
                    "sensor2": [
                    1.97918395667059,
                    -0.67356755290328,
                    -0.3846593127768078,
                    -0.2915201945550501,
                    -0.6294368964354521
                    ],
                    "sensor3": [
                    0.29452117456293736,
                    -1.248208787433402,
                    1.0658861555611072,
                    0.9957620663794554,
                    -1.1079606090700984
                    ]
                }
                }
        '400 BAD REQUEST'
  /api/token/:
    post:
      operationId: api_token_create
      description: |-
        Takes a set of user credentials and returns an access and refresh JSON web
        token pair to prove the authentication of those credentials.
      tags:
      - api
      requestBody:
        content:
          application/json:
            schema:
                    {
        "username": "admin",
        "password": "admin"
        }
        required: true
      responses:
        '200':
          content:
            application/json:
              schema:
                {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MDEyOTc0NiwiaWF0IjoxNjgwMDQzMzQ2LCJqdGkiOiI2MzcyZmQyYmI0NGM0MjM1ODQ4NmQ0MjBhNmFmZTQ1ZCIsInVzZXJfaWQiOjF9.Xb7l9SE30vYFMHXsbn0BPcJfuhSxiBUfzQEpFglWMzk",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgwMDQzNjQ2LCJpYXQiOjE2ODAwNDMzNDYsImp0aSI6IjM5MjU4MzNiOWIxNDQ2Y2Y5ZDZmYmZmNGU2OGZhZmIyIiwidXNlcl9pZCI6MX0.ET-TEE-MmFr0xv70Hm3ddDwC948CouMWdI8YXbGAcJE"
                }
  /api/token/refresh/:
    post:
      operationId: api_token_refresh_create
      description: |-
        Takes a refresh type JSON web token and returns an access type JSON web
        token if the refresh token is valid.
      tags:
      - api
      requestBody:
        content:
          application/json:
            schema:
            {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MDEyOTc0NiwiaWF0IjoxNjgwMDQzMzQ2LCJqdGkiOiI2MzcyZmQyYmI0NGM0MjM1ODQ4NmQ0MjBhNmFmZTQ1ZCIsInVzZXJfaWQiOjF9.Xb7l9SE30vYFMHXsbn0BPcJfuhSxiBUfzQEpFglWMzk"
            }
        required: true
      responses:
        '200':
          content:
            application/json:
              schema:
                {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgwMDQ4NDQ3LCJpYXQiOjE2ODAwNDMzNDYsImp0aSI6ImUyMjA4NjFiYjRlYzRiZTViYjNjNjU2NWFjYjcwZWRjIiwidXNlcl9pZCI6MX0.nie9ODtiiNB0W8wLThsE-6wnhQdm3j3eL13e0FQ4omk"
                }
  /doc/schema/:
    get:
      operationId: doc_schema_retrieve
      description: |-
        OpenApi3 schema for this API. Format can be selected via content negotiation.

      tags:
      - doc
      security:
      - jwtAuth: []
      - {}
      responses:
        '200':
          content:
            application/vnd.oai.openapi:
              schema:
                type: object
                additionalProperties: {}
            application/yaml:
              schema:
                type: object
                additionalProperties: {}
            application/vnd.oai.openapi+json:
              schema:
                type: object
                additionalProperties: {}
            application/json:
              schema:
                type: object
                additionalProperties: {}
          description: ''
components:
  schemas:
    StandardDeviation:
      type: object
      properties:
        success:
          type: boolean
        result:
          type: object
          additionalProperties: {}
      required:
      - result
      - success
    TokenObtainPair:
      type: object
      properties:
        username:
          type: string
          writeOnly: true
        password:
          type: string
          writeOnly: true
        access:
          type: string
          readOnly: true
        refresh:
          type: string
          readOnly: true
      required:
      - access
      - password
      - refresh
      - username
    TokenRefresh:
      type: object
      properties:
        access:
          type: string
          readOnly: true
        refresh:
          type: string
          writeOnly: true
      required:
      - access
      - refresh
  securitySchemes:
    jwtAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
        
Start application
in CL: docker-compose up
              docker-compose run --rm web python manage.py loaddata aircraft.json
              docker-compose run --rm web python manage.py loaddata flight.json
              docker-compose up
