# NexTrace - Username Search Site Definitions
#
# These definitions contain only public profile endpoints.
# NexTrace does not attempt to access private accounts,
# bypass authentication, or retrieve restricted information.


USERNAME_SITES = {
    "GitHub": {
        "url": "https://github.com/{}",
        "check_url": "https://api.github.com/users/{}",
        "method": "status",
        "found_status": [200],
        "not_found_status": [404],
    },

    "GitLab": {
        "url": "https://gitlab.com/{}",
        "check_url": "https://gitlab.com/{}",
        "method": "status",
        "found_status": [200],
        "not_found_status": [404],
    },

    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "check_url": "https://www.reddit.com/user/{}",
        "method": "status",
        "found_status": [200],
        "not_found_status": [404],
    },

    "Pinterest": {
        "url": "https://www.pinterest.com/{}/",
        "check_url": "https://www.pinterest.com/{}/",
        "method": "status",
        "found_status": [200],
        "not_found_status": [404],
    },
}


def get_profile_url(site_data, username):
    """Build the public profile URL for a username."""

    return site_data["url"].format(username)


def get_check_url(site_data, username):
    """Build the URL NexTrace will use to check the username."""

    return site_data["check_url"].format(username)


def get_supported_sites():
    """Return a list of currently supported username platforms."""

    return list(USERNAME_SITES.keys())