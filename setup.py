from setuptools import setup, find_packages

setup(
    name="iso27001-compliance-checker",
    version="0.1.0",
    description="Assess ISO 27001 compliance readiness interactively.",
    author="Daniel Mogilevskiy",
    packages=find_packages(),
    install_requires=["rich>=13.0.0"],
    entry_points={
        "console_scripts": [
            "iso27001-check = src.main:main",
        ]
    },
    python_requires=">=3.8",
)