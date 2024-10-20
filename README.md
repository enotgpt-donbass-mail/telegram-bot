﻿# Mail Booking Bot — чат-бот для бронирования места в электронной очереди

Чат-бот позволяет пользователю удаленно бронировать и управлять своими заявками электронной очереди. 

## Возможности бота: 
- **Авторизация**. Пользователь должен отсканировать QR-код в одном из отделений "Почты Донбасса", после чего ему будет выдан доступ _(в коде предусмотрен режим авторизации по Email)_
- **Поиск отделения**. Пользователь может найти ближайшее отделение по геолокации / найти ближайшее отделение с нужной ему услугой / выбрать отделение по его почтовому индексу
- **Бронирование**. Пользователь может забронировать свободное окошко на отделении почты на ближайшую неделю. После полученного кода брони нужно подойти к терминалу и получить талон вне очереди
- **Напоминание**. За 1 час и потом за 15 минут до конца брони, пользователю будет выслано оповещение и том, что его место забронировано! 
- **Оценка**. В течение часа, после окончания обслуживания, клиенту придет оповещение с просьбой оценки сотрудника, который его обслуживал по 5 бальной шкале

## Стек:
- **Телеграм фреймворк**. Используется `aigoram`
- **База данных.** Локальная БД использует под капотом ORM `peweee` и `SqlLite`

## Запуск: 

Для разворачивания предусмотрен Docker-контейнер. Необходимые действия:

1. Создайте файл ".env" и заполните поля согласно его шаблону - ".env.template": 
2. Соберите образ: `docker build -t имя_образа:тег .`
3. Запустите собранный образ: `docker run -d имя_образа:тег`

## Тестовые данные окружения

> **TelegramToken** = 7635859181:AAGqEqITnh-cnGOiL4rIsHmOZN9xOWpSZG8


> **AuthToken** = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OCwicm9sZXMiOlsidXNlciJdLCJleHAiOjE3OTkzMjE3MzN9.FtlDFJG2r_2HcNjw9vmR7mgJplzVfmW3OHWekxJo7kw

### Тестирование

Бот расположен и доступен по ссылке: https://t.me/post_donbass_bookings_bot

Одноразовые коды для получения доступа (для теста) (которые генерируются в качестве QR на терминале):
1. https://t.me/post_donbass_bookings_bot?start=68218cbb-f32b-4c02-a3fa-2a115726ef2b__111111
2. https://t.me/post_donbass_bookings_bot?start=e98ce57d-b846-401b-a3cd-28558426c1ff__111111
3. https://t.me/post_donbass_bookings_bot?start=d26befea-24a2-4a56-8751-d6d8d829ecc8__111111
4. https://t.me/post_donbass_bookings_bot?start=66f21398-3ba6-47c3-b160-e122cace0c16__111111
5. https://t.me/post_donbass_bookings_bot?start=bb637cd6-1c18-4afd-af12-a81f68a87837__111111
6. https://t.me/post_donbass_bookings_bot?start=16eeb020-316d-4bf4-905a-3a449b8534cf__111111
7. https://t.me/post_donbass_bookings_bot?start=e0857328-a0f5-4df0-b5b5-72439bf5b1a2__111111
8. https://t.me/post_donbass_bookings_bot?start=a0f4fe70-1a45-4454-a6e6-3946b6aa834f__111111
9. https://t.me/post_donbass_bookings_bot?start=f9446c79-408b-4135-94ae-463f0902c40d__111111
10. https://t.me/post_donbass_bookings_bot?start=04678514-d27d-4f2d-b143-11fa39eb0fdc__111111

> Коды можно получать самостоятельно в качестве https://frontend.enotgpt.ru/terminal_talon по кнопке "Бронь по записи"
