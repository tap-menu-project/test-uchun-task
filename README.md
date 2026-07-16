# Library API

Kutubxona kitob ijarasi uchun REST API: kitoblar katalogi, ijaraga
berish/qaytarish, band nusxalarni hisobga olish va background xabarnomalar.

**Stack:** Django 5.1 · DRF · PostgreSQL 16 · Celery + Redis · Docker

## Ishga tushirish

1. Repozitoriyni klonlash:
   ```git clone repo-url```
2. `.env` yaratish (namuna: `.env.example`):
   ```cp .env.example .env```
3. Ko'tarish:
   docker compose up --build
4. Migratsiyalar:
   docker compose exec web python manage.py migrate

API: http://localhost:8000/api/v1/

## Endpoint'lar

| Metod | URL | Tavsif |
|---|---|---|
| GET | /api/v1/authors/ | Authorlar |
| POST | /api/v1/authors/ | Author qo'shish |
| GET | /api/v1/books/ | Kitoblar (muallif bilan) |
| POST | /api/v1/books/ | Kitob qo'shish |
| GET | /api/v1/books/?author=1 | Muallif bo'yicha filter |
| POST | /api/v1/borrowings/ | Ijaraga olish |
| POST | /api/v1/borrowings/{id}/return_book/ | Qaytarish |
| GET | /api/v1/borrowings/?active=true | Faol ijaralar |

### Namuna: ijara yaratish
so'rov tanasi + muvaffaqiyatli javob + 400 javob (nusxa qolmaganda)
— Postman'dagi REAL natijalaringizdan ko'chiring

## Arxitektura qarorlari

- **PROTECT on_delete:** sababi author o'chirilayotgan paytda uning books
borligi tekshiriladi agar bor bo'lsa o'chirishga ruxsatni toxtatadi. borrowing ham shunday agar book o'chib ketsa borrowing ham o'chib ketadi
va loglar butunlay yo'q bo'ladi.
- **Race condition:** transaction.atomic + select_for_update; curl bilan
paralel 2 ta sorov yuborib 1 ta qolgan kitobni olishga urindim. avvaliga transaction.atomic siz 2 marta olindi, kegin himoyani qo'yganimdan kegin 
birinchi odamga nasib qildi. transaction.atomic aynan shunday jarayonlarda
foydali bo'ladi.
- **Celery:** .delay() - sababi oddiy unday holatda sinxron bo'lib qolar edi, hozirgi delay() dan kegin esa jarayon muvofavqiyatli yakunlangandan
kegin yuboriladi.
- **Email o'rniga log:** sababi bizdagi talabda yuborish so'ralgan ammo
emailga so'ralmagan va hattoki borrow olgan user ham FK emas oddiy charfield. kelajakda uni email orqali oladigan qilsa bo'ladi.
- **Beat:** muddati o'tganlarni kunlik loglash, schedule tanlovi

## Keyingi qadamlar (production uchun)

- Auth (JWT) + borrower → User FK
- gunicorn + non-root container user
- Testlar (pytest)