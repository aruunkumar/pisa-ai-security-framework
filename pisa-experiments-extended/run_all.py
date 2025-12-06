#!/usr/bin/env python3
"""
Run all PISA experiments in sequence
"""
import subprocess
import sys

experiments = [
    ("Prompt Integrity", "exp_prompt_integrity.py"),
    ("Information Boundary", "exp_information_boundary.py"),
    ("Semantic Verification", "exp_semantic_verification.py")
]

def run_experiment(name, script):
    """Run a single experiment script"""
    print(f"\n{'='*60}")
    print(f"Running {name} Experiments")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False
        )
        print(f"\n✓ {name} experiments completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {name} experiments failed: {e}")
        return False

def main():
    """Run all experiments"""
    print("="*60)
    print("PISA FRAMEWORK - EXTENDED EXPERIMENTS")
    print("="*60)
    print("\nRunning 39 total scenarios:")
    print("  - Prompt Integrity: 15 scenarios")
    print("  - Information Boundary: 12 scenarios")
    print("  - Semantic Verification: 12 scenarios")
    print()
    
    results = {}
    for name, script in experiments:
        results[name] = run_experiment(name, script)
    
    # Summary
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    for name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_success = all(results.values())
    if all_success:
        print("\n✓ All experiments completed successfully!")
        print("\nNext steps:")
        print("  1. Run: python analyze_results.py")
        print("  2. Run: python create_visualizations.py")
    else:
        print("\n✗ Some experiments failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
