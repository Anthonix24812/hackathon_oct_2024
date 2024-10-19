FROM python:3.10

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

ENV FLASK_APP=src/server.py

# RUN python3 -m pytest tests
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]