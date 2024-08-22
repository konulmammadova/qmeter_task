Oxumadan Keçməyin

Qeyd: 
Proyekti dockerdə qaldırdıqdan dərhal sonra test databazası üçün aşağıdakı kommandan istifadə edin:
	
	docker exec -it qm-feedback-app python /app/restore_db.py

Test etmek ucun browserde asagidaki url-leri aca bilersiz:
http://localhost:8000/score-table/1/
http://localhost:8000/score-table/2/

Proyektde neler edilib:
Dockerfile ve docker-compose fayllari struktura uygun yazilib.
Tapsiriqda istenilen table-in gosterilmesi 2 ferqli yolla yerine yetirilib. 
	

