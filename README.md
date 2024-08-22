# Oxumadan keçməyin

## Proyektin quraşdırılması

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
Dockeri qaldırdıqdan dərhal sonra test databazası üçün aşağıdakı kommandı icra edin:

```bash
docker exec -it qm-feedback-app python /app/restore_db.py
```

## Proyektdə nələr edilib:
- MongoDB və Django proyekti üçün **Dockerfile** və **docker-compose** faylları uyğun formada yazılaraq proyekt *dockerize* edilib.
- Tapışırıqda istənilən table-ın göstərilməsi üçün 2 alternativ yoldan istifadə edilib:
    1. İstənilən qruplaşdırma və hesablamalar, yəni; 
       ```bash
       100 * ( birlərin sayı * 10 + ikilərin sayı * 5 + üçlərin sayı * 0 + dördlərin sayı * -5 + beşlərin sayı * -10 ) / (bir + iki + üç+ dörd + beşlərin sayı ) * 10
       ```
