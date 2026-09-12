import ipaddress
import re
from urllib.parse import urlparse

import dns.resolver
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def normalize_domain(value):
    """Extract and normalize a domain from user input."""

    cleaned = value.strip().lower()

    if not cleaned:
        return False, "KuchuPuchu Yaar Domain Toh Likho 😭"

    # Allow users to paste a full URL too.
    if "://" in cleaned:
        parsed = urlparse(cleaned)
        cleaned = parsed.hostname or ""

    else:
        # Remove path/query if user enters example.com/something
        cleaned = cleaned.split("/")[0]
        cleaned = cleaned.split("?")[0]
        cleaned = cleaned.split("#")[0]

        # Remove optional port.
        if ":" in cleaned:
            cleaned = cleaned.split(":")[0]

    cleaned = cleaned.strip(".")

    if cleaned.startswith("www."):
        cleaned = cleaned[4:]

    if not cleaned:
        return False, "Domain identify nahi ho paaya."

    if len(cleaned) > 253:
        return False, "Domain unusually long hai."

    try:
        ipaddress.ip_address(cleaned)
        return False, "Ye IP address hai. Domain Intelligence mein domain enter karo."
    except ValueError:
        pass

    domain_pattern = (
        r"^(?=.{1,253}$)"
        r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
        r"[a-z]{2,63}$"
    )

    if not re.fullmatch(domain_pattern, cleaned):
        return False, "Domain format valid nahi lag raha."

    return True, cleaned


def query_dns(domain, record_type):
    """Query public DNS records."""

    try:
        answers = dns.resolver.resolve(
            domain,
            record_type,
            lifetime=5,
        )

        return [
            str(answer).rstrip(".")
            for answer in answers
        ]

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return []

    except Exception:
        return []


def get_mx_records(domain):
    """Retrieve public MX records with priority."""

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
            key=lambda item: item[0]
        )

        return records

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return []

    except Exception:
        return []


def get_txt_records(domain):
    """Retrieve public TXT records."""

    try:
        answers = dns.resolver.resolve(
            domain,
            "TXT",
            lifetime=5,
        )

        records = []

        for answer in answers:
            text = b"".join(
                answer.strings
            ).decode(
                "utf-8",
                errors="replace",
            )

            records.append(text)

        return records

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ):
        return []

    except Exception:
        return []


def find_spf_record(txt_records):
    """Find the domain SPF policy from TXT records."""

    for record in txt_records:
        if record.lower().startswith("v=spf1"):
            return record

    return None


def get_dmarc_record(domain):
    """Retrieve the public DMARC policy."""

    records = get_txt_records(
        f"_dmarc.{domain}"
    )

    for record in records:
        if record.lower().startswith("v=dmarc1"):
            return record

    return None


def detect_mail_provider(mx_records):
    """Estimate mail provider using public MX hostnames."""

    if not mx_records:
        return "Unknown"

    mx_text = " ".join(
        server.lower()
        for _, server in mx_records
    )

    providers = {
        "google.com": "Google Workspace / Gmail",
        "googlemail.com": "Google Workspace / Gmail",
        "protection.outlook.com": "Microsoft 365 / Outlook",
        "outlook.com": "Microsoft 365 / Outlook",
        "zoho.com": "Zoho Mail",
        "yahoodns.net": "Yahoo Mail",
        "icloud.com": "Apple iCloud Mail",
        "protonmail.ch": "Proton Mail",
        "protonmail.com": "Proton Mail",
    }

    for signal, provider in providers.items():
        if signal in mx_text:
            return provider

    return "Other / Custom Infrastructure"


def format_records(records):
    """Format multiple DNS records for Rich output."""

    if not records:
        return "Not detected"

    return "\n".join(records)


