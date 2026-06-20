# Docker Flask MySQL Example

A simple full-stack application using:

- Flask (Backend API)
- MySQL (Database)
- HTML, CSS, JavaScript (Frontend)
- Nginx (Frontend Web Server)
- Docker & Docker Compose

## Project Structure

```text
.
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── mysql/
│   └── init.sql
│
├── docker-compose.yml
├── .env
└── README.md
```

## Services

### MySQL
- Database: `personsdb`
- User: `flaskuser`
- Password: `flaskpassword`

### Backend
- Flask REST API
- Runs on port `5000`

### Frontend
- Nginx web server
- Runs on port `2000`

## Getting Started

### Build and Start Containers

```bash
docker compose up --build
```

### Run in Background

```bash
docker compose up -d --build
```

### Stop Containers

```bash
docker compose down
```

### Remove Containers and Database Volume

```bash
docker compose down -v
```

## Access the Application

Frontend:

```text
http://localhost:2000
```

Backend API:

```text
http://localhost:5000
```

## Database Initialization

The file `mysql/init.sql` is executed automatically when the MySQL container is created for the first time.

If you modify `init.sql`, recreate the database volume:

```bash
docker compose down -v
docker compose up --build
```

## Environment Variables

The backend uses the following variables:

```env
DB_HOST=mysql
DB_PORT=3306
DB_NAME=personsdb
DB_USER=flaskuser
DB_PASS=flaskpassword
```

These are provided through `docker-compose.yml`.

## Useful Commands

View running containers:

```bash
docker ps
```

View logs:

```bash
docker compose logs
```

View backend logs:

```bash
docker compose logs backend
```

View database logs:

```bash
docker compose logs mysql
```

## Author

Docker Flask MySQL Example Project