# PISA Framework: Multi-Layered Security for Financial AI Applications

A comprehensive security framework implementing **PISA** (Prompt Integrity, Information boundary, Semantic verification, and Agency authorization) principles to protect GenAI applications in financial services. This repository includes the framework implementation, evaluation tools, and a complete experimental validation across 54 test scenarios.

## What is PISA?

PISA is a defense-in-depth security framework designed specifically for GenAI applications in regulated industries like financial services. It provides four complementary security layers:

### 1. **Prompt Integrity Layer**
Detects and blocks prompt injection attacks and requests for denied topics (e.g., investment advice, romantic advice). Uses AWS Bedrock Guardrails to enforce content policies.

### 2. **Information Boundary Layer**
Protects sensitive PII through automatic anonymization and prevents cross-user data access. Anonymizes email addresses, phone numbers, and credit card numbers in responses.

### 3. **Semantic Verification Layer**
Validates that AI responses are grounded in authoritative source data and detects hallucinations. Uses AWS Bedrock's grounding checks to ensure factual accuracy.

### 4. **Agency Authorization Layer**
Enforces role-based authorization limits and prevents privilege escalation attacks. Uses automated reasoning to validate that requested actions are within agent authority.

## Key Results

Comprehensive evaluation across **54 test scenarios** demonstrates:

- **Overall PISA Effectiveness**: 92.5% (49/53 successful)
- **Baseline Effectiveness**: 34.0% (18/53 successful)  
- **Improvement**: +58.5 percentage points

| Layer | Baseline | PISA | Improvement |
|-------|----------|------|-------------|
| Information Boundary | 9.1% | 90.9% | +81.8 pts |
| Prompt Integrity | 58.3% | 100% | +41.7 pts |
| Semantic Verification | 50% | 83.3% | +33.3 pts |
| Agency Authorization | 22.2% | 94.4% | +72.2 pts |

## Repository Structure

```
.
├── anycorp-demo/              # Demo application and core implementation
│   ├── AnyCorpApp.py          # Streamlit demo app
│   ├── create_guardrail.py    # Guardrail setup script
│   └── requirements.txt       # Python dependencies
│
├── pisa-experiments/          # Security evaluation experiments
│   ├── exp_information_boundary.py    # Layer 1: PII protection tests
│   ├── exp_prompt_integrity.py        # Layer 2: Prompt attack tests
│   ├── exp_semantic_verification.py   # Layer 3: Hallucination tests
│   ├── exp_agency_authorization.py    # Layer 4: Authorization tests
│   ├── ar_validator.py                # Automated reasoning validator
│   └── prompts_agency_authorization.py # Test scenarios
│
├── pisa-experiments-extended/ # Extended evaluation (54 scenarios)
│   ├── RESULTS.md             # Comprehensive results analysis
│   └── results_*.json         # Raw test results
│
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- AWS account with Bedrock access
- Python 3.8+
- AWS credentials configured (`aws configure`)

### Setup (5 minutes)

```bash
# 1. Clone and setup environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r anycorp-demo/requirements.txt

# 2. Configure AWS resources
# Update config.py with your:
# - Knowledge Base ID
# - Guardrail ID  
# - AWS Region
```

### Run Demo Application

```bash
cd anycorp-demo
streamlit run AnyCorpApp.py
```

**Test Queries:**
- ✅ Normal: "What is my overall spend in January 2024?"
- ❌ Blocked: "What stocks should I invest in?"

### Run Security Experiments

```bash
cd pisa-experiments

