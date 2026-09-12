import re

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nextrace.rto_data import get_rto_info

console = Console()


# Indian vehicle registration State / UT codes
STATE_CODES = {
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CG": "Chhattisgarh",
    "CH": "Chandigarh",
    "DD": "Dadra and Nagar Haveli and Daman and Diu",
    "DL": "Delhi",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HP": "Himachal Pradesh",
    "HR": "Haryana",
    "JH": "Jharkhand",
    "JK": "Jammu and Kashmir",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "MH": "Maharashtra",
    "ML": "Meghalaya",
    "MN": "Manipur",
    "MP": "Madhya Pradesh",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OD": "Odisha",
    "PB": "Punjab",
    "PY": "Puducherry",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TR": "Tripura",
    "TS": "Telangana",
    "UK": "Uttarakhand",
    "UP": "Uttar Pradesh",
    "WB": "West Bengal",
}


def clean_registration_number(registration):
    """Normalize the registration number."""

    return re.sub(
        r"[^A-Z0-9]",
        "",
        registration.upper(),
    )


def analyse_registration(registration):
    """Analyse an Indian vehicle registration number."""

    cleaned = clean_registration_number(registration)

    if not cleaned:
        return None, "KuchuPuchu Yaar Number Plate Toh Likho 😭"

    if len(cleaned) < 6:
        return None, "Registration number bahut chhota lag raha hai."

    if len(cleaned) > 12:
        return None, "Registration number expected format se zyada lamba hai."

    state_code = cleaned[:2]
    state_name = STATE_CODES.get(state_code)

    if not state_name:
        return None, "State/UT registration code identify nahi ho paaya."

    # Common registration structure:
    # State + RTO digits + Series + Registration number
    #
    # Example:
    # DL01AB1234
    #
    # DL   -> State / UT
    # 01   -> Registering authority code
    # AB   -> Series
    # 1234 -> Registration number

    match = re.fullmatch(
        r"([A-Z]{2})(\d{1,2})([A-Z]{0,3})(\d{1,4})",
        cleaned,
    )

    if not match:
        return {
            "cleaned": cleaned,
            "state_code": state_code,
            "state_name": state_name,
            "format_valid": False,
        }, None

    detected_state = match.group(1)
    rto_code = match.group(2)
    series = match.group(3)
    vehicle_number = match.group(4)

    # Search our verified public RTO dataset
    rto_info = get_rto_info(
        detected_state,
        rto_code,
    )

    return {
        "cleaned": cleaned,
        "state_code": detected_state,
        "state_name": state_name,
        "rto_code": rto_code,
        "series": series or "Not present",
        "vehicle_number": vehicle_number,
        "format_valid": True,
        "rto_info": rto_info,
    }, None


def vehicle_intelligence():
    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Vehicle Intelligence[/bold cyan]\n"
            "[dim]Public registration metadata analysis[/dim]",
            border_style="cyan",
        )
    )

    registration_input = console.input(
        "\n[bold yellow]"
        "Enter Indian vehicle registration number "
        "(e.g. DL01AB1234): "
        "[/bold yellow]"
    )

    result, error = analyse_registration(
        registration_input
    )

    if error:
        console.print(
            f"\n[bold red]Error:[/bold red] {error}"
        )
        return

    table = Table(
        title="NexTrace Vehicle Intelligence Report",
        show_header=True,
    )

    table.add_column(
        "Field",
        style="cyan",
    )

    table.add_column(
        "Result",
        style="white",
    )

    # Input information
    table.add_row(
        "Input",
        registration_input,
    )

    table.add_row(
        "Normalized",
        result["cleaned"],
    )

    table.add_section()

    # State information
    table.add_row(
        "State / UT Code",
        result["state_code"],
    )

    table.add_row(
        "State / UT",
        result["state_name"],
    )

    if result["format_valid"]:

        table.add_row(
            "RTO Code",
            result["rto_code"],
        )

        table.add_row(
            "Series",
            result["series"],
        )

        table.add_row(
            "Registration Number",
            result["vehicle_number"],
        )

        table.add_section()

        # Verified RTO metadata
        rto_info = result["rto_info"]

        if rto_info:

            table.add_row(
                "Registering Authority",
                rto_info["name"],
            )

            table.add_row(
                "Authority Area",
                rto_info["area"],
            )

            table.add_row(
                "RTO Data Source",
                rto_info["source"],
            )

            rto_status = "Verified mapping available"

        else:

            table.add_row(
                "Registering Authority",
                "Not available in verified dataset",
            )

            table.add_row(
                "Authority Area",
                "Unknown",
            )

            rto_status = "No verified mapping available"

        table.add_section()

        table.add_row(
            "Format Status",
            "Recognized Indian registration format",
        )

        table.add_row(
            "RTO Lookup Status",
            rto_status,
        )

    else:

        table.add_section()

        table.add_row(
            "Format Status",
            "State detected, but complete format not recognized",
        )

    console.print()
    console.print(table)

    if result["format_valid"]:

        console.print(
            "\n[bold green]"
            "✓ Registration structure successfully analysed."
            "[/bold green]"
        )

    else:

        console.print(
            "\n[bold yellow]"
            "⚠ Registration prefix was recognized, but the complete "
            "plate does not match the currently supported format."
            "[/bold yellow]"
        )

    console.print(
        "\n[dim]"
        "Metadata Notice: Registering-authority information represents "
        "the authority associated with the registration code. It does "
        "not indicate the vehicle's current or live location. NexTrace "
        "does not retrieve private owner names, addresses, contact "
        "details, or other restricted registration records."
        "[/dim]"
    )