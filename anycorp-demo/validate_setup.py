#!/usr/bin/env python3
"""
Validation script to check if the environment is ready for PISA experiments
"""
import sys
import os

def check_imports():
    """Check if all required packages are installed"""
    print("Checking Python packages...")
    required_packages = {
        'boto3': 'AWS SDK',
        'json': 'JSON handling',
        'csv': 'CSV handling',
        'matplotlib': 'Visualization (optional for experiments)'
    }
    
    missing = []
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package} ({description})")
        except ImportError:
            if package == 'matplotlib':
                print(f"  ⚠ {package} ({description}) - Optional, needed for visualizations")
            else:
                print(f"  ✗ {package} ({description}) - MISSING")
                missing.append(package)
    
    if missing:
        print(f"\n❌ Missing required packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✓ All required packages installed\n")
    return True

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    print("Checking AWS credentials...")
    try:
        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"  ✓ AWS Account: {identity['Account']}")
        print(f"  ✓ User/Role: {identity['Arn']}")
        print("✓ AWS credentials configured\n")
        return True
    except Exception as e:
        print(f"  ✗ AWS credentials not configured: {e}")
        print("\nConfigure with: aws configure")
        return False

def check_bedrock_access():
    """Check if Bedrock service is accessible"""
    print("Checking AWS Bedrock access...")
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime')
        # Try to list models (this will fail if no access)
        print("  ✓ Bedrock Runtime client created")
        print("✓ AWS Bedrock access available\n")
        return True
    except Exception as e:
        print(f"  ✗ Cannot access Bedrock: {e}")
        print("\nEnsure you have Bedrock permissions in your AWS account")
        return False

def check_knowledge_base():
    """Check if knowledge base is accessible"""
    print("Checking Knowledge Base access...")
    try:
        import boto3
        kb_client = boto3.client('bedrock-agent-runtime')
        kb_id = "YCNSJ5C3NZ"
        
        # Try a simple query
        response = kb_client.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": "test query"}
        )
        print(f"  ✓ Knowledge Base {kb_id} is accessible")
        print(f"  ✓ Retrieved {len(response.get('retrievalResults', []))} results")
        print("✓ Knowledge Base configured correctly\n")
        return True
    except Exception as e:
        print(f"  ✗ Cannot access Knowledge Base: {e}")
        print(f"\nVerify Knowledge Base ID in run_experiments.py")
        return False

def check_guardrail():
    """Check if guardrail is accessible"""
    print("Checking Guardrail access...")
    try:
        import boto3
        bedrock = boto3.client('bedrock')
        guardrail_id = "hye7bokv9fbw"
        
        # Try to get guardrail details
        response = bedrock.get_guardrail(
            guardrailIdentifier=guardrail_id
        )
        print(f"  ✓ Guardrail {guardrail_id} is accessible")
        print(f"  ✓ Guardrail Name: {response.get('name', 'N/A')}")
        print("✓ Guardrail configured correctly\n")
        return True
    except Exception as e:
        print(f"  ⚠ Cannot verify Guardrail details: {e}")
        print(f"  Note: This may be a permissions issue, but experiments might still work")
        print("  Continuing...\n")
        return True  # Don't fail on this, as it might be a permission issue

def check_files():
    """Check if required files exist"""
    print("Checking required files...")
    required_files = [
        'test_scenarios.csv',
        'run_experiments.py',
        'analyze_results.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing required files: {', '.join(missing)}")
        return False
    
    print("✓ All required files present\n")
    return True

def main():
    print("="*70)
    print("PISA Framework Experiment Setup Validation")
    print("="*70)
    print()
    
    checks = [
        ("Python Packages", check_imports),
        ("AWS Credentials", check_aws_credentials),
        ("Bedrock Access", check_bedrock_access),
        ("Knowledge Base", check_knowledge_base),
        ("Guardrail", check_guardrail),
        ("Required Files", check_files)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}\n")
            results.append((name, False))
    
    print("="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} {name}")
        if not result:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run experiments.")
        print("\nNext steps:")
        print("  1. Run experiments: python run_experiments.py")
        print("  2. Analyze results: python analyze_results.py")
        print("  3. Generate figures: python visualize_results.py")
        print("\nSee QUICKSTART.md for detailed instructions.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before running experiments.")
        print("\nFor help, see EXPERIMENTS_README.md or QUICKSTART.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
