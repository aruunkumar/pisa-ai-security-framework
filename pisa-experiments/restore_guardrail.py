#!/usr/bin/env python3
"""Restore full guardrail configuration"""
import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

response = bedrock.update_guardrail(
    guardrailIdentifier="hye7bokv9fbw",
    name="unrelated-advice",
    description="Prevents the model from providing fiduciary or relationship advice.",
    blockedInputMessaging="I can provide general info about AnyCorp Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details.",
    blockedOutputsMessaging="I can provide general info about AnyCorp Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details.",
    topicPolicyConfig={
        'topicsConfig': [
            {
                'name': 'Fiduciary Advice',
                'definition': 'Providing personalized advice or recommendations on managing financial assets, investments, or trusts in a fiduciary capacity.',
                'examples': [
                    'What stocks should I invest in for my retirement?',
                    'Is it a good idea to put my money in a mutual fund?',
                    'How should I allocate my 401(k) investments?'
                ],
                'type': 'DENY'
            },
            {
                'name': 'Romantic Advice',
                'definition': 'Providing personalized advice on relationships, valentines day gifts, any relationship related advice.',
                'examples': [
                    'What gifts should I buy for Valentines day?',
                    'How to be a good spouse?'
                ],
                'type': 'DENY'
            }
        ]
    },
    contentPolicyConfig={
        'filtersConfig': [
            {'type': 'VIOLENCE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'PROMPT_ATTACK', 'inputStrength': 'HIGH', 'outputStrength': 'NONE'},
            {'type': 'HATE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'SEXUAL', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'INSULTS', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'MISCONDUCT', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'}
        ]
    },
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {'type': 'EMAIL', 'action': 'ANONYMIZE'},
            {'type': 'PHONE', 'action': 'ANONYMIZE'},
            {'type': 'NAME', 'action': 'ANONYMIZE'},
            {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'ANONYMIZE'},
            {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},
            {'type': 'US_BANK_ACCOUNT_NUMBER', 'action': 'BLOCK'}
        ]
    },
    contextualGroundingPolicyConfig={
        'filtersConfig': [
            {'type': 'GROUNDING', 'threshold': 0.75},
            {'type': 'RELEVANCE', 'threshold': 0.75}
        ]
    }
)

print("Guardrail restored successfully!")
print(f"Version: {response['version']}")
