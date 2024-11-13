# Sample Web and REST API Django Project

This is a Django-based web and REST API project that demonstrates the use of a D3.js chart after successful login and JWT-based authentication for secure data retrieval via REST API endpoints. The project focuses on functionality over design, utilizing a Cookiecutter-based folder structure and ensuring all required features are operational.

## Features

- **Web Application**: Upon successful login, renders a D3.js bar chart using sample data.
- **REST API**: Secure endpoints for user registration, token management, and data retrieval.
- **Swagger UI**: API documentation and testing interface to interact with endpoints.
- **JWT Authentication**: Secure access to API endpoints using JWT tokens.
- **Git workflows**: Making sure to use git to test all the functionality.
- **Test-Driven Development (TDD)**: Comprehensive tests to verify functionality and prevent regressions.

## Getting Started

### Prerequisites

- **Python**: Install `pyenv` and `pyenv-virtualenv` to manage Python versions and virtual environments.
- **Python Version**: Use Python 3.12 (or adjust to the version specified in the project).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/VineethKumar7/3IVIS_app
   cd DjangoD3ChartApp
   ```

2. **Set Up Python Environment**:
   ```bash
   pyenv install 3.12.7
   pyenv virtualenv 3.12.7 myenv
   pyenv activate myenv
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

### Usage

1. **Web Login**:
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
   - Admin 
      - **Email**: `admin@email.com`
      - **Password**: `admin`
   - Enter the sample credentials:
     - **Email**: `testuser@email.com`
     - **Password**: `testpassword`
   - After login, you will be redirected to a page displaying a D3.js bar chart.

2. **Customize Chart Data**:
   - The chart data is currently added using admin dashboard. Used admin credentials to add the data.
   - Alternative way is to save the data in CSV format with the fields like date,temperature in Celcius and Humidity in the code/data folder. And run this command.
   ```bash
   python manage.py load_september_weather_data
   ```
   - Modify this data to see changes reflected in the bar chart. Currently sqlLite is being used.

3. **API Testing with Swagger UI**:
   - Visit [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) to access the Swagger UI for API documentation and testing.
   - Follow the steps below to authenticate and access protected endpoints.

### API Endpoints

| Endpoint             | Method | Description                                         |
|----------------------|--------|-----------------------------------------------------|
| `/register/`         | POST   | Register a new user (requires email and password).  |
| `/token/`            | POST   | Obtain JWT tokens using credentials.                |
| `/token/refresh/`    | POST   | Refresh the JWT access token.                       |
| `/data/`             | GET    | Retrieve chart data (requires JWT authentication).  |

### Authentication Workflow in Swagger UI

To access protected API endpoints, you need to obtain and use a JWT access token.

1. **Generate an Access Token**:
   - Go to the `/token/` endpoint in Swagger UI.
   - Click **Try it out** and enter the credentials:
     - **Email**: `testuser@email.com`
     - **Password**: `testpassword`
   - Execute the request to receive the `access` token.
   - If you face any issue with the username and password follow this procedure and then re do the above steps.

      To create a test user from the command line:

   ```bash
   python manage.py shell
   ```

   Then, run the following commands in the shell:

   ```python
   from django.contrib.auth import get_user_model
   User = get_user_model()
   User.objects.create_user(email='testuser@email.com', password='testpassword')
   ```


2. **Authorize with the Access Token**:
   - Click the **Authorize** button in the Swagger UI.
   - In the "Bearer" field, enter the token as follows:
     ```
     Bearer <your_access_token>
     ```
   - Click **Authorize** to authenticate your session.

3. **Access Protected Endpoints**:
   - With the token in place, you can access endpoints requiring authentication, such as `/data/`.
   - Click **Try it out** on the desired endpoint and execute the request.

### Test-Driven Development (TDD)

This project follows a TDD approach to ensure functionality works as expected and remains unbroken with each update. The tests are organized to cover different parts of the application:

#### Test Files and Their Purposes

- **`test_auth_api.py`**: Tests the REST API authentication endpoints (`/register/`, `/token/`, and `/token/refresh/`), ensuring user registration and JWT token generation functions correctly.
  
- **`test_auth.py`**: Tests the web-based authentication (login functionality) to ensure users can access the D3 chart page after successful login.

- **`test_chart_rendering.py`**: Tests the chart rendering functionality on the frontend, checking if the chart page loads and displays the correct data format.

- **`test_data_api.py`**: Tests the `/data/` endpoint, verifying that it returns the correct chart data and enforces authentication as expected.

#### Running the Tests

To run all tests, use the following command:

```bash
python manage.py test
```

### Next Steps

- **Improving UI**: 
- Django wrapper for NVD3 is not utilized here because of older mac OS (Older than 11) used for development. Some dependency issues in npm. Its tried in this branch https://github.com/VineethKumar7/3IVIS_app/tree/django_nvd3

### Notes

- Resent UI changes and Chart generated from sqlLite DB (models)

[[demo/1]]
[[demo/2]]
[[demo/3]]