# Run individual layer tests
python exp_information_boundary.py
python exp_prompt_integrity.py
python exp_semantic_verification.py
python exp_agency_authorization.py
```

## Evaluation Framework

### Test Coverage (54 Scenarios)

| Layer | Tests | Attack Scenarios | Legitimate Use Cases |
|-------|-------|------------------|---------------------|
| **Information Boundary** | 12 | PII extraction, cross-user access | Normal account queries |
| **Prompt Integrity** | 15 | Prompt injection, jailbreaks, denied topics | Standard banking questions |
| **Semantic Verification** | 12 | Hallucination attempts, fabricated data | Grounded queries |
| **Agency Authorization** | 21 | Privilege escalation, social engineering | Authorized transactions |

### Attack Types Tested

**Prompt Injection:**
- System override attacks
- Role manipulation
- Instruction injection
- Jailbreak attempts
- Multi-step manipulation

**Authorization Attacks:**
- Confused deputy attacks
- Privilege escalation
- Fabricated policies
- Split transactions
- Authority impersonation

**Information Extraction:**
- PII extraction (email, phone, credit cards)
- Cross-user data access
- Social engineering

**Semantic Attacks:**
- Hallucination injection
- Fabricated merchant names
- Wrong time period queries

## Detailed Results

### Layer-by-Layer Performance

#### 1. Information Boundary Layer (12 Tests)
**Purpose**: Protect PII through anonymization and prevent cross-user access

| Metric | Baseline | PISA | Improvement |
|--------|----------|------|-------------|
| Success Rate | 9.1% | 90.9% | +81.8 pts |
| PII Anonymized | 0% | 63.6% | +63.6 pts |

**Key Findings:**
- ✅ Excellent anonymization for email, phone, credit cards
- ✅ Prevented cross-user data access
- ⚠️ Address anonymization not supported (known limitation)

#### 2. Prompt Integrity Layer (15 Tests)
**Purpose**: Detect and block prompt injection attacks and denied topics

| Metric | Baseline | PISA | Improvement |
|--------|----------|------|-------------|
| Success Rate | 58.3% | 100% | +41.7 pts |
| Attacks Blocked | 58.3% | 100% | +41.7 pts |

**Key Findings:**
- ✅ 100% detection of prompt injection attacks
- ✅ 100% blocking of denied topics (investment, romantic advice)
- ✅ Systematic policy-based protection

#### 3. Semantic Verification Layer (12 Tests)
**Purpose**: Detect hallucinations and ensure grounded responses

| Metric | Baseline | PISA | Improvement |
|--------|----------|------|-------------|
| Success Rate | 50% | 83.3% | +33.3 pts |
| Fabrications Blocked | 0% | 83.3% | +83.3 pts |

**Key Findings:**
- ✅ Detected 5/6 fabrications (83.3% detection rate)
- ⚠️ High grounding scores can fool detection for similar terms
- ⚠️ Incomplete answers may not be detected

#### 4. Agency Authorization Layer (21 Tests)
**Purpose**: Enforce role-based authorization and prevent privilege escalation

| Metric | Baseline | PISA | Improvement |
|--------|----------|------|-------------|
| Success Rate | 22.2% | 94.4% | +72.2 pts |
| Attacks Blocked | 40% | 93.3% | +53.3 pts |
| Legitimate Passed | 66.7% | 100% | +33.3 pts |

**Key Findings:**
- ✅ 93.3% attack detection rate
- ✅ 100% legitimate transaction approval (no false positives)
- ✅ Detected split transactions, fabricated policies, authority impersonation

### Attack Detection Summary

**Overall Performance:**
- Baseline: 13/39 attacks blocked (33.3%)
- PISA: 36/39 attacks blocked (92.3%)
- **Improvement: +59.0 percentage points**

**Legitimate Operations:**
- Baseline: 5/14 passed (35.7%)
- PISA: 13/14 passed (92.9%)
- **Improvement: +57.2 percentage points**

### Output Files

Experiment results are saved in JSON format:
- `pisa-experiments/results_information_boundary.json`
- `pisa-experiments/results_prompt_integrity.json`
- `pisa-experiments/results_semantic_verification.json`
- `pisa-experiments/results_agency_authorization.json`

Comprehensive analysis available in:
- `pisa-experiments-extended/RESULTS.md`

## Key Components

### 1. Demo Application (`anycorp-demo/`)
Interactive Streamlit app demonstrating PISA framework in action:
- Side-by-side comparison of baseline vs PISA-protected responses
- Real-time guardrail enforcement
- Knowledge base integration

### 2. Automated Reasoning Validator (`pisa-experiments/ar_validator.py`)
Core authorization validation engine:
- Parses LLM-extracted intent
- Validates against authorization rules
- Detects split transactions, fabricated policies
- Enforces agent-level limits

### 3. Test Scenarios (`pisa-experiments/prompts_*.py`)
Comprehensive test suites for each layer:
- Attack scenarios designed to bypass security
- Legitimate use cases to measure false positives
- Edge cases to identify limitations

### 4. Experiment Runners (`pisa-experiments/exp_*.py`)
Automated test execution scripts:
- Baseline vs PISA comparison
- Result collection and analysis
- JSON output for further processing

## Configuration

Create `pisa-experiments/config.py`:

```python
KB_ID = "YOUR_KNOWLEDGE_BASE_ID"
GUARDRAIL_ID = "YOUR_GUARDRAIL_ID"
MODEL_CLAUDE = "anthropic.claude-3-haiku-20240307-v1:0"
REGION = "us-east-1"
```

## Known Limitations

### 1. Information Boundary
- **Address Anonymization**: Not supported by current guardrail configuration
- **Impact**: 1 test failure (addresses leaked in responses)
- **Mitigation**: Document as known limitation; requires guardrail update

### 2. Semantic Verification
- **Incomplete Answers**: Partial information may not be detected as incomplete
- **Similar Terms**: High grounding scores for fabricated data with similar terms in source
- **Impact**: 2 test failures (83.3% detection rate)
- **Mitigation**: Acceptable trade-off; perfect detection unrealistic

### 3. Agency Authorization
- **Edge Cases**: Complex multi-step transactions may cause errors
- **Impact**: 1 test error (still blocked the attack)
- **Mitigation**: Improve error handling for edge cases

## Production Deployment Considerations

### Security Posture
- ✅ 92.5% overall effectiveness
- ✅ Low false positive rate (7.1%)
- ✅ High attack detection rate (92.3%)

### Performance
- Latency: +200-500ms per request (guardrail + grounding checks)
- Cost: Additional Bedrock API calls for validation
- Scalability: Fully serverless, scales with AWS Bedrock

### Monitoring
- Track grounding scores for semantic verification
- Monitor authorization violations
- Alert on guardrail blocks for security analysis

## Troubleshooting

### AWS Authentication
```bash
# Verify credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

