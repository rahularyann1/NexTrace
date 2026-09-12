import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from nextrace.phone_utils import (
    get_number_type,
    validate_phone_input,
    get_analysis_status,
)

console = Console()


def phone_intelligence():
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Phone Intelligence[/bold cyan]\n"
            "[dim]Public numbering metadata analysis[/dim]",
            border_style="cyan",
        )
    )

    number_input = console.input(
        "\n[bold yellow]Enter phone number with country code "
        "(e.g. +91XXXXXXXXXX): [/bold yellow]"
    )

    # Step 1: Basic input validation
    is_valid_input, result = validate_phone_input(number_input)

    if not is_valid_input:
        console.print(f"\n[bold red]Error:[/bold red] {result}")
        return

    cleaned_number = result

    try:
        # Step 2: Parse the international phone number
        number = phonenumbers.parse(cleaned_number, None)

        # Step 3: Validation
        valid = phonenumbers.is_valid_number(number)
        possible = phonenumbers.is_possible_number(number)

        # Step 4: Geographic / numbering-plan metadata
        region_code = phonenumbers.region_code_for_number(number)
        region_name = geocoder.description_for_number(number, "en")

        # Step 5: Carrier and timezone metadata
        network = carrier.name_for_number(number, "en")
        timezones = timezone.time_zones_for_number(number)

        # Step 6: Number classification
        detected_type = get_number_type(number)
        analysis_status = get_analysis_status(number)

        # Step 7: Standard number formats
        e164_format = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.E164,
        )

        international_format = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL,
        )

        national_format = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.NATIONAL,
        )

        rfc3966_format = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.RFC3966,
        )

        # Step 8: Build report
        table = Table(
            title="NexTrace Phone Intelligence Report",
            show_header=True,
        )

        table.add_column("Field", style="cyan")
        table.add_column("Result", style="white")

        table.add_row("Input", number_input)
        table.add_row("E.164", e164_format)
        table.add_row("International", international_format)
        table.add_row("National", national_format)
        table.add_row("RFC3966", rfc3966_format)

        table.add_section()

        table.add_row(
            "Country Calling Code",
            f"+{number.country_code}",
        )
        table.add_row(
            "National Number",
            str(number.national_number),
        )
        table.add_row(
            "ISO Region",
            region_code or "Unknown",
        )
        table.add_row(
            "Region Metadata",
            region_name or "Unknown",
        )

        table.add_section()

        table.add_row(
            "Number Type",
            detected_type,
        )
        table.add_row(
            "Valid",
            "Yes" if valid else "No",
        )
        table.add_row(
            "Possible",
            "Yes" if possible else "No",
        )
        table.add_row(
            "Analysis Status",
            analysis_status,
        )

        table.add_section()

        table.add_row(
            "Carrier Metadata",
            network or "Unknown",
        )
        table.add_row(
            "Timezone Metadata",
            ", ".join(timezones) if timezones else "Unknown",
        )

        console.print()
        console.print(table)

        # Step 9: Interpretation
        if valid:
            console.print(
                "\n[bold green]✓ Number passed numbering-plan validation.[/bold green]"
            )
        elif possible:
            console.print(
                "\n[bold yellow]⚠ Number has a possible structure, "
                "but is not considered valid.[/bold yellow]"
            )
        else:
            console.print(
                "\n[bold red]✗ Number does not match the expected "
                "numbering-plan structure.[/bold red]"
            )

        # Step 10: Important OSINT disclaimer
        console.print(
            "\n[dim]"
            "Metadata Notice: Results are derived from public numbering-plan "
            "metadata. Carrier information may represent the originally "
            "assigned network and can become outdated after number portability. "
            "Region and timezone metadata do not represent a person's current "
            "or live physical location."
            "[/dim]"
        )

    except phonenumbers.NumberParseException as error:
        console.print(
            f"\n[bold red]Could not parse phone number:[/bold red] {error}"
        )

    except Exception as error:
        console.print(
            "\n[bold red]Unexpected Phone Intelligence error:[/bold red] "
            f"{error}"
        )