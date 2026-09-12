import re

import dns.resolver
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


# Common disposable / temporary email domains.
# Later we can move this into a larger dedicated dataset.
DISPOSABLE_DOMAINS = {
    "10minutemail.com",
    "guerrillamail.com",
    "mailinator.com",
    "tempmail.com",
    "yopmail.com",
}


def validate_email(email):
    """Perform basic email syntax validation."""

    cleaned = email.strip().lower()

    if not cleaned:
        return False, "KuchuPuchu Yaar Email Toh Likho 😭"

    if len(cleaned) > 254:
        return False, "Email address unusually long hai."

    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, cleaned):
        return False, "Email format valid nahi lag raha."

    return True, cleaned


def get_dns_records(domain, record_type):
    """Retrieve public DNS records for a domain."""

    try:
        answers = dns.resolver.resolve(
            domain,
            record_type,
            lifetime=5,
        )

        return [str(answer).rstrip(".") for answer in answers]

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return []


def get_mx_records(domain):
    """Retrieve and sort public MX records."""

    try:
        answers = dns.resolver.resolve(
            domain,
            "MX",
            lifetime=5,
        )

        records = []

        for answer in answers:
            records.append(
                (
                    answer.preference,
                    str(answer.exchange).rstrip("."),
                )
            )

        records.sort(
            key=lambda record: record[0]
        )

        return records

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return []


def detect_mail_provider(mx_records):
    """Estimate the mail provider from public MX hostnames."""

    if not mx_records:
        return "Unknown"

    mx_text = " ".join(
        server.lower()
        for _, server in mx_records
    )

    providers = {
        "google.com": "Google Workspace / Gmail",
        "googlemail.com": "Google Workspace / Gmail",
        "outlook.com": "Microsoft 365 / Outlook",
        "protection.outlook.com": "Microsoft 365 / Outlook",
        "zoho.com": "Zoho Mail",
        "icloud.com": "Apple iCloud Mail",
        "yahoodns.net": "Yahoo Mail",
        "protonmail.ch": "Proton Mail",
        "protonmail.com": "Proton Mail",
    }

    for signal, provider in providers.items():
        if signal in mx_text:
            return provider

    return "Other / Custom Mail Infrastructure"


def email_intelligence():
    """Run NexTrace Email Intelligence."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Email Intelligence[/bold cyan]\n"
            "[dim]Public email-domain and mail infrastructure analysis[/dim]",
            border_style="cyan",
        )
    )

    email_input = console.input(
        "\n[bold yellow]Enter email address: [/bold yellow]"
    )

    is_valid, result = validate_email(
        email_input
    )

    if not is_valid:
        console.print(
            f"\n[bold red]Error:[/bold red] {result}"
        )
        return

    email = result

    local_part, domain = email.rsplit(
        "@",
        1,
    )

    console.print(
        f"\n[dim]Analysing public mail infrastructure for "
        f"{domain}...[/dim]"
    )

    # Public DNS intelligence
    mx_records = get_mx_records(domain)

    a_records = get_dns_records(
        domain,
        "A",
    )

    aaaa_records = get_dns_records(
        domain,
        "AAAA",
    )

    # Disposable-domain signal
    disposable = (
        domain in DISPOSABLE_DOMAINS
    )

    # Provider estimation from MX records
    mail_provider = detect_mail_provider(
        mx_records
    )

    # Domain existence signal
    domain_resolves = bool(
        mx_records
        or a_records
        or aaaa_records
    )

    # Mail receiving capability signal
    accepts_mail_signal = bool(
        mx_records
    )

    table = Table(
        title="NexTrace Email Intelligence Report",
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

    # Email structure
    table.add_row(
        "Input",
        email_input,
    )

    table.add_row(
        "Normalized Email",
        email,
    )

    table.add_row(
        "Local Part",
        local_part,
    )

    table.add_row(
        "Domain",
        domain,
    )

    table.add_section()

    # Validation signals
    table.add_row(
        "Syntax Valid",
        "Yes",
    )

    table.add_row(
        "Domain Resolves",
        "Yes" if domain_resolves else "No",
    )

    table.add_row(
        "MX Records Present",
        "Yes" if mx_records else "No",
    )

    table.add_row(
        "Mail Receiving Signal",
        "Available" if accepts_mail_signal else "Not detected",
    )

    table.add_row(
        "Disposable Domain",
        "Yes" if disposable else "No",
    )

    table.add_section()

    # Mail infrastructure
    table.add_row(
        "Estimated Mail Provider",
        mail_provider,
    )

    if mx_records:
        formatted_mx = "\n".join(
            f"{priority}  {server}"
            for priority, server in mx_records
        )

        table.add_row(
            "MX Servers",
            formatted_mx,
        )

    else:
        table.add_row(
            "MX Servers",
            "None detected",
        )

    if a_records:
        table.add_row(
            "Domain IPv4",
            ", ".join(a_records),
        )

    else:
        table.add_row(
            "Domain IPv4",
            "Not detected",
        )

    if aaaa_records:
        table.add_row(
            "Domain IPv6",
            ", ".join(aaaa_records),
        )

    else:
        table.add_row(
            "Domain IPv6",
            "Not detected",
        )

    console.print()
    console.print(table)

    # Interpretation
    if mx_records:
        console.print(
            "\n[bold green]"
            "✓ Public MX records indicate that the domain has "
            "mail-receiving infrastructure."
            "[/bold green]"
        )

    elif domain_resolves:
        console.print(
            "\n[bold yellow]"
            "⚠ Domain resolves publicly, but NexTrace did not "
            "detect MX records."
            "[/bold yellow]"
        )

    else:
        console.print(
            "\n[bold red]"
            "✗ NexTrace could not detect public DNS infrastructure "
            "for this domain."
            "[/bold red]"
        )

    console.print(
        "\n[dim]"
        "OSINT Notice: These results analyse public DNS and email-domain "
        "metadata only. A valid format or working MX configuration does "
        "not prove that the specific mailbox exists, is active, or belongs "
        "to a particular person. NexTrace does not log in to accounts, "
        "access inboxes, or bypass authentication."
        "[/dim]"
    )