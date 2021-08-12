## TEST TASK

## Social Network
Object of this task is to create a simple REST API.
API was created using Django Rest Framework.

## Set up and run project:


You should change your work directory to '/network' and run commands:
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
After all you will be able to make requests to ```http://127.0.0.1:8000/```

## Available requests

### Account
#### Register new user:

```POST auth/users/```
```
Request body:
* form-data

Fields:
* email: <email>
* username: <str>
* password: <str>
```

#### Login to service:

```POST auth/jwt/create/```
```
Request body:
* form-data

Fields:
* email: <email>
* password: <str>
```
If credentials are valid and user is authenticated
you will get response with access and refresh tokens.


#### Get user's last activity information(by id):

```GET /api/account/user-activity/```
```
Request headers:
* key: Authorization
* value: 'Bearer' + access token

Query parameters:
* user_id: <int>
```
By default all authenticated user are allowed to make this request.
But we can change permission class for this route if we want to limit the access.

### Post
#### Create the post:

```POST api/post/create/```
```
Request body:
* form-data

Fields:
* content: <Text>

Request headers:
* key: Authorization
* value: 'Bearer' + access token
```
#### Like/unlike post(by post_id):

```POST api/post/<int:post_id>/like/```
```
Request headers:
* key: Authorization
* value: 'Bearer' + access token
```
### Analytics
#### Get count of likes for exact date from date range:

```GET api/analytics/likes-by-day/```
```
Request headers:
* key: Authorization
* value: 'Bearer' + access token
Query parameters:
* date_from: <YYYY-MM-DD>
* date_to: <YYYY-MM-DD>
```
By default all authenticated user are allowed to make this request.
But we can change permission class for this route if we want to limit the access.

## Response status codes
* correct request(loging in, unliking post): 200 OK
* correct request which create some new instance(user, post, like): 201 CREATED
  

* uncorrect request(wrong query parameters): 400 BAD REQUEST
* uncorrect request(user not authenticated): 401 UNAUTHORIZED
* uncorrect request(wrong url, post, user does not exist, etc): 404 NOT FOUND

## Tests

In each application directory(account, analytics, post)
you can find 'tests' directory which contains modules to test this application.

#### To run all project test you should run command:
```
coverage run --source='.' manage.py test .
```
#### To get report about test coverage after testing you should run command:
```
coverage report
```

## Note

If you are going to deploy django application like this on production server, you should remember to 'hide' your SECRET_KEY from settings.py
to environment variable and set DEBUG mode to False. Otherwise, your application will not secure.

