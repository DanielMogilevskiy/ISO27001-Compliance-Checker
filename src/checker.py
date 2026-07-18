import csv
from typing import List, Dict
from .models import Control, ComplianceStatus

def load_controls(csv_path: str) -> List[Control]:
    controls = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            controls.append(Control(
                id=row['id'],
                category=row['category'],
                name=row['control_name'],
                description=row['description']
            ))
    return controls

def collect_status(controls: List[Control]) -> None:
    from rich.console import Console
    from rich.prompt import Prompt
    console = Console()
    
    for idx, ctrl in enumerate(controls, 1):
        console.rule(f"[bold cyan]Control {idx}/{len(controls)}[/]")
        console.print(f"[yellow]{ctrl.id}[/] – [green]{ctrl.name}[/]")
        console.print(f"[italic]{ctrl.description}[/]")
        console.print(f"Category: [blue]{ctrl.category}[/]")
        
        status = Prompt.ask(
            "Status",
            choices=["1", "2", "3", "4"],
            default="1",
            show_choices=True
        )
        mapping = {
            "1": ComplianceStatus.IMPLEMENTED,
            "2": ComplianceStatus.PARTIAL,
            "3": ComplianceStatus.NOT_IMPLEMENTED,
            "4": ComplianceStatus.NOT_APPLICABLE
        }
        ctrl.status = mapping[status]

def compute_score(controls: List[Control]) -> Dict:
    total = len(controls)
    applicable = [c for c in controls if c.status != ComplianceStatus.NOT_APPLICABLE]
    implemented = [c for c in applicable if c.status == ComplianceStatus.IMPLEMENTED]
    partial = [c for c in applicable if c.status == ComplianceStatus.PARTIAL]
    
    weighted_sum = sum(1.0 if c.status == ComplianceStatus.IMPLEMENTED else 0.5 if c.status == ComplianceStatus.PARTIAL else 0.0 for c in applicable)
    max_score = len(applicable)
    overall_pct = (weighted_sum / max_score * 100) if max_score > 0 else 0
    
    categories = {}
    for ctrl in controls:
        cat = ctrl.category
        if cat not in categories:
            categories[cat] = {'applicable': 0, 'weighted': 0}
        if ctrl.status != ComplianceStatus.NOT_APPLICABLE:
            categories[cat]['applicable'] += 1
            weight = 1.0 if ctrl.status == ComplianceStatus.IMPLEMENTED else 0.5 if ctrl.status == ComplianceStatus.PARTIAL else 0.0
            categories[cat]['weighted'] += weight
    
    cat_scores = {}
    for cat, vals in categories.items():
        if vals['applicable'] > 0:
            cat_scores[cat] = (vals['weighted'] / vals['applicable']) * 100
        else:
            cat_scores[cat] = 0.0
    
    return {
        'total_controls': total,
        'applicable_controls': len(applicable),
        'implemented': len(implemented),
        'partial': len(partial),
        'not_implemented': len([c for c in applicable if c.status == ComplianceStatus.NOT_IMPLEMENTED]),
        'overall_pct': overall_pct,
        'category_scores': cat_scores
    }

def generate_report(controls: List[Control], scores: Dict) -> str:
    from rich.table import Table
    from rich.console import Console
    from rich import box
    console = Console()
    report = []
    
    console.print("\n[bold magenta]📊 ISO 27001 Compliance Assessment Report[/]\n", file=report)
    console.print(f"Total controls assessed: {scores['total_controls']}", file=report)
    console.print(f"Applicable controls: {scores['applicable_controls']}", file=report)
    console.print(f"Implemented: {scores['implemented']}", file=report)
    console.print(f"Partially implemented: {scores['partial']}", file=report)
    console.print(f"Not implemented: {scores['not_implemented']}", file=report)
    console.print(f"[bold]Overall compliance: {scores['overall_pct']:.1f}%[/]\n", file=report)
    
    table = Table(title="Category Scores", box=box.ROUNDED)
    table.add_column("Category", style="cyan")
    table.add_column("Compliance %", justify="right", style="green")
    for cat, score in scores['category_scores'].items():
        table.add_row(cat, f"{score:.1f}%")
    console.print(table, file=report)
    
    missing = [c for c in controls if c.status in (ComplianceStatus.NOT_IMPLEMENTED, ComplianceStatus.PARTIAL)]
    if missing:
        console.print("\n[bold red]⛔ Controls needing attention:[/]", file=report)
        for c in missing:
            console.print(f"  • {c.id} – {c.name} ({c.status.value})", file=report)
    
    return "".join(report)