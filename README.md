# PlankData
To run the docker container use:
docker build -t planck-flask .
docker run -p 8080:8080 planck-flask

# Runs:
You can see the image at http://localhost:8080/

# Variant URL's for the models:
http://localhost:8080/hilltop?amp=5400&decay=2000&phase=2.5&freq=0.0125&alpha=0.2&beta=0.4
http://localhost:8080/starobinsky?amp=5500&decay=4000&phase=3.8&freq=0.0128&supp=0.08
