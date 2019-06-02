## Runner App Backend API

### Required system packages:

- rabbitmq-server
- libpq-def
- postgresql v9

### Running the server with rabbit mq

1. python manage.py configurations=DevSettings

Optional: Running the reverse geocoding lookup

2. celery -A runner_recommender_app worker -l info

### Extracting required data from Runtastic

1. Login to your account in https://www.runtastic.com/

2. Go to Settings

3. Click on Export

4. Download and extract the data zip file

5. Select the Sport-Session folder and zip it

6. Submit the Sport-Session zip file

### Extracting required data from Strave

1. Login to https://www.strava.com/

2. Hover on your profile on the top right corner to reveal a drop down menu

3. Click on "Settings" on the drop down menu

4. Click My Account

5. On the "Download and Delete your Account" section below, click "Get Started"

6. On the "Download Request" section, click "Request Your Archive"

7. Check your email for the download link. Download and extract it

8. Select "activites" folder and "activities.csv" files and zip it

9. Submit the zipped files and folders


### TODO:

* Progress Bar while processing the uploads

* Error handling and Success views

* Further testing, Success/Fail messages and handling

### 23-05-2019 Changes:

* make sure to set the following environment variables when running
the backend server:

  - APP\_DOMAIN - used by upload app. This domain is where the app would make POST requests to when uploading data to the server. would use localhost and the request port as the domain if this variable is left blank

  - UPLOAD\_USER - the username used to access the API's. set to 'admin' if blank

  - UPLOAD\_PASS - the password used to access the API's. set to 'admin' if blank

* Added DevSettings and ProdSettings as configuration arguments that can be passed to manage.py when running the server. use --configuration=DevSettings when running locally

* WIP: limitations on Heroku database may need to change the schema to NOT store the individual points. instead set as an Array Field (requires PostgreSQL) in RunPath model.

* These complications would not arise if the server is run locally.

### 21-05-2019

* Added upload app to upload both runtastic and strava data. In strava,
the data that only gets uploaded are the run data

* Upload page for strava can accept GPX, FIT and FIT.GZ files

* Processed FIT files and GPX to retrieve only the necessary things

* Added a Function that computes the corresponding lat lon given semi-circle values

* Tested uploads of both runtastic and strava, given perfect conditions


### 15-05-2019 Updates

* Added upload app to upload data

* Studied Flexible & Interoperable Data Transfer Protocol (FIT by Garmin)

* Processed FIT binary files for processing

* Added Centroid computation using semicircle lat and long point data format


### Semestral Break Task Break down

- 3 days spent on dataset exploration.
  
  * Dataset from Runtastic and Strava has been explored.

  * This involved exporting and gathering dataset from the tracking application

  * Examining the structure of the dataset. Since the dataset from runtastic did
    not have any sort of documentation, a little bit of reverse engineering was
    done to figure out the characteristics of some attributes needed to carry out
    the algorithm.

  * The process of reverse engineering involved comparing the raw dataset of a specific run
    and mapping the data displayed by the app with the attribute that correspond to that value.
    In this way we can have the idea as to how the displayed data in the app came to be, or 
    if the displayed data is actually calculated using the raw data. Using the app as reference
    also helped us determine the units of measurement for each value in the dataset

  * Specifically, the distance attribute was studied, and how the longitude, latitude points
    were used to determine the distance between points as well as the total distance of a run,
    given only longitude latitude points.

  * Euclidean distance calculation did not yield meaningful results, since the points
    do not lie on a flat plane. The resulting distance did not correspond to the distance
    as displayed on the app

  * The Haversine formula was then tested to see if it would yield a close value in terms of distance
    in the dataset. The resulting distance using Haversine value yielded marginal results as the difference
    between the calculated distance and the true distance in the dataset have significant difference.
    My understanding why Haversine formula yields different magnitudes from the dataset is that Haversine
    Formula assumes that the points lie on a perfectly spherical surface, which the earth is not.

  * Finally, A C++ library with python bindings were used to calculate distance between lat,long points.
    the library uses Geodesic distance which considers the earth's ellipsoid attribute. 
    The resulting values got difference close to zero. Hence I decided to use Geodesic distance
    To calculate for the distance between two points.

- 3 Days spent developing and implementing a crude simple algorithm that "clusters" these runs into groups.

   * This involves using the dataset to process the distances between different run paths

   * The run's lat and lon points are different from the lat and lon points that make up the path of a run.
     Because of this, I have assumed that the dataset might have some sort of "centroid" to pinpoint the general
     location of run path

   * Using this centroid, I decided to cluster the runs in terms of area where they are generally located. If the distance between
     two centroids is less than a certain threshold (I have set it to 50 meters), then I deem them to be in the same area and I cluster them together 

   * Having a naive clustering function, I have now an idea of a basic data structure to organize the dataset into
     clustered compartments. 

- 4 Days - Implementing the backend webserver

   * The backend's role is not only to serve the clustered dataset to the client/front-end, but also to run the clustering algorithm
     asynchronously. This requires a separate process for the algorithm, aside from the process that handles the request/responce cylce
     of http

   * This involved determining the architecture of the backend, designing a basic schema, studying the related technologies to 
     to implement the whole backend, as well as preliminary testing if the design works with the given technologies 

   * ERD was used to design the schema. Along woth the schema, a Functional Block Diagram was also drawn up to layout
     the interaction of each tech stack the modules in a single diagram

   * The webserver is done using a python framework Django Rest Framework (DFR).
     Going through the tutorials and reading through the Guides and Documentation.
     Since DFR runs to complement another framework (Django full stack), Django was also studied,
     Specifically the Models and Object Relational Mapper, which we intend to capitalize in the first place.
     The output for this study is to be able to implement API endpoints that the front end would eventually require.
     The endpoints were loosely determined and will possibly change in the future as the front end is developed.

   * After some research, we determined that the execution of the algorithm must not be inside the request/response cycle.
     For this matter, we needed to run the algorithm asynchronously. Since Django is entirely single threaded, it would be bad design
     If we put the clustering algorithm inside the functions that handles the http requests. Because of this I needed to integrate
     Celery, a message based task ditributor. Fortunately the documentation of how to integrate Celery into Django as abundant, though
     I still encountered errors which resulted from differing of versions used in some tutorials.
     I also got exposed to the whole Message Queuing Protocol. In line with this, I used rabbitMQ as the message broker. Since our algorith
     Directly modifies the database, the async function does not return any value. It would be a good addition though to notify the front end
     that a new data has been added and would require refresh of the page

   * As soon as the backend is working in my local machine, I had to deploy the backend to some server if I want the front end to be able
     access my api's. I have previously used heroku before for some front end projects. However I still had to refresh how to deploy, specifically
     a django app, to heroku. This required further study of deployment, setting up the app such that it can be deployed 
     successfully in a heroku instance as well as adding security and authentication to the app so that only
     authorized users can have access to POST http actions.
  
