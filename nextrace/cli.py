from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from nextrace.phone import phone_intelligence
from nextrace.vehicle import vehicle_intelligence
from nextrace.username import username_search
from nextrace.email_intel import email_intelligence
from nextrace.domain_intel import domain_intelligence
from nextrace.ip_intel import ip_intelligence
from nextrace.identity_validator import identity_validator

console = Console()


def show_banner():
    """Display the NexTrace banner."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]NexTrace[/bold cyan]\n"
            "[white]OSINT Intelligence Toolkit[/white]\n"
            "[dim]Developed by voidx[/dim]",
            border_style="cyan",
        )
    )


def show_menu():
    """Display the main NexTrace menu."""

    console.print("\n[bold]Select a module:[/bold]\n")

    console.print("[cyan][1][/cyan] Phone Intelligence")
    console.print("[cyan][2][/cyan] Vehicle Intelligence")
    console.print("[cyan][3][/cyan] Username Search")
    console.print("[cyan][4][/cyan] Email Intelligence")
    console.print("[cyan][5][/cyan] Domain Intelligence")
    console.print("[cyan][6][/cyan] IP Intelligence")
    console.print("[cyan][7][/cyan] Aadhaar & PAN Validator")
    console.print("[cyan][0][/cyan] Exit")


def wait_for_return():
    """Pause before returning to the main menu."""

    console.print()

    console.input(
        "[dim]Press Enter to return to NexTrace...[/dim]"
    )


def main():
    """Run the NexTrace CLI."""

    while True:
        console.clear()

        show_banner()
        show_menu()

        choice = console.input(
            "\n[bold yellow]Enter your choice: [/bold yellow]"
        ).strip()

        if choice == "0":
            console.print(
                "\n[bold cyan]NexTrace closed.[/bold cyan]"
            )

            console.print(
                "[dim]Stay curious. Investigate responsibly.[/dim]\n"
            )

            break

        console.clear()

        if choice == "1":
            phone_intelligence()

        elif choice == "2":
            vehicle_intelligence()

        elif choice == "3":
            username_search()

        elif choice == "4":
            email_intelligence()

        elif choice == "5":
            domain_intelligence()

        elif choice == "6":
            ip_intelligence()

        elif choice == "7":
            identity_validator()

        else:
            console.print()

            console.print(
                Panel.fit(
                    "[bold yellow]"
                    "KuchuPuchu Valid Option Toh Choose Karo 😭"
                    "[/bold yellow]",
                    border_style="yellow",
                )
            )

        wait_for_return()

        console.print(
            Rule(style="dim")
        )


if __name__ == "__main__":
    main()