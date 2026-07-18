# ISO 27001 Compliance Checker

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **command-line tool** that helps organisations assess their readiness against ISO 27001 Annex A controls.  
It interactively collects implementation status for each control, computes a weighted compliance score, and generates a clear, colourful summary – perfect for internal audits or gap analysis.

![Sample Output](screenshots/sample_output.png)

---

## 🔍 What It Solves

**The Problem:**  
Many organisations struggle to get a quick, objective view of their ISO 27001 compliance posture. Manual checklists are tedious, and scoring can be inconsistent.

**Our Solution:**  
This tool provides a **repeatable, standardised assessment** that:
- Guides you through all controls (from your own CSV).
- Scores each control (Implemented / Partially / Not Implemented / N/A).
- Calculates overall and per‑category compliance percentages.
- Highlights areas that need immediate attention.

**Who it's for:**  
Compliance officers, security managers, or any team preparing for ISO 27001 certification.

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/DanielMogilevskiy/ISO27001-Compliance-Checker.git
cd ISO27001-Compliance-Checker

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

Run the interactive assessment:
```bash
python -m src.main
```

Or, after installing via `setup.py`, you can use the shortcut:
```bash
pip install -e .
iso27001-check
```

You can specify a custom controls CSV and save the report:
```bash
python -m src.main --data my_controls.csv --output report.txt
```

---

## 📊 Example Output

![Sample Report](screenshots/sample_output.png)

*The report shows overall score, per‑category breakdown, and a list of controls that are not fully implemented.*

---

## 🧩 Customising the Checklist

Edit `data/iso27001_controls.csv` to add/remove/modify controls. The required columns are:
- `id` – e.g., "A.5.1"
- `category` – e.g., "Information Security Policies"
- `control_name` – short title
- `description` – detailed explanation

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

Maintained by [Daniel Mogilevskiy](https://www.linkedin.com/in/daniel-mogilevskiy/)