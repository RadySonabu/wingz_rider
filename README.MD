## Install python on your local machine

### Create a virtual environment using this command `python -m venv .venv`

### Activate that environment

### Install the necessary packages using this comman `pip install -r requirements.txt`

Run the program using this command and paste it to the CLI `python manage.py runserver`

Challenges:
While working on the projects, I had some questions and needed clarifications, such as whether I am allowed to create more than one serializer for a specific viewset, and so on. Fortunately, I managed to finish the project despite having these questions in mind.

#Bonus SQL
`SELECT 
	DATE_TRUNC('month', pickup_event.created_at) AS month,
    r.id_driver_id,
    COUNT(*) AS trip_count
from rides_ride r
JOIN 
    rides_rideevent pickup_event on r.id_ride  = pickup_event.ride_id
    AND pickup_event.description = 'Status changed to pickup'
JOIN 
    rides_rideevent dropoff_event on r.id_ride  = dropoff_event.ride_id
    AND dropoff_event.description = 'Status changed to dropoff'
WHERE 
    EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) > 3600 
GROUP BY
    month, r.id_driver_id
ORDER BY
    month, r.id_driver_id;
`
