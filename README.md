
TODOS:

1. See docker-compose file to arrange DEBUG=False and settings.py file to st ALLOWED_HOSTS
2. Review docerfile and docker-compose file 
    - change mongodb version to stable last version
    - Fix version 3 in the beginning of compose file
    - set env variables and call from settings or load
3. Check if you need uwsgi.ini file
4. Arrange mongo connection client structure to class based
5. Change os join BASEDIR template to pathlib version
6. db.feedback_collection.distinct("branch.name").length - birbasa gosterdiyin versiyada "" nezere alinmir
db.feedback_collection.distinct("branch.name").length
7. Htmlde branch None olan var.
8. 2 html faylin var
9. sumlar yerine add (performans ferqi)
10. addfield yerine birbasa projectde yazmaq

