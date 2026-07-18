import sys
import argparse
from pathlib import Path
from .checker import load_controls, collect_status, compute_score, generate_report
from rich.console import Console

def main():
    parser = argparse.ArgumentParser(description="ISO 27001 Compliance Checker")
    parser.add_argument(
        "--data",
        default="data/iso27001_controls.csv",
        help="Path to the CSV controls file"
    )
    parser.add_argument(
        "--output",
        help="Optional output file for the report (e.g., report.txt)"
    )
    args = parser.parse_args()
    
    console = Console()
    data_path = Path(args.data)
    if not data_path.exists():
        console.print(f"[red]Error: Data file '{data_path}' not found.[/]")
        sys.exit(1)
    
    controls = load_controls(str(data_path))
    console.print(f"[green]Loaded {len(controls)} controls from {data_path}[/]")
    
    collect_status(controls)
    scores = compute_score(controls)
    report = generate_report(controls, scores)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        console.print(f"\n[green]Report saved to {args.output}[/]")
    else:
        console.print(report)

if __name__ == "__main__":
    main()