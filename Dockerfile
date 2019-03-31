FROM python:3.7.3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.lock.txt
RUN python -m pytest --cov=src --cov-report=html --cov-report=term
CMD [ "python", "./src/PointOfSale.py" ]
