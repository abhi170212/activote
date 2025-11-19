# ACti VOTE - Online Voting System

A Django-based web application that provides a secure and user-friendly online voting platform. The system allows users to register, view candidates, cast votes, and view results. Administrators have access to detailed dashboards with voting statistics and data export capabilities.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Admin Features](#admin-features)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Features

### User Features

- **User Registration and Authentication**: Secure user registration with Django's UserCreationForm and login/logout functionality
- **Voting Interface**: View candidate profiles and manifestos, cast votes for preferred candidates
- **Results Display**: Real-time vote counting with percentage-based results visualization
- **Voter Information**: Access voter guides, security information, privacy policy, and terms of service

### Admin Features

- **Admin Dashboard**: Comprehensive voting statistics with visual data representation using Chart.js
- **Data Export**: Export voting data to Excel and CSV formats
- **Detailed Analytics**: Monitor voting activity and track individual votes

## Technologies Used

- **Backend**: Django 5.2.5 (Python 3.13.9)
- **Frontend**: HTML, CSS, JavaScript with Chart.js for data visualization
- **Database**: SQLite3
- **Authentication**: Django's built-in User model and authentication system

## Project Structure

```
django-final/
├── voting/                 # Main voting application
│   ├── models.py          # Data models (Candidate, Vote)
│   ├── views.py           # Application logic
│   ├── urls.py            # URL routing
│   └── templates/         # HTML templates
├── voting_system/         # Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI deployment
├── static/                # CSS and JavaScript files
├── templates/             # Base HTML templates
└── manage.py             # Django management script
```

## Prerequisites

- Python 3.13.9
- Django 5.2.5
- pip (Python package installer)

## Installation

1. Clone or download the project repository

2. Navigate to the project directory:
   ```bash
   cd django-final
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up your admin username, email, and password.

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`

## Usage

### For Regular Users

1. **Registration**: Visit `http://127.0.0.1:8000/register/` to create an account
2. **Login**: Use your credentials at `http://127.0.0.1:8000/login/` to access the system
3. **Voting**: Navigate to the voting page to view candidates and cast votes
4. **Results**: View personal voting results after casting a vote

### For Administrators

1. **Login**: Use superuser credentials to log in
2. **Dashboard**: Access the admin dashboard by clicking on "Admin Dashboard" in the navigation menu
3. **Monitor**: View real-time voting statistics and charts
4. **Export**: Download voting data using the export buttons (Excel/CSV)

## Admin Features

The admin dashboard provides comprehensive tools for monitoring the voting process:

- **Voting Statistics**: Real-time overview of total votes and candidate performance
- **Data Visualization**: Interactive charts showing voting distribution
- **Detailed Results**: Tabular view of candidate votes and percentages
- **Voter Details**: Information about individual voters and their choices
- **Data Export**: Export all voting data to Excel or CSV formats

To access admin features, a user must have the `is_superuser` flag set to `True`.

## Data Models

### Candidate Model

- **name**: Character field (max 100 characters)
- **party**: Character field (max 100 characters)
- **image_url**: URL field for candidate photos
- **manifesto**: Text field for candidate statements

### Vote Model

- **candidate**: Foreign key to Candidate model
- **user**: Foreign key to Django User model
- **timestamp**: DateTime field (auto-generated)
- **Unique constraint**: One vote per user per candidate

## API Endpoints

| URL | View Function | Description |
|-----|---------------|-------------|
| `/` | home | Homepage |
| `/register/` | register | User registration |
| `/vote/` | vote_view | Voting interface |
| `/vote/results/` | vote_results | Voting results |
| `/candidates/` | candidates | Candidate listing |
| `/candidates/vote/<int:candidate_id>/` | cast_vote | Cast vote for candidate |
| `/manifesto/<int:candidate_id>/` | manifesto | View candidate manifesto |
| `/admin-dashboard/` | admin_dashboard | Admin statistics dashboard |
| `/admin-results/` | admin_results | Detailed admin results |
| `/export-votes/` | export_votes_to_excel | Export data to Excel |
| `/export-detailed-votes/` | export_detailed_votes_to_csv | Export detailed data to CSV |

## Security

The application implements several security measures:

- Django's built-in authentication system
- CSRF protection on forms
- Password validation and security
- Secure session management
- Data encryption for sensitive information

## Contributing

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull 
