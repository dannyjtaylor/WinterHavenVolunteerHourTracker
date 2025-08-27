# Volunteer Hour Tracker

This project is a web application built with Flask for tracking volunteer hours. It allows users to add volunteer hours and view a summary of all volunteers and their total hours as they volunteer at Winter Haven.

## Project Structure

```
volunteer-hour-tracker
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── main.js
│   └── templates
│       ├── base.html
│       ├── index.html
│       └── dashboard.html
├── instance
│   └── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd volunteer-hour-tracker
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

5. **Configure the application:**
   Update the `instance/config.py` file with your database URI and any other necessary configurations.

6. **Run the application:**
   ```
   python run.py
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- On the landing page, you can view the list of volunteers and their total hours.
- Use the form to add new volunteer hours.
- The application will automatically update the displayed data.

## Future Enhancements

- Additional dashboard functionality can be implemented in `app/templates/dashboard.html`.
- Consider adding user authentication for better data management.