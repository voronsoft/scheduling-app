```markdown
backend/
├── .dockerignore
├── .env
├── api_fast_api/
│   ├── auth/
│   │   ├── authentication.py
│   │   
│   ├── config.py
│   ├── db_api/
│   │   ├── async_api_data.db
│   │   
│   ├── func/
│   │   ├── create_project_structure_file.py
│   │   ├── csrf_functions.py
│   │   ├── functions.py
│   │   
│   ├── logger_project/
│   │   ├── logger_config.py
│   │   ├── logger__app.py
│   │   
│   ├── logs_data/
│   │   ├── debug.log
│   │   ├── error.log
│   │   ├── warning.log
│   │   
│   ├── models/
│   │   ├── async_models.py
│   │   ├── models_pydantic.py
│   │   
│   ├── routers/
│   │   ├── routers_html.py
│   │   ├── routes_admin.py
│   │   ├── routes_calendar.py
│   │   
│   ├── static/
│   │   ├── css/
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── navbar-fixed.css
│   │   │   
│   │   ├── img/
│   │   │   ├── favicon.svg
│   │   │   ├── vite.svg
│   │   │   
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.js
│   │   │   ├── bootstrap.bundle.js.map
│   │   │   ├── functions.js
│   │   │   
│   │   
│   ├── templates/
│   │   ├── error_modal_window.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── registration.html
│   │   ├── timetable.html
│   │   
│   ├── __init__.py
│   
├── docker-compose.yml
├── Dockerfile
├── notes_frontend_structure_administrative_part.md
├── notes_project.txt
├── notes_projec_docker.txt
├── requirements.txt
├── run_fapi.py
├── run_fapi_docker.py
├── structure_project.md

```