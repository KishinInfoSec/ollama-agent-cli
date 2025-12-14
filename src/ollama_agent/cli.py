"""CLI interface for the Ollama cybersecurity agent"""

import typer
import os
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax
from pathlib import Path
from .agent import OllamaSecurityAgent
from .prompts import list_available_modes
from .tracing import setup_tracing, TracedAgent

app = typer.Typer(help="Ollama-powered cybersecurity agent CLI")
console = Console()


@app.command()
def interactive(
    model: str = typer.Option("llama2", help="Ollama model to use"),
    host: str = typer.Option("http://localhost:11434", help="Ollama server host"),
    mode: str = typer.Option("default", help="System prompt mode"),
    temperature: float = typer.Option(0.7, help="Model temperature (0-1)"),
    enable_tracing: bool = typer.Option(False, help="Enable OpenTelemetry tracing"),
    otlp_endpoint: str = typer.Option("http://localhost:4317", help="OTLP collector endpoint"),
):
    """Start interactive chat with the cybersecurity agent."""
    try:
        # Initialize agent
        agent = OllamaSecurityAgent(model=model, host=host, prompt_mode=mode)
        
        # Optional tracing setup
        if enable_tracing:
            console.print("[yellow]Setting up tracing...[/yellow]")
            tracer, meter = setup_tracing(
                service_name="ollama-agent-cli",
                otlp_endpoint=otlp_endpoint,
                enabled=True
            )
            if tracer:
                agent = TracedAgent(agent, tracer, meter)
                console.print("[green]✓ Tracing enabled[/green]")
        
        # Test connection
        if not agent.test_connection():
            console.print(
                f"[red]Error: Cannot connect to Ollama at {host}[/red]",
                style="bold"
            )
            console.print("[yellow]Make sure Ollama is running: ollama serve[/yellow]")
            raise typer.Exit(1)
        
        console.print(
            Panel(
                f"[bold cyan]Ollama Cybersecurity Agent[/bold cyan]\n"
                f"Model: {model}\n"
                f"Mode: {mode}\n"
                f"Temperature: {temperature}\n"
                f"Tracing: {'enabled' if enable_tracing else 'disabled'}",
                title="Agent Configuration"
            )
        )
        
        console.print("\n[yellow]Commands:[/yellow]")
        console.print("  /help    - Show help")
        console.print("  /clear   - Clear conversation history")
        console.print("  /mode    - Switch prompt mode")
        console.print("  /modes   - List available modes")
        console.print("  /models  - List available Ollama models")
        console.print("  /tools   - Show available tools")
        console.print("  /exit    - Exit the agent\n")
        
        # Interactive loop
        while True:
            try:
                user_input = Prompt.ask("[cyan]You[/cyan]").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == "/exit":
                    console.print("[yellow]Exiting...[/yellow]")
                    break
                elif user_input.lower() == "/clear":
                    agent.clear_history()
                    console.print("[green]✓ Conversation history cleared[/green]")
                    continue
                elif user_input.lower() == "/modes":
                    modes = agent.get_available_prompt_modes()
                    console.print("[cyan]Available modes:[/cyan]")
                    for m in modes:
                        console.print(f"  • {m}")
                    continue
                elif user_input.lower() == "/models":
                    try:
                        models = agent.get_available_models()
                        console.print("[cyan]Available models:[/cyan]")
                        for m in models:
                            console.print(f"  • {m}")
                    except Exception as e:
                        console.print(f"[red]Error fetching models: {str(e)}[/red]")
                    continue
                elif user_input.lower() == "/tools":
                    console.print(agent.get_tools_info())
                    continue
                elif user_input.lower() == "/help":
                    console.print("""
[bold cyan]Cybersecurity Agent Commands:[/bold cyan]

Use this agent for:
  • Threat analysis and risk assessment
  • Vulnerability analysis and remediation
  • Incident response guidance
  • Security compliance and audits
  • Secure coding practices
  • Network security architecture
  • Malware analysis
  • General cybersecurity questions

Special commands:
  /clear  - Clear conversation history
  /mode   - Switch to different analysis mode
  /modes  - List available modes
  /models - List available Ollama models
  /tools  - Show available tools
  /help   - Show this help
  /exit   - Exit the agent
""")
                    continue
                elif user_input.lower().startswith("/mode "):
                    mode_name = user_input[6:].strip()
                    if agent.set_prompt_mode(mode_name):
                        console.print(f"[green]✓ Switched to '{mode_name}' mode[/green]")
                    else:
                        console.print(f"[red]✗ Unknown mode: {mode_name}[/red]")
                        console.print("[yellow]Use /modes to see available modes[/yellow]")
                    continue
                
                # Get agent response
                console.print("\n[cyan]Agent[/cyan]: ", end="")
                try:
                    for chunk in agent.stream_response(user_input, temperature=temperature):
                        console.print(chunk, end="")
                except Exception as e:
                    console.print(f"\n[red]Error getting response: {str(e)}[/red]")
                console.print("\n")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {str(e)}[/red]")
    
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def query(
    message: str = typer.Argument(..., help="Message to send to the agent"),
    model: str = typer.Option("llama2", help="Ollama model to use"),
    host: str = typer.Option("http://localhost:11434", help="Ollama server host"),
    mode: str = typer.Option("default", help="System prompt mode"),
    temperature: float = typer.Option(0.7, help="Model temperature (0-1)"),
    enable_tracing: bool = typer.Option(False, help="Enable OpenTelemetry tracing"),
):
    """Send a single query to the cybersecurity agent."""
    try:
        agent = OllamaSecurityAgent(model=model, host=host, prompt_mode=mode)
        
        # Optional tracing
        if enable_tracing:
            tracer, meter = setup_tracing(enabled=True)
            if tracer:
                agent = TracedAgent(agent, tracer, meter)
        
        if not agent.test_connection():
            console.print(
                f"[red]Error: Cannot connect to Ollama at {host}[/red]",
                style="bold"
            )
            console.print("[yellow]Make sure Ollama is running: ollama serve[/yellow]")
            raise typer.Exit(1)
        
        console.print(f"[cyan]Query:[/cyan] {message}\n")
        console.print(f"[cyan]Response:[/cyan]\n")
        
        for chunk in agent.stream_response(message, temperature=temperature):
            console.print(chunk, end="")
        console.print()
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def list_modes():
    """List all available prompt modes."""
    modes = list_available_modes()
    console.print("[bold cyan]Available Prompt Modes:[/bold cyan]\n")
    for mode in modes:
        console.print(f"  • {mode}")


@app.command()
def check_connection(
    host: str = typer.Option("http://localhost:11434", help="Ollama server host"),
):
    """Check connection to Ollama server."""
    try:
        console.print(f"[yellow]Connecting to {host}...[/yellow]")
        agent = OllamaSecurityAgent(host=host)
        
        if agent.test_connection():
            try:
                models = agent.get_available_models()
                console.print(
                    Panel(
                        f"[green]✓ Connected to Ollama[/green]\n"
                        f"Host: {host}\n"
                        f"Available models: {len(models)}\n\n"
                        + "\n".join(f"  • {m}" for m in models[:10]),  # Show first 10
                        title="Connection Status"
                    )
                )
            except Exception as e:
                console.print(f"[yellow]Connected but could not list models: {str(e)}[/yellow]")
        else:
            console.print(
                Panel(
                    f"[red]✗ Cannot connect to Ollama[/red]\n"
                    f"Host: {host}\n\n"
                    f"Make sure:\n"
                    f"  1. Ollama is installed (https://ollama.ai)\n"
                    f"  2. Ollama is running: [bold]ollama serve[/bold]\n"
                    f"  3. The host is correct: {host}",
                    title="Connection Failed"
                )
            )
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
