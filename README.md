# Social network test app

# TODO
- make docker-compose file to easy deployment (PostgreSQL/NGINX/REDIS/CELERY Workers)
- optimization of post sync with queue workers

## Table of content
 - [installation](#installation)
 - [API](#api)


## installation
1. Clone the repo
    ```shell script
    git clone https://github.com/nabakirov/social_net.git
    ```
2. Step into repo dir
    ```shell script
    cd social_net/app
    ```
3. Install dependencies   
    using virtualenv
    ```shell script
    python3 -m virtualenv venv && source venv/bin/activate && pip install -r requirements.txt
    ```
4. Set environment variables
    - SECRET_KEY=secret
    - DEBUG=True
    - REDIS_URL=redis://localhost:6379
    - DATABASE_ENGINE=django.db.backends.sqlite3
    - DATABASE_NAME=./db.sqlite3
    - DATABASE_USER=user
    - DATABASE_PASSWORD=pwd
    - DATABASE_HOST=localhost
    - DATABASE_PORT=5432
    - ABSTRACT_EMAIL_API_KEY=token
    - ABSTRACT_IP_API_KEY=token
    - ABSTRACT_HOLIDAY_API_KEY=token

5. Run the tests
   ```shell script
    python3 manage.py tests
    ```
6. Run the celery
   ```shell script
    celery -A socialnet.celery worker
    ```
7. Run the backend
   ```shell script
    python3 manage.py runserver
    ```
8. [Optional] Run with the gunicorn 
   ```shell script
    gunicorn --timeout 120 -w 3 -b 0.0.0.0:80 socialnet.wsgi
    ```

## API
_Authorization_:
```bash
--header 'Authorization: Bearer {access_token}'
```

_Pagination controls with query params_:   
   - ?limit=100
   - ?offset=100

**MAX PAGE SIZE IS 1000**

```json5
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

_topics_: 
- [Auth](#auth)
- [profile](#profile)


### auth
#### signup - POST */auth/v1/signup/*
##### access - *public*

_body_: 

|field | data type | description|
|- | - | -|
|**email** | str | valid email address|
|**password** | str | password|
|first_name | str | first name|
|last_name| str | last name|
 
_response_ 200
```json5
{
    "user": {
        "id": 5,
        "create_date": "2024-10-28T14:52:09.412370Z",
        "email": "nabakirov2@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "refresh": "JWT token",
    "access": "JWT token"
}
```
#### login - POST */auth/v1/login/*
##### access - *public*

_body_:

|field | data type | description|
|- | - | -|
|**email** | str | valid email address|
|**password** | str | password|
 
_response_ 200
```json5
{
    "user": {
        "id": 5,
        "create_date": "2024-10-28T14:52:09.412370Z",
        "email": "nabakirov2@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "refresh": "JWT token",
    "access": "JWT token"
}
```
#### refresh token - POST */auth/v1/refresh/*
##### access - *public*

_body_:

|field | data type | description|
|- | - | -|
|**refresh** | str | refresh token|
 
_response_ 200
```json5
{
    "access": "JWT token"
}
```

### profile
#### get profile - GET */auth/v1/profile/*
##### access - *authorized*

_response_ 200
```json5
{
    "id": 1,
    "create_date": "2024-10-26T12:56:18.447477Z",
    "email": "asdf@asdf.asdf",
    "first_name": "",
    "last_name": ""
}
```

#### update profile - PATCH */auth/v1/profile/*
##### access - *authorized*
_body_: 

|field | data type | description|
|- | - | -|
|first_name | str | first name|
|last_name | str | last name|

_response_ 200
```json5
{
    "id": 1,
    "create_date": "2024-10-26T12:56:18.447477Z",
    "email": "asdf@asdf.asdf",
    "first_name": "",
    "last_name": ""
}
```

### personal posts
#### list of posts - GET */auth/v1/posts/*
##### access - *authorized*

_paginated response_ 200

|field | data type | description|
|- | - | -|
|id | int8 | ID |
|create_date | ISO str | datetime of creation|
|author | obj | public user info|
|title | str | title|
|description | str | description|
|is_private | bool | will be shown only for the author in case of private post, otherwise post will be public|
|like_count | int8 | actual like count|

_example_:
```json5
[
   {
      "id": 1,
      "create_date": "2024-10-27T08:35:56.741898Z",
      "author": {
         "id": 1,
         "first_name": "",
         "last_name": ""
      },
      "title": "Hello World",
      "description": "This is a test project",
      "is_private": false,
      "like_count": 1
   }
]
```
#### create post - POST */auth/v1/posts/*
##### access - *authorized*

_body_:

|field | data type | description|
|- | - | -|
|**title** | str | title|
|**description** | str | description|
|is_private | bool | - |


_response_ 201:
```json5
{
    "id": 3,
    "create_date": "2024-10-28T15:16:59.449118Z",
    "title": "Hello World",
    "description": "This is a test project",
    "is_private": false
}
```
#### update post - PATCH */auth/v1/posts/*
##### access - *authorized*

_body_:

|field | data type | description|
|- | - | -|
|title | str | title|
|description | str | description|
|is_private | bool | - |


_response_ 200:
```json5
{
    "title": "Hello World",
    "description": "This is a test project",
    "is_private": false
}
```
#### delete post - DELETE */auth/v1/posts/{ID}/*
##### access - *authorized*

_response_ 204


### public feed
#### list of posts - GET */auth/v1/feed/*
##### access - *authorized*

_paginated response_ 200

|field | data type | description|
|- | - | -|
|id | int8 | ID |
|create_date | ISO str | datetime of creation|
|author | obj | public user info|
|title | str | title|
|description | str | description, showing only 100 first symbols |
|like_count | int8 | cached like count|
|liked | bool | has the user liked the post|

example:
```json5
[
   {
      "id": 2,
      "create_date": "2024-10-28T15:15:00.794768Z",
      "author": {
         "id": 1,
         "first_name": "",
         "last_name": ""
      },
      "title": "Hello World",
      "description": "This is a test project",
      "like_count": 0,
      "liked": false
   }
]
```
#### like/unlike the post - POST */auth/v1/feed/{ID}/like/*
##### access - *authorized*

If user has liked the post -> post will be unliked
If user has not liked the post -> post will be liked

_response_ 200
