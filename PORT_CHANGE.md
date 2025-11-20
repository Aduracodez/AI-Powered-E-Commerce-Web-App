# Port Configuration Changed

## New Port Configuration

### Frontend
- **Old Port:** 3000
- **New Port:** 3001
- **URL:** http://localhost:3001

### Backend (Django)
- **Old Port:** 8000
- **New Port:** 8001
- **URL:** http://localhost:8001

## How to Start

### Start Backend (Terminal 1)
```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8001
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

Frontend will automatically start on port 3001.

## Access Your Store

Open browser: **http://localhost:3001**

## Files Updated

✅ All frontend API calls updated to use port 8001
✅ Frontend configured to run on port 3001
✅ CORS settings updated to allow port 3001

## Verification

Test API:
```bash
curl http://localhost:8001/api/products/
```

Should return JSON with 50 products.

