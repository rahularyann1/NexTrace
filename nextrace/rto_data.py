# NexTrace - Verified RTO / Registering Authority Data
#
# This file contains registration-authority mappings collected from
# public government transport sources.
#
# Important:
# These mappings identify the registering authority associated with
# a registration code. They do NOT reveal a vehicle's current/live
# location or private owner information.


RTO_DATA = {
    "DL": {
        "01": {
            "name": "North Zone / Mall Road",
            "area": "Civil Lines / Mall Road",
            "source": "Delhi Transport Department",
        },
        "02": {
            "name": "New Delhi Zonal Office",
            "area": "IP Depot",
            "source": "Delhi Transport Department",
        },
        "03": {
            "name": "South Zone / Sheikh Sarai",
            "area": "Sheikh Sarai",
            "source": "Delhi Transport Department",
        },
        "04": {
            "name": "Janak Puri Zonal Office",
            "area": "Janak Puri",
            "source": "Delhi Transport Department",
        },
        "05": {
            "name": "Loni Road Zonal Office",
            "area": "Loni Road",
            "source": "Delhi Transport Department",
        },
        "06": {
            "name": "Sarai Kale Khan Zonal Office",
            "area": "Sarai Kale Khan",
            "source": "Delhi Transport Department",
        },
        "07": {
            "name": "Mayur Vihar Zonal Office",
            "area": "Mayur Vihar",
            "source": "Delhi Transport Department",
        },
        "08": {
            "name": "Wazirpur Zonal Office",
            "area": "Wazirpur",
            "source": "Delhi Transport Department",
        },
    }
}


def get_rto_info(state_code, rto_code):
    """
    Return verified registering-authority metadata when available.

    Returns None when NexTrace does not currently have a verified
    mapping for the supplied state/RTO combination.
    """

    state_code = state_code.upper().strip()
    rto_code = str(rto_code).strip().zfill(2)

    state_data = RTO_DATA.get(state_code)

    if not state_data:
        return None

    return state_data.get(rto_code)