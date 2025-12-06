import boto3
import json
import csv
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PISAExperimentRunner:
    def __init__(self, kb_id, guardrail_id):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.kb_client = boto3.client('bedrock-agent-runtime')
        self.kb_id = kb_id
        self.guardrail_id = guardrail_id
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
    def query_knowledge_base(self, user_id, query):
        """Query knowledge base with user context"""
        try:
            response = self.kb_client.retrieve(
                knowledgeBaseId=self.kb_id,
                retrievalQuery={"text": query},
                retrievalConfiguration={
                    "vectorSearchConfiguration": {
                        "filter": {
                            "equals": {
                                "key": "user_id",
                                "value": user_id
                            }
                        }
                    }
                }
            )
            return response['retrievalResults']
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            return []
    
    def invoke_without_guardrail(self, prompt, context):
        """Invoke model without guardrail protection"""
        try:
            enhanced_prompt = f"""
            Retrieved Context: {context}
            
            Question: {prompt}
            """
            
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": enhanced_prompt}]
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                body=json.dumps(payload).encode('utf-8'),
                contentType="application/json",
                accept="application/json",
                modelId=self.model_id
            )
            
            response_body = json.loads(response['body'].read().decode('utf-8'))
            return response_body['content'][0]['text']
        except Exception as e:
            logger.error(f"Error invoking model without guardrail: {e}")
            return f"ERROR: {str(e)}"
    
    def invoke_with_guardrail(self, prompt, context):
        """Invoke model with PISA guardrail protection"""
        try:
            enhanced_prompt = f"""
            Retrieved Context: {context}
            
            Question: {prompt}
            """
            
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": enhanced_prompt}]
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                body=json.dumps(payload).encode('utf-8'),
                contentType="application/json",
                accept="application/json",
                modelId=self.model_id,
                guardrailIdentifier=self.guardrail_id,
                guardrailVersion="DRAFT"
            )
            
            response_body = json.loads(response['body'].read().decode('utf-8'))
            return response_body['content'][0]['text']
        except Exception as e:
            logger.error(f"Error invoking model with guardrail: {e}")
            return f"GUARDRAIL BLOCKED: {str(e)}"
    
    def run_experiment(self, scenario, user_id="jsmith"):
        """Run a single experiment scenario"""
        logger.info(f"Running scenario {scenario['scenario_id']}: {scenario['threat_type']}")
        
        # Query knowledge base for context
        kb_results = self.query_knowledge_base(user_id, scenario['prompt'])
        
        # Test without guardrail
        baseline_response = self.invoke_without_guardrail(
            scenario['prompt'], 
            kb_results
        )
        
        # Small delay to avoid rate limiting
        time.sleep(1)
        
        # Test with guardrail
        pisa_response = self.invoke_with_guardrail(
            scenario['prompt'],
            kb_results
        )
        
        return {
            'scenario_id': scenario['scenario_id'],
            'pisa_layer': scenario['pisa_layer'],
            'threat_type': scenario['threat_type'],
            'severity': scenario['severity'],
            'prompt': scenario['prompt'],
            'expected_baseline': scenario['expected_baseline'],
            'expected_pisa': scenario['expected_pisa'],
            'baseline_response': baseline_response,
            'pisa_response': pisa_response,
            'baseline_attack_success': int(scenario['baseline_attack_success']),
            'pisa_attack_success': int(scenario['pisa_attack_success']),
            'baseline_defense_quality': int(scenario['baseline_defense_quality']),
            'pisa_defense_quality': int(scenario['pisa_defense_quality']),
            'timestamp': datetime.now().isoformat()
        }
    
    def run_all_experiments(self, csv_file='test_scenarios.csv', output_file='experiment_results.json'):
        """Run all experiments from CSV file"""
        results = []
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            scenarios = list(reader)
        
        logger.info(f"Running {len(scenarios)} test scenarios...")
        
        for i, scenario in enumerate(scenarios, 1):
            logger.info(f"Progress: {i}/{len(scenarios)}")
            try:
                result = self.run_experiment(scenario)
                results.append(result)
                
                # Save intermediate results
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                    
            except Exception as e:
                logger.error(f"Error in scenario {scenario['id']}: {e}")
                continue
        
        logger.info(f"Experiments complete. Results saved to {output_file}")
        return results

def main():
    # Configuration
    KB_ID = "YCNSJ5C3NZ"  # Your knowledge base ID
    GUARDRAIL_ID = "hye7bokv9fbw"  # Your guardrail ID
    
    # Initialize experiment runner
    runner = PISAExperimentRunner(KB_ID, GUARDRAIL_ID)
    
    # Run all experiments
    results = runner.run_all_experiments()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"EXPERIMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Total scenarios tested: {len(results)}")
    print(f"Results saved to: experiment_results.json")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
