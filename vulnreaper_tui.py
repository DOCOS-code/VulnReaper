from rich.console import Console
from rich.prompt import Prompt
import subprocess

console = Console()

def run_idor():
    url = Prompt.ask("Target URL (e.g. https://site.com/user?id=1)")
    param = Prompt.ask("Parameter to fuzz", default="id")
    id_range = Prompt.ask("ID Range (e.g. 1-10)", default="1-10")
    keyword = Prompt.ask("Keyword to detect (optional)", default="")
    token = Prompt.ask("Bearer Token (optional)", default="")
    cookie = Prompt.ask("Session Cookie (optional)", default="")
    cmd = [
        "python", "vulnreaper.py",
        "--mode", "idor",
        "--url", url,
        "--param", param,
        "--range", id_range
    ]
    if keyword: cmd += ["--keyword", keyword]
    if token: cmd += ["--token", token]
    if cookie: cmd += ["--cookie", cookie]
    console.rule("[bold red]IDOR Scan Started")
    subprocess.call(cmd)
    console.rule("[green]IDOR Scan Complete")

def run_sqli():
    url = Prompt.ask("Target URL (e.g. https://site.com/product?item=1)")
    param = Prompt.ask("Parameter to test", default="item")
    cmd = [
        "python", "vulnreaper.py",
        "--mode", "sqli",
        "--url", url,
        "--param", param
    ]
    console.rule("[bold red]SQLi Scan Started")
    subprocess.call(cmd)
    console.rule("[green]SQLi Scan Complete")

def main_menu():
    while True:
        console.print("\n[bold cyan]⚔️ VulnReaper TUI Scanner[/bold cyan]")
        console.print(" [1] Run IDOR Scan")
        console.print(" [2] Run SQLi Scan")
        console.print(" [3] Load Previous Report")
        console.print(" [4] Settings (Coming Soon)")
        console.print(" [0] Exit")
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "0"])
        if choice == "1":
            run_idor()
        elif choice == "2":
            run_sqli()
        elif choice == "3":
            console.print("[yellow]Feature not implemented yet.[/yellow]")
        elif choice == "4":
            console.print("[yellow]Settings coming soon.[/yellow]")
        elif choice == "0":
            console.print("[bold red]Exiting VulnReaper...[/bold red]")
            break

if __name__ == "__main__":
    main_menu()
