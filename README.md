# Library API

Kutubxona kitob ijarasi uchun REST API: kitoblar katalogi, ijaraga
berish/qaytarish, band nusxalarni hisobga olish va background xabarnomalar.

**Stack:** Django 5.1 · DRF · PostgreSQL 16 · Celery + Redis · Docker

## Ishga tushirish

1. Repozitoriyni klonlash:
   ...
2. `.env` yaratish (namuna: `.env.example`):
   ...
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
| POST | /api/v1/borrowings/{id}/return/ | Qaytarish |
| GET | /api/v1/borrowings/?active=true | Faol ijaralar |

### Namuna: ijara yaratish
so'rov tanasi + muvaffaqiyatli javob + 400 javob (nusxa qolmaganda)
— Postman'dagi REAL natijalaringizdan ko'chiring

## Arxitektura qarorlari

- **PROTECT on_delete:** ...(nega — bir jumla)
- **Race condition:** transaction.atomic + select_for_update; qanday
  test qilingani (parallel curl) — 2-3 jumla
- **Celery:** .delay() nima uchun atomic blokdan keyin — 1-2 jumla
- **Email o'rniga log:** talabdagi ziddiyat va tanlov izohi
- **Beat:** muddati o'tganlarni kunlik loglash, schedule tanlovi

## Keyingi qadamlar (production uchun)

- Auth (JWT) + borrower → User FK
- gunicorn + non-root container user
- Testlar (pytest)