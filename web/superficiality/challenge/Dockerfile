# FRONTEND
# ------------------------------------
FROM node:14 as frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json ./
RUN npm install

COPY frontend/ .

RUN npm run build


# BACKEND
# ------------------------------------
FROM python:3.11-slim as backend-builder

WORKDIR /app/backend

COPY backend/requirements.txt ./
RUN pip install  --target=/app/backend/deps --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PYTHONPATH="/app/backend/deps"

# Run Django migrations (if necessary)
RUN python manage.py migrate
RUN python manage.py make_some_data


# PROXY
# ------------------------------------
FROM nginx:mainline-bullseye as app

ENV PYTHONPATH="/app/backend/deps"

RUN apt update -y && apt install gunicorn -y

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html
COPY --from=backend-builder /app/backend /app/backend

# Set the working directory to the backend
WORKDIR /app/backend

COPY flag .

# Start Nginx and run Django backend
#DJANGO_SETTINGS_MODULE=superficiality.settings
CMD service nginx start && gunicorn  superficiality.wsgi:application --bind localhost:8000