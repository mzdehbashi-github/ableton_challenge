## Ableton challenge

### Prerequisites
  - docker
  - docker-compose


### How to set up and run
```shell
# Spin up the services
docker-compose up --build

# Exec into container and create django-admin user
1- docker exec -it ableton_challenge-backendserver-1 bash
2- python manage.py createsuperuser

# Now, you can access django admin dashboard at http://localhost:8000/admin
```

```shell
# Run the tests
docker-compose run backendserver python3 manage.py test --failfast
```

#### You can also visit API-docs on http://localhost:8000/swagger to explore and try the endpoints
Small hint: In order to confirm your email, please visit the django-admin dashboard to check the new <br>
(created or updated) code, after doing signup or resending email-confirmation email.

##
#### Regarding the solution that I implemented:
- Why Django: I used Django since these day I am working alot with django ,and it helps me to implement the solution faster.
If I had more time, then I'd be happy to try fastAPI as well.

- Why using django-mailer (https://github.com/pinax/django-mailer): In order to prevent having the problem of dual
writes, I decided to choose this library. since it first stores the emails in a table (somehow works as a queue)
and then we can send the emails, periodically. I did not implement the cron-job though, but I think celery is a
good choice.
- Why using services (package `user_management.services`): I think it is a good idea to isolate the business
logic into separate functions, it helps readability, maintainability
(the business logic is not scattered among multiple components. i.e. serializer, view, model) and testability of the code
so my idea for testing was, I can write 100% percent coverage tests for service functions, and when writing tests
for views, I can mock the service functions (which are used by the view) and only focus on testing the code inside
the view class/function. I think to use services is a good trade-off (of course it depends on business requirements)
it does not have the complexity of hexagonal or domain driven architecture, but still gives us a good isolation between
different components in the code, and helps the code to be better organized.
