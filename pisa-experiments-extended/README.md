# PISA Framework - Extended Experiments

Comprehensive experimental validation of the PISA framework with 39 test scenarios across three security layers.

## Overview

This extended experiment suite provides more comprehensive coverage than the original 9-scenario test:

- **Prompt Integrity**: 15 scenarios (vs 3 original)
- **Information Boundary**: 12 scenarios (vs 3 original)
- **Semantic Verification**: 12 scenarios (vs 3 original)
- **Total**: 39 scenarios (vs 9 original)

## Test Coverage

### Prompt Integrity Layer (15 scenarios)

**Prompt Injection Attacks (5 scenarios)**
- P1: Direct Prompt Override
- P2: Role Manipulation
- P3: Instruction Injection
- P4: Delimiter Confusion
- P5: Context Switching

**Denied Topics - Fiduciary Advice (5 scenarios)**
- P6: Direct Investment Advice
- P7: Portfolio Recommendation
- P8: Specific Stock Recommendation
- P9: Market Timing Advice
- P10: Retirement Planning Advice

**Denied Topics - Other Inappropriate Content (5 scenarios)**
- P11: Romantic Relationship Advice
- P12: Medical Advice
- P13: Legal Advice
- P14: Political Opinion
- P15: Gambling Advice

### Information Boundary Layer (12 scenarios)

**PII Leakage - Email/Phone (3 scenarios)**
- I1: Email Address Query
- I2: Phone Number Query
- I3: Contact Information Query

**PII Leakage - Financial Data (3 scenarios)**
- I4: Credit Card Number
- I5: Bank Account Number
- I6: Full Financial Profile

**PII Leakage - Personal Identifiers (3 scenarios)**
- I7: Social Security Number
- I8: Driver's License
- I9: Date of Birth

**Cross-User Data Access (3 scenarios)**
- I10: Other User Profile Access
- I11: Other User Transaction Access
- I12: Other User Contact Info

### Semantic Verification Layer (12 scenarios)

**Grounded Queries - Should Pass (4 scenarios)**
- S1: Account Type Query
- S2: Credit Score Query
- S3: Highest Spending Category
- S4: Specific Transaction Query

**Fabricated Data - Should Block (4 scenarios)**
- S5: Non-existent Category
- S6: Non-existent Transaction
- S7: Wrong Month Data
- S8: Non-existent Merchant

**Partial/Incomplete Data - Edge Cases (4 scenarios)**
- S9: Total Spending Query
- S10: Transaction Count
- S11: Date Range Query
- S12: Average Transaction

## Quick Start

```bash
# Run all experiments
python run_all.py

# Or run individual layers
python exp_prompt_integrity.py
python exp_information_boundary.py
python exp_semantic_verification.py
```

## Configuration

Update `config.py` with your AWS Bedrock settings:
- Guardrail ID
- AWS Region
- Model IDs

## Results

Results are saved as JSON files:
- `results_prompt_integrity.json`
- `results_information_boundary.json`
- `results_semantic_verification.json`

## Analysis

After running experiments:
1. Analyze results: `python analyze_results.py`
2. Generate visualizations: `python create_visualizations.py`

## Expected Outcomes

**Baseline System:**
- Prompt Integrity: ~40-50% (blocks some generic attacks)
- Information Boundary: ~25-35% (some PII protection, cross-user blocking)
- Semantic Verification: ~35-45% (handles grounded queries)

**PISA System:**
- Prompt Integrity: ~95-100% (comprehensive blocking)
- Information Boundary: ~95-100% (PII anonymization + access control)
- Semantic Verification: ~80-90% (grounding checks with known limitations)
