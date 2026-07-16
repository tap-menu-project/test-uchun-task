# Kutubxona API — ish rejasi (~6 soat)

## 1-blok: Skelet (≈1 soat)  
- [*] Papka, venv, git init, .gitignore  
- [*] requirements.txt (django, drf, celery, redis, psycopg2-binary, python-dotenv)  
- [*] Dockerfile + docker-compose.yml (web, db, redis, worker) + .env  
- [*] Django loyiha + library app, settings .env'dan o'qiydi  
- [*] ✅ Tekshiruv: `docker-compose up` → Django sahifasi ochiladi, db ulandi

## 2-blok: Book zanjiri (≈1 soat)  
- [*] Draw.io: 3 model sxemasi (10 daqiqadan oshmasin!)  
- [*] Author + Book modellari, migration, admin.register  
- [*] BookSerializer (author nested/ko'rinadigan), AuthorSerializer  
- [*] BookViewSet + router, queryset'da select_related('author')  ← N+1!  
- [*] ?author=<id> filter  
- [*] ✅ Tekshiruv: GET/POST /api/books/ Postman'da ishlaydi

## 3-blok: Borrowing zanjiri + BIZNES-QOIDALAR (≈2 soat — eng muhim blok!)  
- [*] Borrowing modeli, migration, admin  
- [*] POST /api/borrowings/ — yaratish:  
      - [*] transaction.atomic + select_for_update(kitob qatoriga)  ← race condition!  
      - [*] available_copies == 0 → 400 + xabar  
      - [*] muvaffaqiyatda available_copies -= 1  
- [*] POST /borrowings/<id>/return/ (custom action):  
      - [*] allaqachon qaytarilgan bo'lsa → 400  
      - [*] returned_at = now, available_copies += 1 (atomic!)  
- [*] ?active=true filter  
- [*] ✅ Tekshiruv: oxirgi nusxani 2 ta parallel so'rov bilan olishga urinish — bittasi 400 olsin

## 4-blok: Celery (≈1 soat)  
- [*] celery.py sozlash, worker docker-compose'da ishlaydi  
- [*] send_confirmation_email task (log/print), ijara yaratilganda .delay()  
- [*] ✅ Tekshiruv: worker logida xabar ko'rinadi  
- [*] Bonus (vaqt qolsa): Beat + muddati o'tganlarni loglash

## 5-blok: Pardoz va topshirish (≈1 soat)  
- [ ] README: o'rnatish, docker-compose up, endpoint'lar jadvali + curl misollar  
- [ ] Hamma endpoint'ni boshidan qo'lda bir aylanib chiqish  
- [ ] Kod tozalash: o'lik kod, print'lar, izohsiz joylar  
- [ ] Oxirgi commit + push

## Vaqt qolsa (ixtiyoriy)  
- [ ] Celery Beat bonus / prod-dev settings / 2-3 ta oddiy test  
