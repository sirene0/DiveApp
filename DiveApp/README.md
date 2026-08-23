# DiveApp
🤿 RinaDive — Dive Management API

A Django REST API for scuba diving management, featuring a full implementation of the Bühlmann ZHL-16C decompression algorithm for safe dive planning.

📋 Description

RinaDive is a backend API that allows scuba divers to plan, track, and analyze their dives. The application automatically calculates decompression stops based on depth, duration, and gas mixture using the Bühlmann ZHL-16C algorithm, and generates safety alerts based on the diver's certification level.

🛠️ Technologies
Layer	Technology
Backend	Python 3.x / Django
API	Django REST Framework
Database	SQLite (development) / PostgreSQL (production)
Frontend	React / TypeScript (in progress)
Auth	Manual JWT (SHA-256 + salt)
Algorithm	Bühlmann ZHL-16C
⚙️ Installation
bash
# 1. Clone the repository
git clone https://github.com/sirene0/DiveApp.git
cd DiveApp/DiveApp

# 2. Create a virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 3. Install dependencies
pip install django djangorestframework

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
📁 Project Structure
DiveApp/
├── alerts/               # Safety alerts system
│   ├── models.py         # Alert model (INFO / WARNING / DANGER)
│   └── serializers.py
├── decompression/        # Decompression planning
│   ├── models.py         # DecompressionModel (stops)
│   └── serializers.py
├── dives/                # Dive management
│   ├── models.py         # Dive model (depth, duration, status...)
│   └── serializers.py
├── gases/                # Gas mixtures
│   ├── models.py         # GasMixture (O2 / N2 percentages)
│   └── serializers.py
├── users/                # User management
│   ├── models.py         # User model (certification P1/P2/P3)
│   └── serializers.py
├── services/             # Business logic layer
│   ├── gas_service.py
│   ├── dive_service.py
│   ├── user_service.py
│   ├── alert_service.py
│   └── decompression_service.py
└── manage.py
🔑 User Certification Levels
Level	Max Depth
P1	20 m
P2	40 m
P3	60 m
🌊 Dive Status Flow
PLANNED → IN_PROGRESS → COMPLETED
                      ↘ CANCELLED
🫧 Bühlmann ZHL-16C Algorithm

RinaDive implements the Bühlmann ZHL-16C decompression model, the industry standard used in professional dive computers.

How it works

The human body is modeled as 16 tissue compartments, each absorbing nitrogen at a different rate.

Compartment  Half-time (min)  M-value (bar)
    1              4.0             3.3
    2              8.0             2.8
    3             12.5             2.4
   ...             ...             ...
   16            635.0             1.2
Formula

For each compartment, nitrogen absorption is calculated as:

P_final = P_initial + (P_inspired - P_initial) × (1 - 2^(-t / t½))

Where:
  P_initial  = N2 pressure in tissue at surface (0.79 bar)
  P_inspired = ambient pressure × N2 fraction
  t          = dive duration (minutes)
  t½         = compartment half-time
Decompression Stop Calculation
1. Calculate N2 load for all 16 compartments
2. If any compartment P_final > M-value → decompression required
3. Ascent by 3m steps from max depth to surface
4. At each depth, wait until all compartments are safe
5. Generate the stop plan
Safety Checks
✅ Depth limit per certification level
✅ Maximum dive duration (60 min without decompression)
✅ Maximum ascent speed (9 m/min)
📡 API Endpoints (coming soon)
Method	Endpoint	Description
POST	/api/users/register/	Register a new diver
POST	/api/users/login/	Login
GET	/api/dives/	List all dives
POST	/api/dives/	Create a dive
POST	/api/dives/{id}/start/	Start a dive
POST	/api/dives/{id}/finish/	Finish a dive
GET	/api/dives/{id}/decompression/	Get decompression plan
GET	/api/gases/	List gas mixtures
GET	/api/dives/{id}/alerts/	List dive alerts
👤 Author

Rina
GitHub: @sirene0

📌 Project Status
✅ Models & Migrations
✅ Service Layer (business logic)
✅ Bühlmann ZHL-16C Algorithm
✅ Serializers
🔄 Views & URLs       ← in progress
⬜ Frontend React/TypeScript
