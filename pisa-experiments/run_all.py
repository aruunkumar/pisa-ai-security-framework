#!/usr/bin/env python3
"""
Run all PISA layer experiments
"""
import subprocess
import sys

print("="*70)
print("PISA FRAMEWORK EXPERIMENTS")
print("="*70)

experiments = [
    ("Prompt Integrity Layer", "exp_prompt_integrity.py"),
    ("Information Boundary Layer", "exp_information_boundary.py"),
    ("Semantic Verification Layer", "exp_semantic_verification.py"),
]

for name, script in experiments:
    print(f"\n\n{'#'*70}")
    print(f"# Running: {name}")
    print(f"{'#'*70}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"ERROR: {script} failed")

print("\n\n" + "="*70)
print("ALL EXPERIMENTS COMPLETE")
print("="*70)
print("\nResults saved to:")
print("  - results_prompt_integrity.json")
print("  - results_information_boundary.json")
print("  - results_semantic_verification.json")
