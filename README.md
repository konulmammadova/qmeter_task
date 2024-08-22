
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

how can I turn into 
[{'branch_name': 'NEW BASHIR', 
'service_name': 'Bashir servis', 
'ones': 2, 
'twos': 0, 
'threes': 0, 
'fours': 2, 
'fives': 6, 
'total': 10, 
'score': -50.0}, 
{'branch_name': 'role test ucun', 
'service_name': 'Yeni servis',
'ones': 1,
'twos': 0,
'threes': 0, 
'fours': 0,
'fives': 0, 
'total': 1, 
'score': 100.0}, 
{'branch_name': 'role test ucun', 
'service_name': 'Other servis',
'ones': 1,
'twos': 0,
'threes': 0, 
'fours': 0,
'fives': 0, 
'total': 1, 
'score': 50.0}, 
] type of list to a dictionary like 

{'NEW BASHIR': {'services': [{'service_name': 'Bashir servis', 
'ones': 2, 
'twos': 0, 
'threes': 0, 
'fours': 2, 
'fives': 6, 
'total': 10, 
'score': -50.0}]},
'role test ucun': {'services': [{'service_name': 'Yeni servis',
'ones': 1,
'twos': 0,
'threes': 0, 
'fours': 0,
'fives': 0, 
'total': 1, 
'score': 100.0},{'Other servis',
'ones': 1,
'twos': 0,
'threes': 0, 
'fours': 0,
'fives': 0, 
'total': 1, 
'score': 50.0} ]}
}
