from celery import shared_task

@shared_task
def upload_run_data(endpoint, data, user='admin', passwd='admin'):
    """
    Async task to POST on the micro service for runpaths and points
    """
    # single place
    # POST to runner_app api
    # runpaths_uri = endpoint['runpaths']
    # points_uri = endpoint['points']
    # results = []
    # for path_points in data:
    #     runpath = path_points[0]
    #     points = path_points[1]

    #     res_path = rq.post(runpaths_uri,
    #             data=runpath,
    #             auth=(user, passwd))
    #     run_id = res_path.json()['id']

    #     for point in points:
    #         point['run_path'] = run_id

    #     res_points = rq.post(points_uri,
    #             json = points,
    #             auth=(user, passwd))
    #     results.append((res_path, res_points))
    # return results


