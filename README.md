# PlankData
To run the docker container use:
docker build -t planck-flask .
docker run -p 8080:8080 planck-flask

# Runs:
You can see the image at http://localhost:8080/

# Variant URL's for the models:
http://localhost:8080/hilltop?amp=4700&mu=13.5&v=1.8&p=3.2&phi=0.37
http://localhost:8080/starobinsky?amp=5500&decay=9000&phase=4.0&freq=0.95&supp=0.07

