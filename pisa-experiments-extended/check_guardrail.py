#!/usr/bin/env python3
"""
Check and display current guardrail configuration
"""
import boto3
import json
from config import GUARDRAIL_ID, REGION

bedrock = boto3.client('bedrock', region_name=REGION)

def check_guardrail():
    """Check current guardrail configuration"""
    try:
        response = bedrock.get_guardrail(
            guardrailIdentifier=GUARDRAIL_ID,
            guardrailVersion='DRAFT'
        )
        
        print("="*70)
        print("CURRENT GUARDRAIL CONFIGURATION")
        print("="*70)
        print(f"\nGuardrail ID: {response['guardrailId']}")
        print(f"Name: {response['name']}")
        print(f"Status: {response['status']}")
        
        # Check Sensitive Information Filter
        if 'sensitiveInformationPolicyConfig' in response:
            print("\n### SENSITIVE INFORMATION POLICY ###")
            config = response['sensitiveInformationPolicyConfig']
            
            for pii in config.get('piiEntitiesConfig', []):
                print(f"  - {pii['type']}: {pii['action']}")
        
        # Check Content Policy
        if 'contentPolicyConfig' in response:
            print("\n### CONTENT POLICY ###")
            config = response['contentPolicyConfig']
            for filter in config.get('filtersConfig', []):
                print(f"  - {filter['type']}: {filter['inputStrength']}/{filter['outputStrength']}")
        
        # Check Topic Policy
        if 'topicPolicyConfig' in response:
            print("\n### TOPIC POLICY ###")
            config = response['topicPolicyConfig']
            for topic in config.get('topicsConfig', []):
                print(f"  - {topic['name']}: {topic['type']}")
        
        # Check Word Policy
        if 'wordPolicyConfig' in response:
            print("\n### WORD POLICY ###")
            config = response['wordPolicyConfig']
            if config.get('wordsConfig'):
                print(f"  - Blocked words: {len(config['wordsConfig'])}")
            if config.get('managedWordListsConfig'):
                print(f"  - Managed lists: {len(config['managedWordListsConfig'])}")
        
        # Check Contextual Grounding
        if 'contextualGroundingPolicyConfig' in response:
            print("\n### CONTEXTUAL GROUNDING POLICY ###")
            config = response['contextualGroundingPolicyConfig']
            for filter in config.get('filtersConfig', []):
                print(f"  - {filter['type']}: threshold={filter['threshold']}")
        
        # Check Blocked Messaging
        if 'blockedInputMessaging' in response:
            print(f"\n### BLOCKED INPUT MESSAGE ###")
            print(f"  {response['blockedInputMessaging'][:100]}...")
        
        if 'blockedOutputsMessaging' in response:
            print(f"\n### BLOCKED OUTPUT MESSAGE ###")
            print(f"  {response['blockedOutputsMessaging'][:100]}...")
        
        print("\n" + "="*70)
        
        # Save full config
        with open('guardrail_config.json', 'w') as f:
            json.dump(response, f, indent=2, default=str)
        print("\nFull configuration saved to guardrail_config.json")
        
    except Exception as e:
        print(f"Error checking guardrail: {e}")

if __name__ == "__main__":
    check_guardrail()
