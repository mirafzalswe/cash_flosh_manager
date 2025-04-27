пш# Cash Flow Manager

A comprehensive Django-based web application for managing personal and business finances. The application allows users to track income and expenses, categorize transactions, and generate financial reports.

## Features

- **Transaction Management**
  - Create, edit, and delete transactions
  - Categorize transactions by status, type, category, and subcategory
  - Track income and expenses with detailed categorization
  - Add comments and notes to transactions

- **Directory Management**
  - Manage transaction statuses (e.g., Business, Personal, Taxes)
  - Configure transaction types (Income/Expense)
  - Organize categories and subcategories
  - Safe deletion with dependency handling

- **Financial Overview**
  - View total balance
  - Track monthly income and expenses
  - Analyze transactions by period
  - Visual representation of financial data

- **User Interface**
  - Clean and intuitive design
  - Responsive layout for all devices
  - Bootstrap-based styling
  - Interactive tooltips and alerts

## Technical Stack

- **Backend**
  - Django 4.x
  - Python 3.x
  - PostgreSQL (recommended) or SQLite

- **Frontend**
  - HTML5
  - CSS3
  - Bootstrap 5
  - Font Awesome icons
  - JavaScript (vanilla)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cash_flow_manager.git
   cd cash_flow_manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - For SQLite (default):
     ```bash
     python manage.py migrate
     ```
   - For PostgreSQL:
     - Create a database
     - Update DATABASES in settings.py
     - Run migrations

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
cash_flow_manager/
├── core/                    # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   └── urls.py             # URL routing
├── static/                  # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── img/                # Images
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies
```

## Models

- **Transaction**
  - Date, amount, comment
  - Foreign keys to Status, TransactionType, Category, Subcategory

- **Status**
  - Name (e.g., Business, Personal)

- **TransactionType**
  - Name (e.g., Income, Expense)
  - is_income flag

- **Category**
  - Name
  - Relation to TransactionType

- **Subcategory**
  - Name
  - Relation to Category

## Usage

1. **Access the Application**
   - Open your browser and navigate to `http://localhost:8000`
   - Log in with your superuser credentials

2. **Manage Directories**
   - Navigate to "Directories" to manage:
     - Statuses
     - Transaction Types
     - Categories
     - Subcategories

3. **Create Transactions**
   - Go to "Transactions"
   - Click "Add Transaction"
   - Fill in the details:
     - Date
     - Amount
     - Status
     - Type
     - Category
     - Subcategory
     - Optional comment

4. **View Reports**
   - Check the dashboard for:
     - Current balance
     - Monthly income/expenses
     - Recent transactions

## Security Features

- User authentication
- Protected routes
- Safe deletion with dependency handling
- Input validation
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Django Framework
- Bootstrap
- Font Awesome
- All contributors and users 