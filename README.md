# ⚠️ Oxumadan keçməyin


# Mündəricat
#### Ən önəmli başlıq ən sondadır
- [Proyektin quraşdırılması](#proyektin-quraşdırılması)
- [Birbaşa nəticəni görmək üçün](#birbaşa-nəticəni-görmək-üçün)
- [Nəzər yetirilməli olan fayllar](#nəzər-yetirilməli-olan-fayllar)
- [Proyektdə nələr edilib](#proyektdə-nələr-edilib)
- [Kod Strukturunun İzahı](#kod-strukturunun-izahı-***) ***


## Proyektin quraşdırılması

Proyekti Dockerdə qaldırmaq üçün build commandını və ondan dərhal sonra test databazası üçün növbəti kommandı icra edin:

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
 - [*Dockerfile*](https://github.com/konulmammadova/qmeter_task/blob/main/Dockerfile)
 - [*docker-compose.py*](https://github.com/konulmammadova/qmeter_task/blob/main/docker-compose.yml)
 - [*feedback/views.py*](https://github.com/konulmammadova/qmeter_task/blob/main/feedback/views.py)
 - [*feedback/templates/feedback/score_table.html*](https://github.com/konulmammadova/qmeter_task/blob/main/feedback/templates/feedback/score_table.html)
 - [*qmeter/client.py*](https://github.com/konulmammadova/qmeter_task/blob/main/qmeter/client.py) (MongoDB query-ləri burada yerləşir.)

## Proyektdə nələr edilib:
- MongoDB və Django proyekti üçün **Dockerfile** və **docker-compose** faylları uyğun formada yazılaraq proyekt *dockerize* edilib.
- Tapışırıqda istənilən table-ın göstərilməsi üçün 2 alternativ yoldan istifadə edilib:
**1-ci yol:** - Qruplaşdırma və hesablamalar; yəni datanın *branch name* və *service name*-lərə görə qruplaşdırılıb;   
       `**100 * ( birlərin sayı * 10 + ikilərin sayı * 5 + üçlərin sayı * 0 + dördlərin sayı * -5 +
beşlərin sayı * -10 ) / (bir + iki + üç+ dörd + beşlərin sayı ) * 10**`  
düsturu ilə hesablanması, tapşırıqda istənildiyi kimi MongoDB query-si ilə yazılıb.(qmeter/client.py faylındakı [`get_score_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/qmeter/client.py#L22) methodunda)
        - Əldə olunan *output document*-lərin üzərində Pythonla dəyişiklik edilərək istənilən formatda table-da göstərilib.(feedback/views.py faylında -[`ScoreTable1View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L6)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L9) methodunda)


   **2-ci yol:** Qruplaşdırma və hesablamaların edilməsi, həmçinin table-da göstərmək üçün uyğun formata salınması MongoDB query-si ilə edilib və birbaşa istifadə olunub.(qmeter/client.py faylındakı  [`get_score_data_by_branch`](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L96) və [`ScoreTable2View`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L74)-da [`get_context_data`](https://github.com/konulmammadova/qmeter_task/blob/ada6f363ea41386ea387c1891625f2bd61d8fda9/feedback/views.py#L117) methodunda)

## Kod Strukturunun İzahı ***

- Aggregate pipeline-ları uzun sətirlərlə olsa da bütöv bir python kodu halında yazılıb ki, həmin python kodlarını MongoDB query-ləri olaraq tam şəkildə görmək və test etmək mümkün olsun.

- *Query*-ləri *view*-ların içində birbaşa yazmaq yerinə [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L9) *class*-ından istifadə olunub. İçində uzun pipeline kodları olduğu üçün ən yaxşı versiyasında deyil. Uzun pipeline kodlarının olduğu kimi yazılmasının səbəbini artıq oxumusunuz. *Bu class sadəcə həm kod səliqəliliyi üçündür, həm də ümumi məqsədlidir, yəni, query sayı artdıqca və ya başqa collection-lardan data götürmək lazım olduqca [`MongoDBClient`](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L9)-a yeni methodlar əlavə olunaraq istifadə oluna bilər.* 

- Kodda bəzi yerlərdə faydalı olacağı düşünülərək, xüsusilə method *return type*-larını göstərmək üçün **type hinting** istifadə olunub. 

## MongoDB Query-lərinin İzahı 
##### Pipeline-1 və Pipeline-2 -də unwind və group stage-ləri
- Hər iki pipeline aggregation-da ( [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L29), [Pipeline-2](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L100) ), eyni branch-daki hər bir servis ayrı-ayrı handle edə bilək deyə `{ $unwind: "$feedback_rate" }` *stage*-i əlavə olunub.   

   Hər document-də *service*-lər *feedback_rate* içində aşağıdakı formada saxlanılır.
   ```python
   {
      "branch": { ..., "name": "Branch 1" },
      "feedback_rate": [
         {
            "service": {..., "name": "A" },
            "rate_option": 4,
            ...,
         },
         {
            "service": {..., "name": "B" },
            "rate_option": 5,
            ...,
         }
      ]
   }
   ```
   `$unwind` istifadə edərək yuxarıdakı 1 document əvəzinə aşağıdakı kimi 2 ayrı document əldə etmiş oluruq:

   ```python
   {
      "branch": { ..., "name": "Branch 1" },
      "feedback_rate": [
         ...
          "service": {..., "name": "A" },
         "rate_option": 4,
         ...
      ]
   }
   ```

   ```python
   {
      "branch": { ..., "name": "Branch 1" },,
      "feedback_rate": [
         ...
          "service": {..., "name": "B" },
         "rate_option": 5,
         ...
      ]
   }
   ```
   və datanı bu formada növbəti $group stagenə ötürürük.

- `$group` *stage*-də datanı branch name və service name-ə əsasən qruplaşdırılır, növbəti stage-də tapşırıqda verilən düsturla bağlı hesablamaları aparmaq üçün lazım olan hər bir *rate_option* sayı hesablanır:
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

##### Pipeline-1 -də sonuncu stage
Bura qədərki query-lər hər iki pipeline üçün eyni idi. İndi isə [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/main/qmeter/client.py#L28) üzərindən davam edək. [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/main/qmeter/client.py#L28) yalnız düsturun tətbiqinə fokuslandığım query-lərdir. Burada növbəti, yəni 3-cü *stage*, output documenti formalaşdırdığım `$project` stage-dir.
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
```  
Bu stage-də;
   - `_id` -ni output document-də göstərməmək üçün `"_id": 0` yazmışam.
   - Datanı table-da göstərərkən 1-lərin, ..., 5-lərin sayı lazım olacağı üçün (pythonla       sonradan hesablaya bilməyəcəyim üçün) onları da əlavə etmişəm.
   - `$group` *stage*-dən aldığım field-lərin dəyərlərini istifadə etmişəm.
   - `score` fieldinin hesablamaq almaq üçün də düsturu tətbiq etmişəm. 
   - 0-a bölünmə xətasının qarşısını almaq üçün `if else` istifadə etmişəm:
 `"if": { "$gt": [ { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] }, 0] }`
   - **`$sum` əvəzinə `$add` istifadə etmişəm. Document içində field dəyərlərini toplayarkən bu dəyərlərin sayı bəllidirsə(çox deyilsə), belə hallarda `$add` `$sum`-dan daha optimal/sürətli işləyir.**
   - **Oxunaqlılıq üçün `score` dəyərini `$addField` stage-ində hesablaya bilərdim. Bu həm də onu, növbəti diğər stage-lər olarsa, birdən çox yerdə istifadə etmək şansı verərdi. Lakin, `score`-u son dəyər olaraq hesabladığım üçün birbaşa `$project` stage-ində yazdım.**

 [Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L28)-in tətbiqi burada bitir və biz datanı table üçün uyğun formata gətirmək üçün view içərisində [python kodlarını](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/feedback/views.py#L19) tətbiq edirik.

##### Pipeline-2 -də Stage-lər
[Pipeline-2](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L99)-də isə data üzərində yalnız düsturu tətbiq etməyə fokuslanmamışam, eyni zamanda table-da göstərə bilmək üçün uyğun formata çevirmişəm. Bu pipeline-da `$unwind` və `$group` stage-lərindən sonra gələn stage-lər bunlardır:
      - 2 ədəd `$addField` stage-i
      - növbəti `$group` stage-i
      - `$project` stage-i

`$addField` stage-ləri belədir:
```python
{
   "$addFields": {
      "total_count": { "$add": ["$ones", "$twos", "$threes", "$fours", "$fives"] },
      "weighted_sum": {
         "$add": [
               { "$multiply": ["$ones", 10] },
               { "$multiply": ["$twos", 5] },
               { "$multiply": ["$fours", -5] },    
               { "$multiply": ["$fives", -10] }
         ]
      }
   }
},

{
   "$addFields": {
      "score": {
         "$cond": {
            "if": { "$gt": ["$total_count", 0] },
            "then": {
               "$multiply": [
                  { "$divide": [{ "$multiply": ["$weighted_sum", 100] }, { "$multiply": ["$total_count", 10] }] },
                  1
               ]
            },
            "else": 0
         }
      }  
   }
},
```

Burada oxunaqlılıq, *modularity* və daha rahat debug etmək adına  2 ədəd `"$addFields"` istifadə etmişəm. 1-ci `"$addFields"`-də yaratdığım `total_count` və `weighted_sum` fieldlərini 2-ci `"$addFields"`-də `score` hesablamaq üçün istifadə etmişəm.

[Pipeline-1](https://github.com/konulmammadova/qmeter_task/blob/main/qmeter/client.py#L28)-dən fərli olaraq, [Pipeline-2](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L99)-də datanı sonradan Pythonla uyğun formata salmaq əvəzinə həmin işi Pipeline-2-nin özündə aşağıda gördüyünüz `$group` stage-ində etmişəm:

```python
{
   "$group": {
      "_id": "$_id.branch_name",
      "services": {
         "$push": {
               "service_name": "$_id.service_name",
               "score": "$score",
               
               "ones": "$ones",
               "twos": "$twos",
               "threes": "$threes",
               "fours": "$fours",
               "fives": "$fives",

               "total": "$total_count",

         }
      }
   }
}
```

Buradaki `$group` özündən əvvəlki stage-dən aşağıdakı strukturda input document-lər alır;
```python
{
   "_id": {
      "branch_name": "Branch 1",
      "service_name": "Customer service"
   },
   "ones": 1,
   "twos": 0,
   "threes": 0,
   "fours": 0,
   "fives": 0,
   "total_count": 1,
   "weighted_sum": 10,
   "score": 100
},
{
   "_id": {
      "branch_name": "Branch 1",
      "service_name": "Marketing service"
   },
   "ones": 1,
   "twos": 0,
   "threes": 0,
   "fours": 0,
   "fives": 0,
   "total_count": 1,
   "weighted_sum": 10,
   "score": 100
},
```   
və bu 2 documentləri branch_name-ə görə qruplayır, $push ilə service_name-ləri array halında toplayır. Aşağıdakı formatda document-ləri qaytarır:
```python
{
   "_id": "Branch 1",
   "services": [
      {
         "service_name": "Marketing service",
         "score": 25,
         "ones": 1,
         "twos": 0,
         "threes": 0,
         "fours": 1,
         "fives": 0,
         "total": 2
      },
      {
         "service_name": "Customer Service",
         "score": 0,
         "ones": 2,
         "twos": 1,
         "threes": 0,
         "fours": 3,
         "fives": 1,
         "total": 7
      },
   ]
}
```

[Pipeline-2](https://github.com/konulmammadova/qmeter_task/blob/4575138823dcee73e88fcdf3e68a762715efa148/qmeter/client.py#L99)-də **sonuncu stage** olan  `$project `-də **table-da göstərməyə uyğun formatda olan output document-ləri** əldə edirəm:
```python
{
   "branch_name": "ios test",
   "services": [
      {
         "service_name": "Speed of service",
         "score": 25,
         "ones": 1,
         "twos": 0,
         "threes": 0,
         "fours": 1,
         "fives": 0,
         "total": 2
      },
      {
         "service_name": "Marketing Service",
         "score": 0,
         "ones": 2,
         "twos": 1,
         "threes": 0,
         "fours": 3,
         "fives": 1,
         "total": 7
      },
   ],
}
```




    