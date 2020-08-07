# Project Motivation
The main objective of the project is to determine distance between two points lying on geodesic plane or euclidean plane.

In this project software engineering practices will be applied to create a python package.

### Background
**Distance between Two Points on Geodesic Plane:** Distance between two points in geodesic plane such as location coordinates on earth can be obtained by using [haversine formula](https://www.movable-type.co.uk/scripts/latlong.html)

**Distance between Two Points on Euclidean Plane (2-D):** Distance between two points lying on a 2D plane can be determined by using the formula: `sqrt((x1-x2)^2 + (y1-y2)^2))`

### Required Libraries
1. math

### Instructions
```python
pip install pointdistance
```
```python
# Import package
# Measure Geodesic distance
from pointdistance import GeodesicPoints
geodesicPoints = GeodesicPoints((latitude_1, longitude_1), (latitude_2, longitude_2))
print(geodesicPoints.distance)

# Measure Euclidean distance
from pointdistance import EuclideanPoints
euclideanPoints = EuclideanPoints((x_1, y_1), (x_2, y_2))
print(euclideanPoints.distance)
```

### Acknowledgement
[Haversine formula](https://www.movable-type.co.uk/scripts/latlong.html)