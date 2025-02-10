# AI Tools Platform

A comprehensive platform for hosting and managing AI tools powered by Hugging Face.

## Features
- User authentication and membership management
- Integration with Hugging Face models
- Rate limiting for API calls
- Tool status monitoring
- Admin dashboard for tool management
- Membership tiers with different access levels

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
DATABASE_URL=postgresql://user:password@localhost/db_name
REDIS_URL=redis://localhost
SECRET_KEY=your-secret-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Deployment on Vercel

### Prerequisites
1. A GitHub account
2. A Vercel account (sign up at vercel.com)
3. A Hugging Face account with API access

### Deployment Steps

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

2. Connect to Vercel:
- Go to [Vercel Dashboard](https://vercel.com/dashboard)
- Click "New Project"
- Import your GitHub repository
- Configure the project:
  - Framework Preset: Next.js
  - Root Directory: ./frontend
  - Build Command: `npm run build`
  - Output Directory: .next

3. Add Environment Variables in Vercel:
```
NEXT_PUBLIC_API_URL=your-api-url
HUGGINGFACE_API_KEY=your-api-key
DATABASE_URL=your-database-url
JWT_SECRET=your-jwt-secret
```

4. Deploy:
- Click "Deploy"
- Vercel will automatically build and deploy your application

### Development

1. Frontend Development:
```bash
cd frontend
npm install
npm run dev
```

2. API Development:
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn index:app --reload
```

### Project Structure
```
.
├── api/                 # Backend API (Python/FastAPI)
│   ├── app/            # Application code
│   ├── requirements.txt
│   └── index.py        # Entry point for Vercel
├── frontend/           # Frontend (Next.js)
│   ├── components/
│   ├── pages/
│   └── package.json
├── vercel.json         # Vercel configuration
└── README.md
```

## Project Structure
```
.
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── alembic/
├── frontend/
├── requirements.txt
└── README.md
```
