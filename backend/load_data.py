"""
Load raw json or gpx data into the database
"""
import sqlite3
import os
import re
import json
import time


def load_json_data(dir=None):

    if dir is None:
        return None

    data = []
    json_file = None
    json_file_regex = re.compile('[A-Za-z0-9\-]+.json')
    list_all_files = os.listdir(dir)

    for file_data in list_all_files:
        if re.match(json_file_regex, file_data):
            json_file = '/'.join([dir, file_data])
            with open(json_file) as f:
                data.append(json.load(f))

    return data

def load_runtastic_data():
    """
    Returns
    """
    # load data from runtastic
    cwd = os.getcwd()
    path_to_data = '/'.join([cwd, 'data', 'runtastic', 'Sport-sessions'])

    # load run activity data
    run_activity_data = load_json_data(dir=path_to_data)

    # load run points data 
    run_points_data_path = '/'.join([path_to_data, 'GPS-data'])
    # run_points_data = load_json_data(dir=run_points_data_path)

    # print('Total run activities: ', len(run_activity_data))
    # print('Total run points data: ', len(run_points_data))

    # append the run_points data for each run activity 
    for run_activity in run_activity_data:
        run_points = '/'.join([run_points_data_path, run_activity['id']]) + '.json'
        with open(run_points) as f:
            run_activity['run_points'] = json.load(f)

    return run_activity_data

def populate_database(run_data=None, db_name=None):

    if run_data is None or db_name is None:
        return

    db_conn = sqlite3.connect(db_name)
    cursor = db_conn.cursor()

    run_activity_table = 'runner_api_backend_runpath'
    point_table = 'runner_api_backend_point'

    points_count = 1

    for idx, run in enumerate(run_data):

        # create the run
        # start_time = time.ctime(run['start_time'])
        # end_time = time.ctime(run['end_time'])
        start_time = run['start_time']
        end_time = run['end_time']
        distance = run['distance']
        duration = run['duration']
        # elevation_gain = run['elevation_gain']
        # elevation_loss = run['elevation_loss']
        average_speed = run['average_speed']
        longitude = run['longitude']
        latitude = run['latitude']
        id_name = run['id']
        id_unique = idx

        # Special case for elevation loss and elavatio gain
        if 'elevation_loss' in run.keys():
            elevation_loss = run['elevation_loss']
        else:
            elevation_loss = 'NULL'
        if 'elevation_gain' in run.keys():
            elevation_gain = run['elevation_gain']
        else:
            elevation_gain = 'NULL'

        insert_run = 'INSERT INTO ' + run_activity_table + \
            '(id, start_time, end_time, distance, duration,' + \
            'elevation_gain, elevation_loss, average_speed,' + \
            'longitude, latitude, id_name)' + \
            " VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}')".format(
                    id_unique,
                    start_time,
                    end_time,
                    distance,
                    duration,
                    elevation_gain,
                    elevation_loss,
                    average_speed,
                    longitude,
                    latitude,
                    id_name)
        cursor.execute(insert_run)
        lastrow_id = cursor.lastrowid

        # insert the points 
        # open 
        run_points = run['run_points']
        for idx, point in enumerate(run_points):
            timestamp = point['timestamp']
            longitude = point['longitude']
            latitude = point['latitude']
            altitude = point['altitude']
            speed = point['speed']
            duration = point['duration']
            distance = point['distance']
            elevation_gain = point['elevation_gain']
            elevation_loss = point['elevation_loss']
            run_path_id = lastrow_id

            insert_point = 'INSERT INTO {} '.format(point_table) + \
                    '(id, timestamp, longitude, latitude, altitude,' + \
                    ' speed, duration, distance, elevation_gain, elevation_loss,' + \
                    ' run_path_id) VALUES ' + \
                    "('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}')".format(
                            points_count, timestamp, longitude, latitude, altitude,
                            speed, duration, distance, elevation_gain, elevation_loss,
                            run_path_id)
            cursor.execute(insert_point)
            points_count += 1

    db_conn.commit()
    db_conn.close()
        # TODO: create the points


def main():
    run_activities = load_runtastic_data()
    run_activity = run_activities[1]
    populate_database(run_data=run_activities, db_name='db.sqlite3')

if __name__ == '__main__':
    main()


