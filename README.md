## Основная идея

Имеются два docker-контейнера, крутящихся на постоянной основе:
1) Раз в час обновляет погоду в каждом поддерживаемом городе;
2) Раз в сутки обновляет базу данных мероприятий, добавляя появившиеся за последние сутки.


Для контейнера с обновлением погоды: 

Из папки weather_api:

```commandline
docker build -t weather_scheduler .
docker run --env-file ../.env weather_scheduler
```

Для контейнера с обновлением мероприятий: 

Из папки event_api:

```commandline
docker build -t event_scheduler .
docker run event_scheduler
```
