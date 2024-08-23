# ⚠️ Oxumadan keçməyin


# Mündəricat
#### Ən önəmli başlıq ən sondadır
- [Proyektin quraşdırılması](#proyektin-quraşdırılması)
- [Birbaşa nəticəni görmək üçün](#birbaşa-nəticəni-görmək-üçün)
- [Nəzər yetirilməli olan fayllar](#nəzər-yetirilməli-olan-fayllar)
- [Proyektdə nələr edilib](#proyektdə-nələr-edilib)
- [Kod Strukturu Haqqında](#kod-strukturu-haqqında-***) ***


## Proyektin quraşdırılması

Dockeri qaldırdıqdan dərhal sonra test databazası üçün aşağıdakı kommandı icra edin:

```bash
docker-compose up --build -d
docker exec -it qm-feedback-app python manage.py restore_db
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
- MongoDB və Django proyekti üçün **Dockerfile** və **docker-compose** faylları uyğun formada yazılaraq proyekt *dockerize* edilib.
- Tapışırıqda istənilən table-ın göstərilməsi üçün 2 alternativ yoldan istifadə edilib:
    1. - Qruplaşdırma və hesablamalar; yəni datanın *branch name* və *service name*-lərə görə qruplaşdırılıb;   
       **100 * ( birlərin sayı * 10 + ikilərin sayı * 5 + üçlərin sayı * 0 + dördlərin sayı * -5 +
beşlərin sayı * -10 ) / (bir + iki + üç+ dörd + beşlərin sayı ) * 10**  
düsturu ilə hesablanması, tapşırıqda istənildiyi kimi MongoDB query-si ilə yazılıb.(qmeter/client.py faylındakı [`get_score_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L22) methodunda)
        - Əldə olunan *output document*-lərin üzərində Pythonla dəyişiklik edilərək istənilən formatda table-da göstərilib.(feedback/views.py faylında -[`ScoreTable1View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L6)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L9) methodunda)

     2. Qruplaşdırma və hesablamaların edilməsi, həmçinin table-da göstərmək üçün uyğun formata salınması MongoDB query-si ilə edilib və birbaşa istifadə olunub.(qmeter/client.py faylındakı  [`get_score_data_by_branch`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L90) və [`ScoreTable2View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L74)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L117) methodunda)

## Kod Strukturu Haqqında ***

- [aggregate pipeline](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L91)-ları uzun sətirlərlə olsa da bütöv bir python kodu halında yazılıb ki, eyni python kodlarını MongoDB query-ləri olaraq tam şəkildə görmək və test etmək mümkün olsun.

- *Query*-ləri *view*-ların içində birbaşa yazmaq yerinə [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L6) *class*-ından istifadə olunub. İçində uzun pipeline kodları olduğu üçün ən yaxşı versiyasında deyil. Uzun pipeline kodlarının olduğu kimi yazılmasının səbəbini artıq oxumusunuz. *Bu class sadəcə həm kod səliqəliliyi üçündür, həm də ümumi məqsədlidir, yəni, query sayı artdıqca və ya başqa collection-lardan data götürmək lazım olduqca [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L6)-a yeni methodlar əlavə olunaraq istifadə oluna bilər.* 

- Kodda bəzi yerlərdə faydalı olacağı düşünülərək, xüsusilə method *return type*-larını göstərmək üçün **type hinting** istifadə olunub. 

## MongoDB Query-ləri Haqqında ```python ```
1. Hər iki pipeline aggregation-da ( [pipeline1](https://github.com/konulmammadova/qmeter_task/blob/52176945760f8bd89171551e29b71242e09f7e70/qmeter/client.py#L28), [pipeline2](https://github.com/konulmammadova/qmeter_task/blob/52176945760f8bd89171551e29b71242e09f7e70/qmeter/client.py#L99) ), eyni branch-daki hər bir servisi ayrı-ayrı handle edə bilək deyə `{ $unwind: "$feedback_rate" }` *stage*-i əlavə olunub.   

   Hər document-də service-lər feedback_rate içində aşağıdakı formada saxlanılır.
   ```python
      "feedback_rate": [
      {
         "service": {...},
         "rate_option": 4,
         ...
      },
      {
         "service": {...},
         "rate_option": 4,
         ...
      }
   ]
   ```
   `$unwind` istifadə edərək yuxarıdakı 1 document əvəzinə aşağıdakı kimi 2 ayrı document əldə etmiş oluruq:

   ```python
      "feedback_rate": [
         ...
         "service": {...},
         "rate_option": 4,
         ...
      ]
   ```

   ```python
      "feedback_rate": [
         ...
         "service": {...},
         "rate_option": 5,
         ...
      ]
   ```
   və datanı bu formada növbəti $group stage-nə ötürürük.

2. $group stage-də datanı branch name və service name-ə əsasən qruplayıb növbəti stage-ə hesablamaları apara bilməyi üçün tapşırıqda verilən düstura əsasən hər bir rate_option sayını hesablayırıq:
```python
"$group": {
            "_id": {
               "branch_name": "$branch.name",
               "service_name": "$feedback_rate.service.name"
            },
            "ones": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 1] }, 1, 0] }},
            "twos": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 2] }, 1, 0] }},
            "threes": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 3] }, 1, 0] }},
            "fours": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 4] }, 1, 0] }},
            "fives": { "$sum": { "$cond": [{ "$eq": ["$feedback_rate.rate_option", 5] }, 1, 0] }}
}
```

3. Bura qədərki query-lər hər iki pipeline üçün eyni idi. İndi isə [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/52176945760f8bd89171551e29b71242e09f7e70/qmeter/client.py#L28)-dən davam edək. [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/52176945760f8bd89171551e29b71242e09f7e70/qmeter/client.py#L28) sadəcə düsturla bağlı qruplaşdırma ve hesablamanı edirdi. Burada növbəti stage output documenti formalaşdırdığımız $project stage-dir.
```python
"$project": {
      "_id": 0,
      "branch_name": "$_id.branch_name",
      "service_name": "$_id.service_name",
      "ones": "$ones", 
      "twos": "$twos", 
      "threes": "$threes", 
      "fours": "$fours", 
      "fives": "$fives",
      "total": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
      "score": { 
         "$cond": { 
               "if": { "$gt": [ { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] },
               "then": {
                  "$divide": [
                     {
                           "$multiply": [
                              100,
                              {
                                 "$sum": [
                                       { "$multiply": ["$ones", 10] },
                                       { "$multiply": ["$twos", 5] },
                                       { "$multiply": ["$fours", -5] },
                                       { "$multiply": ["$fives", -10] }
                                 ]
                              }
                           ]
                     },
                     {
                           "$multiply": [
                              { "$sum": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
                              10
                           ]
                     }
                  ]
               },
               "else": 0
         }    
      }
   }
}
```python

feedback_rate array-indəki services array-i əvəzinə hər feedback_rate içində bir service objekti olan document əldə etmiş oluruq

--------
// Unwind the feedback_rate array to handle each service individually
    { $unwind: "$feedback_rate" },
    
------
// Group by branch.name and service.name, and accumulate the counts for each rate_option
```python
    {
        $group: {
            _id: {
                branch: "$branch.name",
                service: "$feedback_rate.service.name"
            },
            count1: { $sum: { $cond: [{ $eq: ["$feedback_rate.rate_option", 1] }, 1, 0] } },
            count2: { $sum: { $cond: [{ $eq: ["$feedback_rate.rate_option", 2] }, 1, 0] } },
            count3: { $sum: { $cond: [{ $eq: ["$feedback_rate.rate_option", 3] }, 1, 0] } },
            count4: { $sum: { $cond: [{ $eq: ["$feedback_rate.rate_option", 4] }, 1, 0] } },
            count5: { $sum: { $cond: [{ $eq: ["$feedback_rate.rate_option", 5] }, 1, 0] } }
        }
    }
```  
    