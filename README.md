# ⚠️ Oxumadan keçməyin


# Mündəricat
#### Ən önəmli başlıq ən sondadır
- [Proyektin quraşdırılması](#proyektin-quraşdırılması)
- [Birbaşa nəticəni görmək üçün](#birbaşa-nəticəni-görmək-üçün)
- [Nəzər yetirilməli olan fayllar](#nəzər-yetirilməli-olan-fayllar)
- [Proyektdə nələr edilib](#proyektdə-nələr-edilib)
- [Kod Strukturu Haqqında](#kod-strukturu-haqqında) ***


## Proyektin quraşdırılması

Dockeri qaldırdıqdan dərhal sonra test databazası üçün aşağıdakı kommandı icra edin:

```bash
docker exec -it qm-feedback-app python /app/restore_db.py
```

## Birbaşa nəticəni görmək üçün:
- `http://localhost:8000/score-table/1/`  
və ya
- `http://localhost:8000/score-table/2/` 

url-lərinə daxil ola bilərsiz. 
 
(Hər iki url datanı eyni formada göstərən lakin, fərqli üsullarla yazılmış variantlardır.)

## Nəzər yetirilməli olan fayllar:
 - [*Dockerfile*](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/Dockerfile)
 - [*docker-compose.py*](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/docker-compose.yml)
 - [*feedback/views.py*](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py)
 - [*feedback/templates/feedback/score_table.html*](https://github.com/konulmammadova/qmeter_task/blob/main/feedback/templates/feedback/score_table.html)
 - [*qmeter/client.py*](https://github.com/konulmammadova/qmeter_task/blob/main/qmeter/client.py) (MongoDB query-ləri burada yerləşir.)

## Proyektdə nələr edilib:
- MongoDB və Django proyekti üçün [**Dockerfile**] və **docker-compose** faylları uyğun formada yazılaraq proyekt *dockerize* edilib.
- Tapışırıqda istənilən table-ın göstərilməsi üçün 2 alternativ yoldan istifadə edilib:
    1. - İstənilən qruplaşdırma və hesablamalar; yəni datanın *branch name* və *service name*-lərə görə qruplaşdırılıb;   
       **100 * ( birlərin sayı * 10 + ikilərin sayı * 5 + üçlərin sayı * 0 + dördlərin sayı * -5 +
beşlərin sayı * -10 ) / (bir + iki + üç+ dörd + beşlərin sayı ) * 10**  
düsturu ilə hesablanması, tapşırıqda istənildiyi kimi MongoDB query-si ilə yazılıb.(qmeter/client.py faylındakı [`get_score_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L22) methodunda)
        - Əldə olunan *output document*-lərin üzərində Pythonla dəyişiklik edilərək istənilən formatda table-da göstərilib.(feedback/views.py faylında -[`ScoreTable1View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L6)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L9) methodunda)

     2. İstənilən qruplaşdırma və hesablamaların edilməsi, həmçinin table-da göstərmək üçün uyğun formata salınması MongoDB query-si ilə edilib və birbaşa istifadə olunub.(qmeter/client.py faylındakı  [`get_score_data_by_branch`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L90) və [`ScoreTable2View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L74)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L117) methodunda)

## Kod Strukturu Haqqında ***

- [*aggregate pipeline*](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L91)-ları uzun sətirlərlə olsa da bütöv bir python kodu halında yazılıb ki, eyni python kodlarını MongoDB query-ləri olaraq tam şəkildə görmək və test etmək mümkün olsun.

- *Query*-ləri *view*-ların içində birbaşa yazmaq yerinə [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L6) *class*-ından istifadə olunub. Bu *class* həm kod səliqəliliyi üçündür, həm də ümumi məqsədlidir, yəni, query sayı artdıqca və ya başqa *collection*-lardan data götürmək lazım olduqca [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L6)-a yeni methodlar əlavə olunaraq istifadə oluna bilər.(qmeter/client.py faylında)

- Kodda bəzi yerlərdə faydalı olacağı düşünülərək, xüsusilə method *return type*-larını göstərmək üçün **type hinting** istifadə olunub. 
