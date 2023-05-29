![Madrigal](https://github.com/ValiantDoge/madrigal/blob/dev/website_hr/static/img/logo.png?raw=true)
# Job Recruitment Web Application

This is a job recruitment web application developed by: 
[Agnelo Fernandes](https://github.com/ValiantDoge), 
[Eric Fernandes,](https://github.com/Ericfdes) 
[Shivam Dhargalkar](https://github.com/ShivamD01). 
It is built using Django/Python and includes various features to facilitate the recruitment process.

## Features

- **Resume Builder**: The application includes a resume builder module developed using the ReportLab library. Users can create professional resumes within the application.
- **Authentication with LinkedIn**: The application integrates LinkedIn authentication, allowing users to log in using their LinkedIn accounts.
- **Admin Panel**: An admin panel is available for administrators to manage job listings and content within the application.

## Installation

To install and run the application locally, follow these steps:

1. Clone the repository:

```shell
   git clone https://github.com/ValiantDoge/madrigal.git
 ```
2. Install the required dependencies:

```shell

pip install -r requirements.txt
```

3.Configure the application settings. Update the settings.py file with your specific configuration details, such as database credentials and LinkedIn API keys.

Apply database migrations:

```shell
python manage.py migrate
```

4.Run the development server:

```shell
    python manage.py runserver
```

5.Access the application by navigating to http://localhost:8000 or http://127.0.0.1:8000/ in your web browser.


## Madrigal is deployed on PythonAnywhere. ![Click here to visit!](https://valiantdoge.pythonanywhere.com/) 
