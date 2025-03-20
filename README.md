# Budgetan - Student Budgeting Application

## Overview
Budgetan is a specialized budgeting application designed specifically for students to manage their monthly finances effectively. This application provides intuitive tools and features to help students track their expenses, set budgets, and make informed financial decisions throughout their academic journey.

## Features
- Monthly budget planning and tracking
- Expense categorization
- Student-specific expense categories (textbooks, supplies, meal plans, etc.)

## Technical Stack
- Backend: Python Flask
- Database: SQLAlchemy with SQLite
- Authentication: JWT (JSON Web Tokens)

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/maretrodep/BudgetanBackend.git
cd BudgetanBackend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration Setup

1. Copy the sample configuration file:
```bash
cp config.py.sample config.py
```

2. Edit `config.py` with your specific settings:
   - Set your `SECRET_KEY`
   - Configure database URL
   - Set JWT secret key
   - Configure other environment-specific settings
   - Enviroment variables can be used instead

## Running the Application

```bash
cd backend
flask run
```
The application will be available at `http://localhost:5000`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the GNU General Public License version 2 (GPL-2.0) - see the LICENSE file for details.

