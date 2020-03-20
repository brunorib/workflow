# WORKFLOW REST SERVICE
Service in charge of workflow

Set up to develop
1. Install with: 
'python setup.py install'

2. Start database server 
'pg_ctl -D /usr/local/var/postgres/ start'

3. Create flask_api database 
'createdb flask_dev'

4a. Run api
'export $(cat .env)'
'python manage.py run'

4b. Run api in container
'docker build . -t workflow-mq:0.1.0-SNAPSHOT .'
'docker run --env-file .env workflow-mq:0.1.0-SNAPSHOT'