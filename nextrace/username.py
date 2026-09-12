import re

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nextrace.username_sites import (
    USERNAME_SITES,
    get_check_url,
    get_profile_url,
)

console = Console()


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; NexTrace/1.0; "
        "Public OSINT Username Checker)"
    ),
    "Accept": "text/html,application/json",
}


def validate_username(username):
    """Validate and normalize the supplied username."""

    cleaned = username.strip()

    if not cleaned:
        return False, "KuchuPuchu Yaar Username Toh Likho 😭"

    if len(cleaned) > 100:
        return False, "Username unusually long hai."

    if re.search(r"\s", cleaned):
        return False, "Username ke andar spaces nahi hone chahiye."

    return True, cleaned


def check_username_on_site(site_name, site_data, username):
    """
    Check whether a username appears to exist on a public platform.

    Results:
        Found
        Not Found
        Uncertain
        Error
    """

    profile_url = get_profile_url(
        site_data,
        username,
    )

    check_url = get_check_url(
        site_data,
        username,
    )

    try:
        response = requests.get(
            check_url,
            headers=HEADERS,
            timeout=8,
            allow_redirects=True,
        )

        status_code = response.status_code

        found_status = site_data.get(
            "found_status",
            [],
        )

        not_found_status = site_data.get(
            "not_found_status",
            [],
        )

        if status_code in found_status:
            status = "Found"

        elif status_code in not_found_status:
            status = "Not Found"

        else:
            status = "Uncertain"

        return {
            "site": site_name,
            "status": status,
            "status_code": status_code,
            "profile_url": profile_url,
        }

    except requests.Timeout:
        return {
            "site": site_name,
            "status": "Error",
            "status_code": "Timeout",
            "profile_url": profile_url,
        }

    except requests.RequestException:
        return {
            "site": site_name,
            "status": "Error",
            "status_code": "Request failed",
            "profile_url": profile_url,
        }


def username_search():
    """Run NexTrace Username Search."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Username Search[/bold cyan]\n"
            "[dim]Public profile discovery[/dim]",
            border_style="cyan",
        )
    )

    username_input = console.input(
        "\n[bold yellow]Enter username: [/bold yellow]"
    )

    is_valid, result = validate_username(
        username_input
    )

    if not is_valid:
        console.print(
            f"\n[bold red]Error:[/bold red] {result}"
        )
        return

    username = result

    console.print(
        f"\n[dim]Checking public profiles for "
        f"'{username}'...[/dim]\n"
    )

    results = []

    for site_name, site_data in USERNAME_SITES.items():

        result = check_username_on_site(
            site_name,
            site_data,
            username,
        )

        results.append(result)

    table = Table(
        title="NexTrace Username Intelligence Report",
        show_header=True,
    )

    table.add_column(
        "Platform",
        style="cyan",
    )

    table.add_column(
        "Status",
    )

    table.add_column(
        "HTTP",
        justify="center",
    )

    table.add_column(
        "Public Profile",
        style="blue",
    )

    found_count = 0
    not_found_count = 0
    uncertain_count = 0
    error_count = 0

    for result in results:

        status = result["status"]

        if status == "Found":
            status_display = "[bold green]Found[/bold green]"
            found_count += 1

        elif status == "Not Found":
            status_display = "[dim]Not Found[/dim]"
            not_found_count += 1

        elif status == "Uncertain":
            status_display = "[yellow]Uncertain[/yellow]"
            uncertain_count += 1

        else:
            status_display = "[red]Error[/red]"
            error_count += 1

        table.add_row(
            result["site"],
            status_display,
            str(result["status_code"]),
            result["profile_url"],
        )

    console.print(table)

    console.print(
        "\n[bold cyan]Scan Summary[/bold cyan]"
    )

    console.print(
        f"Found: [green]{found_count}[/green]  |  "
        f"Not Found: {not_found_count}  |  "
        f"Uncertain: [yellow]{uncertain_count}[/yellow]  |  "
        f"Errors: [red]{error_count}[/red]"
    )

    console.print(
        "\n[dim]"
        "OSINT Notice: NexTrace checks publicly accessible profile "
        "endpoints only. A matching username does not prove that "
        "accounts on different platforms belong to the same person. "
        "Some platforms may block automated requests or return "
        "ambiguous responses, which NexTrace reports as Uncertain "
        "rather than claiming a false match."
        "[/dim]"
    )