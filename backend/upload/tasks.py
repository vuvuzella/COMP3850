from celery import shared_task
import requests

@shared_task
def upload_run_data(endpoint, data, user='admin', passwd='admin'):
    """
    Async task to POST on the micro service for runpaths and points
    Uploads a single run path and its points
    """
    # single place
    # POST to runner_app api
    runpaths_uri = endpoint['runpaths']
    points_uri = endpoint['points']

    runpath = data[0]
    points = data[1]

    res_path = requests.post(runpaths_uri,
            data=runpath,
            auth=(user, passwd))
    run_id = res_path.json()['id']

    for point in points:
        point['run_path'] = run_id

    res_points = requests.post(points_uri,
            json=points,
            auth=(user, passwd))

    # if res_path.status_code == 201 and res_points.status_code == 201:
    #     return True
    # else:
    #     return False

    return (res_path.status_code, res_points.status_code)


