# PISA Framework Experiments

Experimental validation of the PISA (Prompt Integrity, Information Boundary, Semantic Verification, Agency Authorization) framework using AWS Bedrock Guardrails.

## Quick Start

```bash
# Run all experiments
python run_all.py

# Analyze results
python analyze_results.py

# Generate visualizations
python create_overall_chart.py
python create_layer_chart.py
```

## Files

### Experiment Scripts
- `exp_prompt_integrity.py` - Tests prompt injection and denied topics (3 scenarios)
- `exp_information_boundary.py` - Tests PII protection and cross-user access (3 scenarios)
- `exp_semantic_verification.py` - Tests grounding and hallucination detection (3 scenarios)
- `run_all.py` - Runs all experiments sequentially

### Analysis & Visualization
- `analyze_results.py` - Analyzes experiment results and generates metrics
- `create_overall_chart.py` - Creates overall effectiveness comparison chart
- `create_layer_chart.py` - Creates layer-by-layer comparison chart

### Results
- `results_prompt_integrity.json` - Raw experiment results for Prompt Integrity layer
- `results_information_boundary.json` - Raw experiment results for Information Boundary layer
- `results_semantic_verification.json` - Raw experiment results for Semantic Verification layer
- `analysis_results.json` - Computed metrics and scores
- `RESULTS.md` - Comprehensive results documentation with tables and IEEE paper writeup
- `pisa_overall_effectiveness.png` - Overall baseline vs PISA comparison chart
- `pisa_layer_comparison.png` - Layer-by-layer comparison chart

### Configuration
- `config.py` - AWS Bedrock configuration (guardrail ID, models, region)
- `restore_guardrail.py` - Utility to restore guardrail to original state

## Results Summary

**Overall Protection Score**: Baseline 44.4/100 → PISA 94.4/100 (+50.0 points)

| Layer | Baseline | PISA | Improvement |
|-------|----------|------|-------------|
| Prompt Integrity | 66.7/100 | 100/100 | +33.3 points |
| Information Boundary | 33.3/100 | 100/100 | +66.7 points |
| Semantic Verification | 33.3/100 | 83.3/100 | +50.0 points |

## Test Scenarios

### Prompt Integrity (3 tests)
- P1: Prompt injection attack detection
- P2: Denied topic - fiduciary advice
- P3: Denied topic - romantic advice

### Information Boundary (3 tests)
- I1: PII anonymization - email/phone
- I2: PII anonymization - credit card
- I3: Cross-user data access prevention

### Semantic Verification (3 tests)
- S1: Grounded query (correct data)
- S2: Fabricated data detection
- S3: Incomplete answer (limitation test)

## Requirements

```bash
pip install boto3 matplotlib numpy
```

## AWS Configuration

Update `config.py` with your:
- Guardrail ID
- AWS Region
- Model ARNs (if different)

## Notes

- Experiments use AWS Bedrock with Guardrails
- Baseline tests run without guardrails
- PISA tests run with guardrails enabled
- All results are reproducible by re-running the experiment scripts
