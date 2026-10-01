# Classory

A classroom management application built with Django and Tailwind CSS.

## Tech Stack

- **Backend:** Django 6.1
- **Frontend:** Django Templates + Tailwind CSS (CDN)
- **Database:** None yet — UI only with mock data
- **Theme:** Blue & Yellow

## Project Structure

```
classory/
├── manage.py
├── classory/              # Project config (settings, urls, wsgi, asgi)
├── accounts/              # Auth app
│   ├── views.py           # login, register, profile setup views
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html         # Homepage — split-screen login
│       ├── register.html      # Register with student/teacher role picker
│       └── profile_setup.html # Role-aware profile form
├── classrooms/            # Classroom app
│   ├── views.py           # dashboard, create, classroom home (mock data)
│   ├── urls.py
│   └── templates/classrooms/
│       ├── dashboard.html         # Grid of classroom cards
│       ├── create_classroom.html  # 3-step wizard with Excel upload
│       ├── classroom_home.html    # Same UI for student & teacher
│       ├── upload_scores.html     # Teacher Excel upload
│       ├── upload_done.html       # Success notification
│       └── student_scores.html    # Student scores view
└── templates/base.html    # Tailwind CDN + blue/yellow theme config
```

## Getting Started

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

Open `http://localhost:8000` — you'll land on the login screen.

## User Flow

| Step | What happens |
|------|-------------|
| **`/`** | Renders the **login screen** (split-screen with branding) |
| **Login → "Create one"** | Goes to **register** with a student/teacher role selector |
| **Register → Continue** | **Profile setup** — students get name + section + student ID fields; teachers get name + department |
| **Profile → Submit** | Teachers → **create classroom** (name, description, subject, grade level + Excel import zone). Students → **dashboard** |
| **Dashboard** | Card grid of classrooms — clicking one enters the **classroom home** |
| **Classroom home** | Test card + teacher upload link |
| **Teacher: Upload Scores** | Upload Excel → success notification → back to classroom |
| **Student: Test card** | View own scores only |

---

## Data Flow Diagram

### Context Diagram (Level 0)

```
┌─────────────────────────────────────────────────────────┐
│                      EXTERNAL                           │
│                                                         │
│   ┌──────────┐                              ┌────────┐  │
│   │  Student │                              │Teacher │  │
│   └────┬─────┘                              └───┬────┘  │
│        │                                        │       │
└────────┼────────────────────────────────────────┼───────┘
         │                                        │
         ▼                                        ▼
┌─────────────────────────────────────────────────────────┐
│                    CLASSORY SYSTEM                      │
│                                                         │
│   [Login] → [Register] → [Profile Setup] → [Dashboard]  │
│                                                         │
│   [Classroom Home] ←→ [Upload Scores] ←→ [Scores]       │
│                                                         │
│              ┌──────────────────┐                       │
│              │   Mock Data      │                       │
│              │  (No Database)   │                       │
│              └──────────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

### Level 1 DFD — Detailed Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLASSORY                                        │
│                                                                             │
│  ┌─────────┐    POST     ┌──────────────┐    redirect    ┌──────────────┐  │
│  │  User   │────────────▶│  Login View  │───────────────▶│  Dashboard   │  │
│  └─────────┘             └──────────────┘                └──────┬───────┘  │
│       │                                                         │          │
│       │ GET /register/                                          │ renders  │
│       ▼                                                         ▼          │
│  ┌──────────────┐    GET    ┌──────────────┐    GET    ┌──────────────┐  │
│  │  Register    │──────────▶│   Profile    │──────────▶│  Classroom   │  │
│  │    View      │           │    Setup     │           │    Cards     │  │
│  └──────────────┘           └──────┬───────┘           └──────┬───────┘  │
│                                    │                          │          │
│                          role=student│         role=teacher    │          │
│                                    ▼                          ▼          │
│                           ┌──────────────┐           ┌──────────────┐   │
│                           │  Dashboard   │           │   Create     │   │
│                           │              │           │  Classroom   │   │
│                           └──────┬───────┘           └──────┬───────┘   │
│                                  │                          │           │
│                                  │  click card              │ submit    │
│                                  ▼                          ▼           │
│                           ┌──────────────┐           ┌──────────────┐   │
│                           │  Classroom   │           │  Dashboard   │   │
│                           │    Home      │           │  (redirect)  │   │
│                           └──────┬───────┘           └──────────────┘   │
│                                  │                                      │
│                    ┌─────────────┼─────────────┐                        │
│                    │             │             │                        │
│                    ▼             ▼             ▼                        │
│            ┌──────────────┐ ┌──────────┐ ┌──────────────┐              │
│            │   Upload     │ │  Test    │ │   Student    │              │
│            │   Scores     │ │  Card    │ │   Scores     │              │
│            │   (Teacher)  │ │          │ │   (Student)  │              │
│            └──────┬───────┘ └────┬─────┘ └──────┬───────┘              │
│                   │              │              │                       │
│                   │ POST         │ click        │ click                 │
│                   ▼              │              │                       │
│            ┌──────────────┐      │              │                       │
│            │   Upload     │      │              │                       │
│            │    Done      │      │              │                       │
│            │  (success)   │      │              │                       │
│            └──────┬───────┘      │              │                       │
│                   │              │              │                       │
│                   │ redirect     │              │                       │
│                   ▼              │              │                       │
│            ┌──────────────┐      │              │                       │
│            │  Classroom   │◀─────┴──────────────┘                       │
│            │    Home      │                                             │
│            └──────────────┘                                             │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                         MOCK DATA STORE                            │  │
│  │                                                                    │  │
│  │  MOCK_CLASSROOMS ──▶ Dashboard, Classroom Home                     │  │
│  │  MOCK_STUDENT_SCORES ──▶ Student Scores                            │  │
│  │                                                                    │  │
│  │  (No database — data lives in views.py as Python dicts)            │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Sequences

#### 1. Login Flow
```
User ──POST /login/──▶ Login View ──redirect──▶ Dashboard
                                         │
                                         ▼
                                   Mock Classrooms
                                   (rendered as cards)
