FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# #  app.run(....) is needed 
# CMD ["python", "main.py"]  

# app run() is  not needed, better for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
