"""
Configuration for PISA experiments - matches original setup
"""

# AWS Bedrock Configuration
KB_ID = "YCNSJ5C3NZ"
GUARDRAIL_ID = "hye7bokv9fbw"
GUARDRAIL_VERSION = "DRAFT"
REGION = "us-east-1"

# Model Configuration
MODEL_CLAUDE = "anthropic.claude-3-haiku-20240307-v1:0"
MODEL_TITAN = "amazon.titan-text-lite-v1"  # Used for semantic verification to allow hallucination
