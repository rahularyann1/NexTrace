import re

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


# Verhoeff tables used for Aadhaar checksum validation
VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]


def validate_verhoeff(number):
    """Validate a numeric string using Verhoeff checksum."""

    checksum = 0

    try:
        digits = [int(digit) for digit in reversed(number)]

        for position, digit in enumerate(digits):
            checksum = VERHOEFF_D[checksum][
                VERHOEFF_P[position % 8][digit]
            ]

        return checksum == 0

    except (ValueError, IndexError):
        return False


def clean_aadhaar(value):
    """Remove spaces and hyphens."""

    return re.sub(
        r"[\s-]",
        "",
        value.strip(),
    )


def validate_aadhaar(value):
    """Offline Aadhaar structure and checksum validation."""

    cleaned = clean_aadhaar(value)

    if not cleaned:
        return {
            "valid": False,
            "number": "",
            "reason": "KuchuPuchu Aadhaar Number Toh Likho Yaar 😭",
        }

    if not cleaned.isdigit():
        return {
            "valid": False,
            "number": cleaned,
            "reason": "Aadhaar mein sirf digits hone chahiye.",
        }

    if len(cleaned) != 12:
        return {
            "valid": False,
            "number": cleaned,
            "reason": "Aadhaar exactly 12 digits ka hona chahiye.",
        }

    if cleaned[0] in {"0", "1"}:
        return {
            "valid": False,
            "number": cleaned,
            "reason": "Aadhaar structure valid nahi hai.",
        }

    if not validate_verhoeff(cleaned):
        return {
            "valid": False,
            "number": cleaned,
            "reason": "Verhoeff checksum validation failed.",
        }

    return {
        "valid": True,
        "number": cleaned,
        "reason": "Structure and checksum passed.",
    }


def mask_aadhaar(number):
    """Mask Aadhaar in terminal output."""

    if len(number) != 12:
        return "Invalid / unavailable"

    return f"XXXX XXXX {number[-4:]}"


def validate_pan(value):
    """Offline PAN format validation."""

    cleaned = value.strip().upper().replace(" ", "")

    if not cleaned:
        return {
            "valid": False,
            "pan": "",
            "reason": "KuchuPuchu PAN Toh Likho Yaar 😭",
        }

    if not re.fullmatch(r"^[A-Z]{5}[0-9]{4}[A-Z]$", cleaned):
        return {
            "valid": False,
            "pan": cleaned,
            "reason": "PAN expected format ABCDE1234F se match nahi karta.",
        }

    return {
        "valid": True,
        "pan": cleaned,
        "reason": "PAN format passed.",
    }


def mask_pan(pan):
    """Mask PAN in terminal output."""

    if len(pan) != 10:
        return "Invalid / unavailable"

    return f"{pan[:2]}***{pan[5:7]}**{pan[-1]}"


def aadhaar_validator():
    """Interactive Aadhaar validator."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Aadhaar Validator[/bold cyan]\n"
            "[dim]Offline structure and checksum validation[/dim]",
            border_style="cyan",
        )
    )

    aadhaar_input = console.input(
        "\n[bold yellow]Enter Aadhaar number: [/bold yellow]"
    )

    result = validate_aadhaar(aadhaar_input)

    table = Table(
        title="NexTrace Aadhaar Validation Report",
        show_header=True,
    )

    table.add_column("Field", style="cyan")
    table.add_column("Result", style="white")

    table.add_row(
        "Masked Aadhaar",
        mask_aadhaar(result["number"]),
    )

    table.add_row(
        "Length",
        str(len(result["number"])),
    )

    table.add_row(
        "Digits Only",
        "Yes" if result["number"].isdigit() else "No",
    )

    table.add_row(
        "Validation",
        "Passed" if result["valid"] else "Failed",
    )

    table.add_row(
        "Reason",
        result["reason"],
    )

    console.print()
    console.print(table)

    if result["valid"]:
        console.print(
            "\n[bold green]"
            "✓ Aadhaar structure and checksum validation passed."
            "[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]"
            "✗ Aadhaar validation failed."
            "[/bold red]"
        )

    console.print(
        "\n[dim]"
        "Privacy Notice: NexTrace performs offline mathematical "
        "validation only. A passing result does not confirm that the "
        "Aadhaar was issued by UIDAI, is active, or belongs to a "
        "particular person. No private identity records are retrieved."
        "[/dim]"
    )


def pan_validator():
    """Interactive PAN validator."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • PAN Validator[/bold cyan]\n"
            "[dim]Offline PAN format analysis[/dim]",
            border_style="cyan",
        )
    )

    pan_input = console.input(
        "\n[bold yellow]Enter PAN: [/bold yellow]"
    )

    result = validate_pan(pan_input)

    table = Table(
        title="NexTrace PAN Validation Report",
        show_header=True,
    )

    table.add_column("Field", style="cyan")
    table.add_column("Result", style="white")

    table.add_row(
        "Masked PAN",
        mask_pan(result["pan"]),
    )

    table.add_row(
        "Length",
        str(len(result["pan"])),
    )

    table.add_row(
        "Expected Pattern",
        "AAAAA9999A",
    )

    table.add_row(
        "Format Validation",
        "Passed" if result["valid"] else "Failed",
    )

    table.add_row(
        "Reason",
        result["reason"],
    )

    console.print()
    console.print(table)

    if result["valid"]:
        console.print(
            "\n[bold green]"
            "✓ PAN format validation passed."
            "[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]"
            "✗ PAN format validation failed."
            "[/bold red]"
        )

    console.print(
        "\n[dim]"
        "Privacy Notice: NexTrace performs offline PAN format "
        "validation only. A passing result does not confirm that the "
        "PAN was issued, is active, or belongs to a particular person. "
        "No taxpayer or private identity records are retrieved."
        "[/dim]"
    )


def identity_validator():
    """Main Aadhaar & PAN Validator menu."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Aadhaar & PAN Validator[/bold cyan]\n"
            "[dim]Offline identity-number validation tools[/dim]",
            border_style="cyan",
        )
    )

    console.print("\n[cyan][1][/cyan] Aadhaar Validator")
    console.print("[cyan][2][/cyan] PAN Validator")
    console.print("[cyan][0][/cyan] Back")

    choice = console.input(
        "\n[bold yellow]Enter your choice: [/bold yellow]"
    )

    if choice == "1":
        aadhaar_validator()

    elif choice == "2":
        pan_validator()

    elif choice == "0":
        return

    else:
        console.print(
            "\n[yellow]"
            "KuchuPuchu Valid Option Toh Choose Karo 😭"
            "[/yellow]"
        )


if __name__ == "__main__":
    identity_validator()