### Rate Limiting
Add delays between API calls in experiment scripts:
```python
time.sleep(1)  # Between requests
```

### Missing Dependencies
```bash
pip install boto3 streamlit pandas
```

## Extending the Framework

### Add New Test Scenarios

Edit `pisa-experiments/prompts_agency_authorization.py`:
```python
{
    "id": "A16",
    "name": "New Attack Scenario",
    "agent_level": "Junior Banker",
    "prompt": "Your test prompt here..."
}
```

### Customize Authorization Rules

Modify `pisa-experiments/ar_validator.py`:
```python
def _load_authorization_rules(self):
    return {
        'wire_transfer': {
            'agent_limits': {
                'Junior Banker': 5000,  # Adjust limits
                'Senior Banker': 50000
            }
        }
    }
```

### Add New Security Layers

Create new experiment file following the pattern:
```python
# pisa-experiments/exp_new_layer.py
def run_test(test_id, name, prompt):
    baseline = call_model(prompt, use_protection=False)
    protected = call_model(prompt, use_protection=True)
    return compare_results(baseline, protected)
```

## Use Cases

### Financial Services
- Customer service chatbots with account access
- Loan application processing assistants
- Investment advisory platforms (with appropriate disclaimers)
- Fraud detection and prevention systems

### Healthcare
- Patient information systems
- Medical record assistants
- Appointment scheduling with PII protection

### Enterprise
- HR systems with employee data
- Customer support with access controls
- Document processing with sensitive information

## Related Work

This framework builds on:
- **OWASP Top 10 for LLM Applications**: Addresses prompt injection, data leakage, and authorization issues
- **MITRE ATLAS**: Implements defenses against adversarial ML attacks
- **AWS Bedrock Guardrails**: Leverages cloud-native security controls
- **Automated Reasoning**: Uses formal verification for authorization decisions

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{kumar2025pisa,
  title={PISA: A Multi-Layered Security Framework for GenAI Applications in Financial Services},
  author={Kumar, Aruun K. and Belsian, George and Sankararaman, Gokul S. and Srinivasan, Sriram},
  year={2025}
}
```

## Contributing

Contributions welcome! Areas of interest:
- Additional test scenarios
- New security layers
- Performance optimizations
- Integration with other LLM providers

## Contact

- **Aruun K Kumar**: aruunkumar@gmail.com
- **George Belsian**: georaj.be@gmail.com

## License

[Add your license here]

---

**Protecting GenAI applications with defense-in-depth security** 🛡️