def domain_intelligence():
    """Run NexTrace Domain Intelligence."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace • Domain Intelligence[/bold cyan]\n"
            "[dim]Public DNS and mail-security analysis[/dim]",
            border_style="cyan",
        )
    )

    domain_input = console.input(
        "\n[bold yellow]Enter domain (e.g. example.com): [/bold yellow]"
    )

    is_valid, result = normalize_domain(
        domain_input
    )

    if not is_valid:
        console.print(
            f"\n[bold red]Error:[/bold red] {result}"
        )
        return

    domain = result

    console.print(
        f"\n[dim]Analysing public DNS infrastructure for "
        f"{domain}...[/dim]"
    )

    # Core DNS records
    a_records = query_dns(
        domain,
        "A",
    )

    aaaa_records = query_dns(
        domain,
        "AAAA",
    )

    ns_records = query_dns(
        domain,
        "NS",
    )

    cname_records = query_dns(
        domain,
        "CNAME",
    )

    mx_records = get_mx_records(
        domain
    )

    txt_records = get_txt_records(
        domain
    )

    # Email-security policies
    spf_record = find_spf_record(
        txt_records
    )

    dmarc_record = get_dmarc_record(
        domain
    )

    mail_provider = detect_mail_provider(
        mx_records
    )

    domain_resolves = bool(
        a_records
        or aaaa_records
        or ns_records
        or mx_records
    )

    table = Table(
        title="NexTrace Domain Intelligence Report",
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

    # Domain information
    table.add_row(
        "Input",
        domain_input,
    )

    table.add_row(
        "Normalized Domain",
        domain,
    )

    table.add_row(
        "DNS Status",
        "Resolved" if domain_resolves else "Not resolved",
    )

    table.add_section()

    # DNS infrastructure
    table.add_row(
        "IPv4 (A)",
        format_records(a_records),
    )

    table.add_row(
        "IPv6 (AAAA)",
        format_records(aaaa_records),
    )

    table.add_row(
        "Nameservers (NS)",
        format_records(ns_records),
    )

    table.add_row(
        "CNAME",
        format_records(cname_records),
    )

    table.add_section()

    # Mail infrastructure
    if mx_records:
        formatted_mx = "\n".join(
            f"{priority}  {server}"
            for priority, server in mx_records
        )
    else:
        formatted_mx = "Not detected"

    table.add_row(
        "MX Servers",
        formatted_mx,
    )

    table.add_row(
        "Estimated Mail Provider",
        mail_provider,
    )

    table.add_section()

    # Security signals
    table.add_row(
        "SPF",
        "Detected" if spf_record else "Not detected",
    )

    if spf_record:
        table.add_row(
            "SPF Policy",
            spf_record,
        )

    table.add_row(
        "DMARC",
        "Detected" if dmarc_record else "Not detected",
    )

    if dmarc_record:
        table.add_row(
            "DMARC Policy",
            dmarc_record,
        )

    table.add_row(
        "TXT Record Count",
        str(len(txt_records)),
    )

    console.print()
    console.print(table)

    # Simple interpretation
    if domain_resolves:
        console.print(
            "\n[bold green]"
            "✓ Public DNS infrastructure detected."
            "[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]"
            "✗ NexTrace could not detect public DNS infrastructure "
            "for this domain."
            "[/bold red]"
        )

    if mx_records:
        console.print(
            "[green]✓ MX mail infrastructure detected.[/green]"
        )
    else:
        console.print(
            "[yellow]⚠ MX mail infrastructure not detected.[/yellow]"
        )

    if spf_record and dmarc_record:
        console.print(
            "[green]"
            "✓ SPF and DMARC policies are publicly configured."
            "[/green]"
        )

    elif spf_record or dmarc_record:
        console.print(
            "[yellow]"
            "⚠ Only part of the checked mail-security policy "
            "configuration was detected."
            "[/yellow]"
        )

    else:
        console.print(
            "[yellow]"
            "⚠ SPF and DMARC policies were not detected."
            "[/yellow]"
        )

    console.print(
        "\n[dim]"
        "OSINT Notice: NexTrace analyses publicly available DNS "
        "metadata only. DNS records describe domain infrastructure "
        "and do not identify a private individual or prove ownership. "
        "SPF and DMARC detection indicates published policies, not a "
        "complete security assessment."
        "[/dim]"
    )