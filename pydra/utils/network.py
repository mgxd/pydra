"""Methods for network communication"""

import requests
import time


def post_taskinfo(task, url: str, **kwargs):
    """
    Create unique identifier for task and post to url.

    Parameters
    ----------
    task : `pydra.engine.core.Task`

    url : str

    Returns
    -------
    nodeid : str
    """
    # create Unique Task IDentifier by combining task checksum with time
    utid = f'{task.checksum}-{time.time()}'
    data = {'pydraTask': utid}
    resp = requests.post(url, json=data, **kwargs)
    if not 199 < resp.status_code <= 201:
        raise ConnectionError("POST request unsuccessful.")
    return utid


def get_completed_tasks(url: str, utid: str = None, **kwargs) -> bool:
    """
    Ping url and parse result for completed task.
    """
    resp = requests.get(url)
    if not resp.status_code == 200:
        raise ConnectionError("GET request unsuccessful.")
    try:
        data = resp.json()
    except ValueError as e:
        raise Exception("Response not in JSON format.") from e
    # parse response for utid
    if data.get(utid, None) is not None:
        complete = data[utid].get("Complete")
        if complete == 'yes':
            return True
    return False
