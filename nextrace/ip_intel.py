import ipaddress
import socket

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def validate_ip(ip_input):
    """Validate and normalize an IPv4 or IPv6 address."""

    cleaned = ip_input.strip()

    if not cleaned:
        return False, "KuchuPuchu Yaar IP Address Toh Likho 😭"

    try:
        ip_object = ipaddress.ip_address(cleaned)
        return True, ip_object

    except ValueError:
        return False, "Valid IPv4 ya IPv6 address enter karo."


def classify_ip(ip_object):
    """Return useful IP classification information."""

    if ip_object.is_loopback:
        category = "Loopback"

    elif ip_object.is_private:
        category = "Private / Local"

    elif ip_object.is_multicast:
        category = "Multicast"

    elif ip_object.is_link_local:
        category = "Link-Local"

    elif ip_object.is_reserved:
        category = "Reserved"

    elif ip_object.is_unspecified:
        category = "Unspecified"

    elif ip_object.is_global:
        category = "Public / Global"

    else:
        category = "Special / Non-Global"

    return category


def reverse_dns_lookup(ip_address):
    """Attempt a standard reverse-DNS lookup."""

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(
            ip_address
        )

        return {
            "hostname": hostname,
            "aliases": aliases,
            "addresses": addresses,
        }

    except (
        socket.herror,
        socket.gaierror,
        socket.timeout,
    ):
        return {
            "hostname": None,
            "aliases": [],
            "addresses": [],
        }

    except Exception:
        return {
            "hostname": None,
            "aliases": [],
            "addresses": [],
        }


def ip_intelligence():
    """Run NexTrace IP Intelligence."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • IP Intelligence[/bold cyan]\n"
            "[dim]IP classification and public reverse-DNS analysis[/dim]",
            border_style="cyan",
        )
    )

    ip_input = console.input(
        "\n[bold yellow]Enter IPv4 or IPv6 address: [/bold yellow]"
    )

    is_valid, result = validate_ip(
        ip_input
    )

    if not is_valid:
        console.print(
            f"\n[bold red]Error:[/bold red] {result}"
        )
        return

    ip_object = result
    normalized_ip = str(ip_object)

    console.print(
        f"\n[dim]Analysing IP address "
        f"{normalized_ip}...[/dim]"
    )

    ip_version = (
        "IPv4"
        if ip_object.version == 4
        else "IPv6"
    )

    category = classify_ip(
        ip_object
    )

    reverse_dns = reverse_dns_lookup(
        normalized_ip
    )

    table = Table(
        title="NexTrace IP Intelligence Report",
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

    table.add_row(
        "Input",
        ip_input,
    )

    table.add_row(
        "Normalized IP",
        normalized_ip,
    )

    table.add_row(
        "IP Version",
        ip_version,
    )

    table.add_section()

    table.add_row(
        "Category",
        category,
    )

    table.add_row(
        "Public / Global",
        "Yes" if ip_object.is_global else "No",
    )

    table.add_row(
        "Private",
        "Yes" if ip_object.is_private else "No",
    )

    table.add_row(
        "Loopback",
        "Yes" if ip_object.is_loopback else "No",
    )

    table.add_row(
        "Link-Local",
        "Yes" if ip_object.is_link_local else "No",
    )

    table.add_row(
        "Multicast",
        "Yes" if ip_object.is_multicast else "No",
    )

    table.add_row(
        "Reserved",
        "Yes" if ip_object.is_reserved else "No",
    )

    table.add_section()

    table.add_row(
        "Reverse DNS Hostname",
        reverse_dns["hostname"] or "Not detected",
    )

    if reverse_dns["aliases"]:
        table.add_row(
            "Hostname Aliases",
            "\n".join(reverse_dns["aliases"]),
        )
    else:
        table.add_row(
            "Hostname Aliases",
            "None detected",
        )

    console.print()
    console.print(table)

    if ip_object.is_global:
        console.print(
            "\n[bold green]"
            "✓ Public/global IP address detected."
            "[/bold green]"
        )

    elif ip_object.is_private:
        console.print(
            "\n[bold yellow]"
            "⚠ This address belongs to a private/local or "
            "non-public address range."
            "[/bold yellow]"
        )

    else:
        console.print(
            "\n[bold yellow]"
            "⚠ This IP belongs to a special or non-global range."
            "[/bold yellow]"
        )

    if reverse_dns["hostname"]:
        console.print(
            "[green]"
            "✓ Public reverse-DNS hostname detected."
            "[/green]"
        )
    else:
        console.print(
            "[dim]"
            "No reverse-DNS hostname was detected."
            "[/dim]"
        )

    console.print(
        "\n[dim]"
        "OSINT Notice: NexTrace performs IP classification and standard "
        "reverse-DNS analysis only. An IP address does not identify a "
        "specific person or reveal their exact/live physical location. "
        "Reverse-DNS records, when available, describe public network "
        "metadata and may be incomplete or outdated."
        "[/dim]"
    )


if __name__ == "__main__":
    ip_intelligence()