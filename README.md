# Email Automation Software for SMEs

## Overview

This software is a SaaS (Software as a Service) application designed to help small and medium-sized enterprises (SMEs) manage their invoicing processes efficiently. It enables users to create, update, delete, and download invoices in PDF format. Additionally, it automates the process of sending email reminders to customers about upcoming invoice payments, ensuring timely payments and reducing the burden on the accounting department.

## Features

- **Invoice Management**:
  - Create new invoices.
  - Update existing invoices.
  - Delete invoices.
  - Download invoices as PDF files.

- **Email Automation**:
  - Sends reminder emails to unpaid customers 7 days, 5 days, 3 days, and 1 day before the due date.
  - If the invoice remains unpaid after the due date, it sends daily reminders until the payment is made.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL
- An email service provider (e.g., SendGrid, Mailgun)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/email-automation-software.git
   cd email-automation-software
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**:
   Update the `DATABASES` setting in `settings.py` to match your PostgreSQL configuration.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Configure Email Service**:
   Add your email service provider's configuration details to the `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` settings in `settings.py`.

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

9. **Set up celery and Redis**:
    Check settings file for configuration details
    ```bash - Run 2 terminal windows
    Terminal 1: celery -A project_name worker --loglevel=info
    Terminal 2: celery -A project_name beat --loglevel=info
    ```

## Usage

### Invoice Management

- **Create Invoice**:
  Navigate to the invoices section in the dashboard and click on "Create New Invoice." Fill in the necessary details and save.

- **Update Invoice**:
  Click on the invoice you wish to update, make the necessary changes, and save.

- **Delete Invoice**:
  Select the invoice you want to delete and click on the "Delete" button.

- **Download Invoice**:
  Click on the "Download" button next to the invoice you wish to download. The invoice will be saved as a PDF on your local computer.

### Email Reminders

The system automatically sends email reminders to customers with unpaid invoices as follows:
- 7 days before the due date.
- 5 days before the due date.
- 3 days before the due date.
- 1 day before the due date.
- Daily reminders after the due date until the invoice is paid.

## Contributing

We welcome contributions to enhance the functionality of this software. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact us at [team-payprompter@outlook.com](mailto:team-payprompter@outlook.com).

---