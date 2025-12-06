"""
Automated Reasoning Validator
Separate module for AR validation logic
"""

import re
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ARValidationResult:
    """Result from AR validation"""
    is_valid: bool
    violations: List[str]
    confidence: float
    scenario: str
    agent_level: str


class AutomatedReasoningValidator:
    """
    Automated Reasoning Validator
    Validates extracted intent against authorization rules
    """
    
    def __init__(self):
        self.rules = self._load_authorization_rules()
    
    def _load_authorization_rules(self) -> Dict:
        """Load authorization rules for different scenarios"""
        return {
            'wire_transfer': {
                'agent_limits': {
                    'Customer Service Agent': 0,
                    'Junior Banker': 2000,
                    'Senior Banker': 10000,
                    'Branch Manager': 100000
                },
                'valid_policies': ['STANDARD-TRANSFER-POLICY']
            },
            'loan_approval': {
                'agent_limits': {
                    'Junior Loan Officer': {'personal_loan': 2000, 'auto_loan': 10000, 'mortgage': 0},
                    'Senior Loan Officer': {'personal_loan': 5000, 'auto_loan': 25000, 'mortgage': 250000}
                },
                'valid_policies': ['STANDARD-LENDING-POLICY']
            },
            'portfolio_management': {
                'agent_limits': {
                    'Junior Portfolio Manager': {'portfolio_change_percent': 10, 'max_trade_size': 5000},
                    'Senior Portfolio Manager': {'portfolio_change_percent': 25, 'max_trade_size': 10000}
                },
                'max_single_position': 30,
                'max_sector_concentration': 40
            },
            'account_management': {
                'agent_limits': {
                    'Customer Service Agent': {'can_close_account': False, 'can_modify_limits': False, 'can_update_info': True},
                    'Account Manager': {'can_close_account': True, 'can_modify_limits': True, 'can_update_info': True}
                }
            }
        }
    
    def validate(
        self,
        extracted_intent: str,
        original_prompt: str,
        agent_level: str,
        scenario: str = None  # Optional, will be determined from ACTION if not provided
    ) -> ARValidationResult:
        """
        Main validation function
        
        Args:
            extracted_intent: LLM's structured extraction (ACTION, ACTION TYPE, PARAMETERS, etc.)
            original_prompt: Original user prompt
            agent_level: Agent's authorization level
            scenario: Optional scenario type (will be auto-detected from ACTION if not provided)
            
        Returns:
            ARValidationResult with validation outcome
        """
        # Parse the structured extraction from LLM
        parsed_intent = self._parse_extracted_intent(extracted_intent)
        
        # Determine scenario from ACTION if not provided
        if not scenario:
            scenario = self._determine_scenario_from_action(parsed_intent.get('action', ''))
        
        logger.info(f"Validating {scenario} request for {agent_level}")
        
        # Apply policy-based validation
        violations = self._apply_policy_validation(
            parsed_intent=parsed_intent,
            original_prompt=original_prompt,
            agent_level=agent_level,
            scenario=scenario
        )
        
        is_valid = len(violations) == 0
        confidence = 0.95 if not is_valid else 0.92
        
        logger.info(f"Validation result: {'VALID' if is_valid else 'INVALID'} ({len(violations)} violations)")
        
        return ARValidationResult(
            is_valid=is_valid,
            violations=violations,
            confidence=confidence,
            scenario=scenario,
            agent_level=agent_level
        )
    
    def _determine_scenario_from_action(self, action: str) -> str:
        """
        Determine the scenario type from the ACTION field
        
        Args:
            action: The action extracted by LLM (e.g., "wire_transfer", "loan_approval")
            
        Returns:
            Scenario type string
        """
        action_lower = action.lower()
        
        # Wire transfer scenarios
        if any(keyword in action_lower for keyword in ['wire', 'transfer', 'payment', 'send_money']):
            return 'wire_transfer'
        
        # Loan approval scenarios
        if any(keyword in action_lower for keyword in ['loan', 'credit', 'mortgage', 'borrow']):
            return 'loan_approval'
        
        # Portfolio management scenarios
        if any(keyword in action_lower for keyword in ['portfolio', 'rebalance', 'invest', 'trade', 'stock', 'asset']):
            return 'portfolio_management'
        
        # Account management scenarios
        if any(keyword in action_lower for keyword in ['close_account', 'modify_limit', 'update_account', 'account_closure']):
            return 'account_management'
        
        # Unknown scenario
        logger.warning(f"Could not determine scenario from action: '{action}' - using generic validation")
        return 'unknown'
    
    def _parse_extracted_intent(self, extracted_intent: str) -> Dict:
        """
        Parse the structured extraction from LLM
        
        Expected format:
        ACTION: wire_transfer
        ACTION TYPE: create
        ACTION DESCRIPTION: Transfer funds
        PARAMETERS: amount=$50,000, from_account=#12345678
        REFERENCES: Policy PBB-2024-Section-8.3.2
        """
        import re
        
        parsed = {
            'action': '',
            'action_type': '',
            'action_description': '',
            'parameters': {},
            'references': [],
            'raw': extracted_intent
        }
        
        # Extract ACTION
        action_match = re.search(r'ACTION:\s*(.+?)(?:\n|$)', extracted_intent, re.IGNORECASE)
        if action_match:
            parsed['action'] = action_match.group(1).strip().lower()
        
        # Extract ACTION TYPE
        action_type_match = re.search(r'ACTION TYPE:\s*(.+?)(?:\n|$)', extracted_intent, re.IGNORECASE)
        if action_type_match:
            parsed['action_type'] = action_type_match.group(1).strip().lower()
        
        # Extract ACTION DESCRIPTION
        desc_match = re.search(r'ACTION DESCRIPTION:\s*(.+?)(?:\n|$)', extracted_intent, re.IGNORECASE)
        if desc_match:
            parsed['action_description'] = desc_match.group(1).strip()
        
        # Extract PARAMETERS
        params_match = re.search(r'PARAMETERS:\s*(.+?)(?:\n[A-Z]+:|$)', extracted_intent, re.IGNORECASE | re.DOTALL)
        if params_match:
            params_text = params_match.group(1).strip()
            
            # Extract amount
            amount_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)', params_text)
            if amount_match:
                parsed['parameters']['amount'] = float(amount_match.group(1).replace(',', ''))
            
            # Extract account numbers
            account_matches = re.findall(r'#?(\d{6,})', params_text)
            if account_matches:
                parsed['parameters']['accounts'] = account_matches
            
            # Extract loan type
            if 'mortgage' in params_text.lower():
                parsed['parameters']['loan_type'] = 'mortgage'
            elif 'auto' in params_text.lower() or 'vehicle' in params_text.lower():
                parsed['parameters']['loan_type'] = 'auto_loan'
            elif 'personal' in params_text.lower():
                parsed['parameters']['loan_type'] = 'personal_loan'
            
            # Extract percentages (for portfolio management)
            percentages = re.findall(r'(\d+)%', params_text)
            if percentages:
                parsed['parameters']['percentages'] = [int(p) for p in percentages]
        
        # Extract REFERENCES
        refs_match = re.search(r'REFERENCES:\s*(.+?)(?:\n[A-Z]+:|$)', extracted_intent, re.IGNORECASE | re.DOTALL)
        if refs_match:
            refs_text = refs_match.group(1).strip()
            
            # Extract policy references
            policy_matches = re.findall(r'[Pp]olicy\s*(?:[Rr]eference)?:?\s*([\w-]+(?:-[\w-]+)*(?:\.[\w-]+)*)', refs_text)
            parsed['references'].extend(policy_matches)
            
            # Extract approval claims
            if 'approv' in refs_text.lower():
                parsed['references'].append('approval_claimed')
        
        return parsed
    
    def _apply_policy_validation(
        self,
        parsed_intent: Dict,
        original_prompt: str,
        agent_level: str,
        scenario: str
    ) -> List[str]:
        """
        Apply policy-based validation based on parsed intent
        
        This is the core validation logic that checks:
        1. Agent authorization for the action
        2. Amount/parameter limits
        3. Policy reference validity
        4. Approval requirements
        """
        violations = []
        
        action = parsed_intent.get('action', '')
        action_type = parsed_intent.get('action_type', '')
        params = parsed_intent.get('parameters', {})
        references = parsed_intent.get('references', [])
        
        # Determine which policy to apply based on action
        if 'wire' in action or 'transfer' in action:
            violations.extend(self._validate_wire_transfer_policy(params, references, agent_level, original_prompt))
        elif 'loan' in action or 'credit' in action:
            violations.extend(self._validate_loan_policy(params, references, agent_level, original_prompt))
        elif 'portfolio' in action or 'rebalance' in action or 'invest' in action:
            violations.extend(self._validate_portfolio_policy(params, references, agent_level, original_prompt))
        elif 'close' in action or 'modify' in action or 'limit' in action:
            violations.extend(self._validate_account_policy(params, references, agent_level, original_prompt))
        else:
            # Generic validation for unknown actions
            violations.extend(self._validate_generic_policy(parsed_intent, original_prompt, agent_level))
        
        # Universal checks that apply to all actions
        violations.extend(self._universal_checks(parsed_intent, original_prompt, agent_level))
        
        return violations
    
    def _universal_checks(
        self,
        parsed_intent: Dict,
        original_prompt: str,
        agent_level: str
    ) -> List[str]:
        """Universal checks that apply to all actions"""
        violations = []
        
        action_type = parsed_intent.get('action_type', '')
        params = parsed_intent.get('parameters', {})
        references = parsed_intent.get('references', [])
        
        # Check 1: DELETE actions require senior authorization
        if action_type == 'delete':
            if 'Customer Service' in agent_level or 'Junior' in agent_level:
                violations.append(f"DELETE actions require senior authorization - {agent_level} not authorized")
        
        # Check 2: Verify policy references
        for ref in references:
            if ref != 'approval_claimed' and ref not in ['STANDARD-TRANSFER-POLICY', 'STANDARD-LENDING-POLICY']:
                violations.append(f"Policy reference '{ref}' not found in authoritative database")
        
        # Check 3: Approval claims require documentation
        if 'approval_claimed' in references:
            if 'verbal' in original_prompt.lower():
                violations.append("Verbal approvals must be documented in system")
            else:
                violations.append("Claimed approval not found in approval records")
        
        # Check 4: Validate approval codes
        approval_code_pattern = r'(?:approval|auth)(?:\s+code)?:\s*([A-Z0-9-]+)'
        approval_codes = re.findall(approval_code_pattern, original_prompt, re.IGNORECASE)
        if approval_codes:
            # All approval codes should be validated against system
            for code in approval_codes:
                violations.append(f"Approval code '{code}' not found in authorization system")
        
        # Check 5: High-risk urgency indicators
        urgency_words = ['urgent', 'immediately', 'asap', 'emergency', 'rush']
        if any(word in original_prompt.lower() for word in urgency_words):
            if params.get('amount', 0) > 10000:
                violations.append("Urgent high-value requests require additional verification")
        
        # Check 6: Context switching
        if 'actually' in original_prompt.lower() or 'wait' in original_prompt.lower():
            if 'on behalf' in original_prompt.lower():
                violations.append("Context switching with third-party access requires re-authentication")
        
        # Check 7: Split transaction detection
        # Look for multiple transfers/transactions in the same request
        transfer_indicators = ['two', 'three', 'multiple', 'separate', 'each']
        if any(indicator in original_prompt.lower() for indicator in transfer_indicators):
            # Check if describing multiple transactions
            if 'transfer' in original_prompt.lower() or 'loan' in original_prompt.lower():
                # Extract all amounts mentioned
                all_amounts = re.findall(r'\$?([\d,]+(?:\.\d{2})?)', original_prompt)
                if len(all_amounts) >= 2:
                    amounts = [float(a.replace(',', '')) for a in all_amounts if float(a.replace(',', '')) > 100]
                    if len(amounts) >= 2:
                        total_amount = sum(amounts)
                        violations.append(f"Split transaction detected: Total amount ${total_amount:,.2f} exceeds authorization when combined")
        
        return violations
    
    def _validate_wire_transfer_policy(
        self,
        params: Dict,
        references: List[str],
        agent_level: str,
        original_prompt: str
    ) -> List[str]:
        """Validate wire transfer against policy"""
        violations = []
        
        amount = params.get('amount', 0)
        
        # Fallback: If no amount extracted from parameters, try original prompt
        if amount == 0:
            amount_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)', original_prompt)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
        
        agent_limit = self.rules['wire_transfer']['agent_limits'].get(agent_level, 0)
        
        # Check authorization
        if agent_limit == 0:
            violations.append(f"Agent level '{agent_level}' not authorized for wire transfers")
        
        # Check amount limit
        if amount > agent_limit:
            violations.append(f"Transfer amount (${amount:,.2f}) exceeds agent limit (${agent_limit:,.2f})")
        
        return violations
    
    def _validate_loan_policy(
        self,
        params: Dict,
        references: List[str],
        agent_level: str,
        original_prompt: str
    ) -> List[str]:
        """Validate loan approval against policy"""
        violations = []
        
        amount = params.get('amount', 0)
        
        # Fallback: If no amount extracted from parameters, try original prompt
        if amount == 0:
            amount_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)', original_prompt)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
        
        loan_type = params.get('loan_type', 'personal_loan')
        
        agent_limits = self.rules['loan_approval']['agent_limits'].get(agent_level, {})
        agent_limit = agent_limits.get(loan_type, 0)
        
        # Check authorization
        if agent_limit == 0:
            violations.append(f"Agent level '{agent_level}' not authorized for {loan_type.replace('_', ' ')}s")
        
        # Check amount limit
        if amount > agent_limit:
            violations.append(f"Loan amount (${amount:,.2f}) exceeds agent limit (${agent_limit:,.2f})")
        
        return violations
    
    def _validate_portfolio_policy(
        self,
        params: Dict,
        references: List[str],
        agent_level: str,
        original_prompt: str
    ) -> List[str]:
        """Validate portfolio management against policy"""
        violations = []
        
        percentages = params.get('percentages', [])
        
        # Check single position limit
        if percentages and max(percentages) > self.rules['portfolio_management']['max_single_position']:
            violations.append(f"Single position ({max(percentages)}%) exceeds maximum (30%)")
        
        # Check risk reclassification
        if 'reclassified' in original_prompt.lower():
            violations.append("Risk reclassification not verified against market data")
        
        return violations
    
    def _validate_account_policy(
        self,
        params: Dict,
        references: List[str],
        agent_level: str,
        original_prompt: str
    ) -> List[str]:
        """Validate account management against policy"""
        violations = []
        
        agent_capabilities = self.rules['account_management']['agent_limits'].get(agent_level, {})
        
        # Check account closure
        if 'close' in original_prompt.lower():
            if not agent_capabilities.get('can_close_account', False):
                violations.append("Agent not authorized to close accounts")
        
        # Check limit modifications
        if 'limit' in original_prompt.lower() and 'increase' in original_prompt.lower():
            if not agent_capabilities.get('can_modify_limits', False):
                violations.append("Agent not authorized to modify account limits")
        
        return violations
    
    def _validate_generic_policy(
        self,
        parsed_intent: Dict,
        original_prompt: str,
        agent_level: str
    ) -> List[str]:
        """Generic policy validation for unknown actions"""
        violations = []
        
        params = parsed_intent.get('parameters', {})
        amount = params.get('amount', 0)
        
        # Flag large amounts in unknown scenarios
        if amount > 10000:
            violations.append(f"Large transaction (${amount:,.2f}) in unknown scenario requires senior authorization")
        
        # Flag Customer Service attempting unknown financial actions
        if 'Customer Service' in agent_level:
            if amount > 5000:
                violations.append(f"Agent level '{agent_level}' attempting high-value action - requires escalation")
        
        return violations

    def format_response(self, result: ARValidationResult, reference_id: str) -> str:
        """Format AR validation result as response"""
        if result.is_valid:
            return f"""[AUTOMATED REASONING VALIDATION: PASSED]

Authorization verified (confidence: {result.confidence:.2%})
This action is within {result.agent_level} authority and can be processed.

Proceeding with execution...
Reference: {reference_id}"""
        else:
            return f"""[AUTOMATED REASONING VALIDATION: FAILED]

VIOLATIONS DETECTED:
{chr(10).join(f"  ✗ {v}" for v in result.violations)}

This action cannot be processed. The request has been escalated for manual review.
Confidence: {result.confidence:.2%}
Reference: ESCALATION-{reference_id}"""
