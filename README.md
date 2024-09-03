This application creates a RESTful API that generates unique tracking numbers for parcels that matches the pattern `^[A-Z0-9]{1,16}$`
The API is created using django REST framework. The dependencies are listed in requirements.txt file

steps to run the app locally

- clone the git repository using git clone command
- create virtual environment
  
  python3 -m venv venv
  
- install dependencies
  
  pip install -r requirements.txt
  
- apply migrations
  
  python manage.py makemigrations
  python manage.py migrate
  
- run the server
  
  python manage.py runserver


Example API endpoint - "http://localhost:8000/next-tracking-number/?origin_country_id=MY&destination_country_id=ID&weight=1.234&created_at=2018-11-20T19:29:32%2B08:00&customer_id=de619854-b59b-425e-9db4-943979e1bd49&customer_name=RedBox%20Logistics&customer_slug=redbox-logistics"