```

#### 2. Registration Flow
```
User ──GET /register/──▶ Register View
                              │
                              ▼
                        Profile Setup
                              │
                    ┌─────────┴─────────┐
                    │                   │
              role=student        role=teacher
                    │                   │
                    ▼                   ▼
              Dashboard          Create Classroom
```

#### 3. Teacher Upload Flow
```
Teacher ──click "Upload Scores"──▶ Upload Scores View
                                         │
                                         ▼
                                   Fill form +
                                   select Excel
                                         │
                                         ▼
                                   POST submit
                                         │
                                         ▼
                                   Upload Done View
                                   (success message)
                                         │
                                         ▼
                                   redirect ──▶ Classroom Home
```

#### 4. Student Scores Flow
```
Student ──click "Test" card──▶ Student Scores View
                                     │
                                     ▼
                               Mock Student Scores
                               (only their own data)
                                     │
                                     ▼
                               Scores Table
                               (name, section,
                                test, score, date)
```

### Key Data Points

| Data | Source | Destination | Storage |
|------|--------|-------------|---------|
| Classroom list | `MOCK_CLASSROOMS` | Dashboard, Classroom Home | Python dict in `views.py` |
| Student scores | `MOCK_STUDENT_SCORES` | Student Scores page | Python dict in `views.py` |
| Uploaded Excel | Teacher's file | Upload Done (success) | **Not stored** — UI only |
| User role | Register form | Profile Setup | **Not stored** — UI only |

> **Note:** Since this is UI-only with no models, all "data" is mock data hardcoded in `views.py`. The Excel upload doesn't actually parse or store anything yet — it just shows a success notification. When you add models later, the mock data will be replaced with real database queries.

---

## User Stories

### Authentication

- [ ] As a user, I want to see a login screen when I visit the homepage
- [ ] As a user, I want to navigate to the registration page from the login screen
- [ ] As a user, I want to register as a student or teacher
- [ ] As a user, I want to be redirected to the dashboard after logging in

### Student Stories

- [ ] As a student, I want to set up my profile with my first name, last name, section, and student ID after registering
- [ ] As a student, I want to see all classrooms I'm part of on the dashboard
- [ ] As a student, I want to click on a classroom to enter it
- [ ] As a student, I want to click the Test card to view my scores
- [ ] As a student, I want to see only my own scores (not other students' scores)
- [ ] As a student, I want to see my name, section, and a table of my test scores

### Teacher Stories

- [ ] As a teacher, I want to set up my profile with my first name, last name, and department after registering
- [ ] As a teacher, I want to be prompted to create a classroom after registration
- [ ] As a teacher, I want to create a classroom with a name, description, subject, and grade level
- [ ] As a teacher, I want to import students from an Excel file when creating a classroom
- [ ] As a teacher, I want to see all classrooms I'm part of on the dashboard
- [ ] As a teacher, I want to click on a classroom to enter it
- [ ] As a teacher, I want to upload test scores via an Excel file
- [ ] As a teacher, I want to see a success notification after uploading scores
- [ ] As a teacher, I want to be redirected back to the classroom after uploading

### General

- [ ] As a user, I want a beautiful blue and yellow themed UI
- [ ] As a user, I want consistent navigation across all pages
- [ ] As a user, I want to log out and return to the login screen

---

## Future Enhancements

- [ ] Add Django models (User, Classroom, Student, Test, Score)
- [ ] Implement real authentication with Django's auth system
- [ ] Parse uploaded Excel files with `openpyxl` or `pandas`
- [ ] Add real database queries replacing mock data
- [ ] Add student enrollment via classroom codes
- [ ] Add grade computation and analytics
- [ ] Add email notifications
# classory
# classory
