## Contents
- [Intro](#intro)
- [Models](#models)
- [Views](#views)
  - [Authentication](#authentication)
  - [Permissions](#permissions)
  - [Mixins](#mixins)
  - [Cache](#cache)
  - [Endpoints](#endpoints)
- [Crud](#crud)

## Run
- [Run from docker-compose](#run-from-docker-compose)
__________
__________
## [Intro](#intro)
The project is initialized by a Django Command `common/management/commands/mock_users_and_projects.py`, this command creates 15 users from `user_1` to `user_15` with password `Passw0rd!` and an admin user with username `admin` and password `Passw0rd!`.

It also creates 3 `project` instances assigning users as follow:
* `proj1` --> `user_1`, `user_2`, `user_3`, `user_4`, `user_5` 
* `proj2` --> `user_6`, `user_7`, `user_8`, `user_9`, `user_10`
* `proj3` --> no user
* no project --> `user_11`, `user_12`, `user_13`, `user_14`, `user_15`

Rest Framework serializers are used only to serialize object and to check validity for input data. Validation in general is inside the models `clean` method and on models `constraints`.

Access to database is done by `crud` modules, so that Views can access to DB only through crud modules.

Main business logic is done in `core` or in `permissions` modules.

## [Models](#models)

* **common/models:BaseModel**
    
    Abstract model to handle common columns

* **projects/models:Project**
    
    General infos about the project, has both a 1to1 relation with `UserCustom` model as `creator` and a M2M relation as `assignees`

* **projects/models:ProjectAssignment**
    
    Bridge table for M2M relation `Project-UserCustom`, it has a `unique_toghether` constraint so that one user can be assigned to one project only once.

* **time_log/models:TimeLog**
    
    Keeps track of working time per user and per project, so it has a M21 relation with `ProjectAssignment` table both for `user` and `project`.
    The `end_time` field is null when a user is currently working on some project.
    It has a constraint to check that `end_time` is greater than `start_time` and performs additional validation in the `clean` method to ensure that two instance of `time_log` per same user and same project don't overlap.

* **users/models:UserCustom**
    
    Simply inherits from Django default `AbstractUser` model.

## [Views](#views)

### [Authentication](#authentication)
It is Session based authentication on top of all views and it is handled by `REST_FRAMEWORK` Basic Authentication and SessionAuthentication `DEFAULT_AUTHENTICATION_CLASSES`

### [Permissions](#permissions)
As a general rule, Admin user can do any operation, so next consideration are applied only to standard users. All classes inherits from `rest_framework.permissions.BasePermissions` overriding, as needed, `has_permission` and `has_object_permissions` method

* **common/permissions:IsAssignedToProjectOrAdmin**

    Checks that a user is access project or time_log information of only assigned projects

* **common/permissions:IsLogOwnerOrAdmin**

    Inherits from the previous and ensure that a time_log object can only be read by users that are part of the projects and can only be written by user who logged the specific object

* **common/permissions:IsAdminForWriting**

    Inherits from `rest_framework.permissions.IsAdminUser` to ensure that specic view is accessed by non admin users only for reading operations.


### [Mixins](#mixins)
All custom mixins implements the `initial` method of `rest_framework.views.APIView` mostly to inject in the view kwargs a specific object or to ensure that a required query parameter was provided

* **common/mixins:ObjectFromIdMixin**

    Base class that based on field `lookup_name` searches in the request kwargs the key to be used to search in the `crud_instance` field so that it can injects the specifc object in the request context using the `injection_name`. 
Optionally it can be defined as `required` so that if it is not found it will raise a `ParseError` exception

* **projects/mixins:ProjectFromIdMixin**

    Subclass of base `ObjectFromIdMixin`

* **projects/mixins:ProjectIdQueryStringMixin**

    Subclass of `ProjectFromIdMixin` ensures the `?project_id=_` is passed as query param
    
* **time_log/mixins:TimeLogFromIdMixin**

    Subclass of base `ObjectFromIdMixin`

* **users/mixins:UserIdQueryStringMixin**

    Takes user from optional `?user_id=_` query param


### [Cache](#cache)
Is implemented with a Redis container, it caches the GET views at high level


### [Endpoints](#endpoints)
* **projects/views:ProjectListCreateApi**

    ```shell
    /projects/
    ```
    
    **GET**

    Returns the list of projects per user (admin sees them all)

    **POST**
    
    Creates a project (only admin)

    _body_
    ```json
    {
        "name": "proj_test",
        "description": "my test proj"
    }
    ```

* **projects/views:ProjectRetrieveUpdateDelete**

    ```shell
    /projects/<id>
    ```
    
    **GET**

    Read a project instance, if assigned to user (admin sees them all)

    **PUT**
    
    Edit a project (only admin)

    _body_
    ```json
    {
        "name": "proj_test_edit",
        "description": "my test proj edited"
    }
    ```

    **DELETE**
    
    Delete a project (only admin)

* **projects/views:ProjectHandleUsers**

    ```shell
    /projects/<id>/handle_users
    ```

    **POST**
    
    Assign a list of users to a project (only admin)

    _body_
    ```json
    [
        "user_7",
        "user_8"
    ]
    ```

    **DELETE**
    
    Remove a list of users to a project (only admin)

    _body_
    ```json
    [
        "user_7"
    ]
    ```

* **projects/views:ProjectStatistics**

    ```shell
    /projects/<id>/statistics[?user_id=1]
    ```

    **GET**
    
    Total time spent on the given project from all assignees.

    _query param (optional)_
    
    `?user_id=1` 
    
    To see only time spent by a given user

* **time_log/views:TimeLogListCreateApi**

    ```shell
    /time_log/project_id=1
    ```
    
    **GET**

    Returns the list of time_log per user (admin sees them all)

    _query param (required)_
    
    `?project_id=1` 
    
    To indicate for which project get the logs

    **POST**
    
    Creates a time_log (only admin)

    _body_
    ```json
    {
        "start_time": "2022-12-23T12:41:52Z",
        "end_time": "2022-12-23T12:41:53Z"
    }
    ```

    _query param (required)_
    
    `?project_id=1` 
    
    To indicate for which project create the logs

* **time_log/views:TimeLogRetrieveUpdateDelete**

    ```shell
    /time_log/<id>
    ```
    
    **GET**

    Read a time_log instance, if user is assigned to project (admin sees them all)

    **PUT**
    
    Edit a time_log if user was the logger (admin edits them all)

    _body_
    ```json
    {
        "name": "proj_test_edit",
        "description": "my test proj edited"
    }
    ```

    **DELETE**
    
    Delete a time_log if user was the logger (admin deleted them all)

## [Crud](#crud)
In this module there are the classes that access to Database.
All classes inherit from `common/crud:BaseCRUD` that implements some basic methods.

__________
__________

## [Run from docker-compose](#run-from-docker-compose)

The Django server is exposed on port `7777`
```shell
docker-compose up
```

To run tests, from a different terminal run 
```shell
docker exec ptt_backend python project_time_tracker/manage.py test tests     
```

To run again the init command, run 
```shell
docker exec ptt_backend python project_time_tracker/manage.py mock_users_and_projects     
```
