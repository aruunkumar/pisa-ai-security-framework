import streamlit as st
import boto3
import json
import logging
from datetime import datetime
import concurrent.futures

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_bedrock():
    return boto3.client('bedrock-runtime')

def initialize_knowledge_base():
    return boto3.client('bedrock-agent-runtime')

def query_knowledge_base(client, kb_id, user_id, query):
    try:
        response = client.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={
                "text": query
            },
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
        return None

def invoke_model_without_guardrail(client, prompt, retrieved_context):
    try:
        enhanced_prompt = f"""
        Retrieved Context: {retrieved_context}
        Follow these instructions strictly:
        1. If the retrieved context do not have information, then provide your knowledge to answer questions
        2. Make sure to provide meaningful human assistant like response 
        3. Do not include information regarding context that is retrieved.
        4. If the context do not have information, just state the response in numbered points. For example do not specify statements like "Since the retrieved context does not contain any information about gift ideas for Valentine's Day, I will provide my own knowledge to answer this question." in the beginning of your response
        
        Question: {prompt}
        """

        payload = {
            "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
            "contentType": "application/json",
            "accept": "application/json",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": enhanced_prompt
                            }
                        ]
                    }
                ]
            }
        }

        body_bytes = json.dumps(payload['body']).encode('utf-8')
        
        response = client.invoke_model(
            body=body_bytes,
            contentType=payload['contentType'],
            accept=payload['accept'],
            modelId=payload['modelId']
        )

        response_body = json.loads(response['body'].read().decode('utf-8'))
        return json.dumps(response_body['content'][0]['text'], indent=2)
    except Exception as e:
        logger.error(f"Error invoking model without guardrail: {e}")
        return str(e)

def invoke_model_with_guardrail(client, prompt, retrieved_context, guardrail_id):
    try:
        enhanced_prompt = f"""
        Retrieved Context: {retrieved_context}
        Follow these instructions strictly:
        1. Make sure to provide meaningful human assistant like response 
        2. Do not include information regarding context that is retrieved.
        3. Strictly answer based on the context information. 
        
        Question: {prompt}
        
        """

        payload = {
            "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
            "contentType": "application/json",
            "accept": "application/json",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": enhanced_prompt
                            }
                        ]
                    }
                ]
            }
        }

        body_bytes = json.dumps(payload['body']).encode('utf-8')
        
        response = client.invoke_model(
            body=body_bytes,
            contentType=payload['contentType'],
            accept=payload['accept'],
            modelId=payload['modelId'],
            guardrailIdentifier=guardrail_id,
            guardrailVersion="DRAFT"
        )

        response_body = json.loads(response['body'].read().decode('utf-8'))
        return json.dumps(response_body['content'][0]['text'], indent=2)
    except Exception as e:
        logger.error(f"Error invoking model with guardrail: {e}")
        return str(e)

def main():
    st.title("AnyCorp Financials - Assistant")
    
    # Initialize clients
    bedrock_client = initialize_bedrock()
    kb_client = initialize_knowledge_base()
    guardrail_id = "hye7bokv9fbw"
    kb_id = "YCNSJ5C3NZ"  # Your knowledge base ID
    
    if not guardrail_id:
        st.error("Guardrail ID not found. Please run create_guardrail.py first.")
        return

    # Create a dictionary mapping names to user IDs
    user_mapping = {
        "John Smith": "jsmith",
        "Jane Doe": "jdoe"
    }

    # Create the select box with names as options but return user IDs as values
    selected_name = st.selectbox(
        "Select User:",
        options=list(user_mapping.keys()),
        format_func=lambda x: x  # This shows the name
    )

    # Get the selected user ID
    selected_user = user_mapping[selected_name]

    # User input
    user_input = st.text_area("Enter your question:", height=100)
    
    if st.button("Submit"):
        if user_input:
            # Retrieve context from knowledge base
            kb_results = query_knowledge_base(kb_client, kb_id, selected_user, user_input)
            
            col1, col2 = st.columns(2)
            
            # Create ThreadPoolExecutor to run functions in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit both function calls to run in parallel
                future_without_guardrail = executor.submit(
                    invoke_model_without_guardrail,
                    bedrock_client,
                    user_input,
                    kb_results
                )
                
                future_with_guardrail = executor.submit(
                    invoke_model_with_guardrail,
                    bedrock_client,
                    user_input,
                    kb_results,
                    guardrail_id
                )
                
                # Get results from both futures
                response_without = future_without_guardrail.result()
                response_with = future_with_guardrail.result()
            
            # Display results in columns
            with col1:
                st.subheader("Without Guardrail")
                st.write(response_without)
                
            with col2:
                st.subheader("With Guardrail")
                st.write(response_with)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
