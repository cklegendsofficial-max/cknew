#!/usr/bin/env python3
"""
Self Improver Module
Improves code logic without modifying the environment
"""

import os
import ast
import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import sys

# Try to import javalang for Java code analysis
try:
    import javalang
    JAVALANG_AVAILABLE = True
except ImportError:
    print("Warning: javalang not available for Java code analysis")
    JAVALANG_AVAILABLE = False

# Try to import ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    print("Warning: ollama not available")
    OLLAMA_AVAILABLE = False

@dataclass
class CodeImprovement:
    """Data structure for code improvements"""
    file_path: str
    improvement_type: str
    description: str
    original_code: str
    improved_code: str
    confidence: float

class SelfImprover:
    """Self-improvement system that enhances code logic without environment changes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        self.improvement_history = self.load_improvement_history()
        
    def load_config(self) -> Dict:
        """Load configuration"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def load_improvement_history(self) -> Dict:
        """Load improvement history to prevent infinite loops"""
        history_path = os.path.join(os.path.dirname(__file__), 'improvement_history.json')
        try:
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading improvement history: {e}")
        return {}
    
    def save_improvement_history(self):
        """Save improvement history"""
        history_path = os.path.join(os.path.dirname(__file__), 'improvement_history.json')
        try:
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(self.improvement_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving improvement history: {e}")
    
    def analyze_code_quality(self, file_path: str) -> Dict:
        """Analyze code quality and identify improvement opportunities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            analysis = {
                'file_path': file_path,
                'issues': [],
                'suggestions': [],
                'complexity_score': 0
            }
            
            # Parse Python code
            try:
                tree = ast.parse(code)
                analysis.update(self._analyze_python_ast(tree))
            except SyntaxError as e:
                analysis['issues'].append(f"Syntax error: {e}")
            
            # Additional analysis
            analysis.update(self._analyze_code_patterns(code))
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing code: {e}")
            return {'file_path': file_path, 'issues': [f"Analysis error: {e}"]}
    
    def _analyze_python_ast(self, tree: ast.AST) -> Dict:
        """Analyze Python AST for code quality issues"""
        issues = []
        suggestions = []
        complexity_score = 0
        
        for node in ast.walk(tree):
            # Check for nested loops
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)) and child != node:
                        issues.append("Nested loops detected. Consider using list comprehensions or vectorized operations.")
                        complexity_score += 2
                        break
            
            # Check for long functions
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    issues.append("Long function detected. Consider breaking it into smaller functions.")
                    complexity_score += 1
            
            # Check for hardcoded strings
            if isinstance(node, ast.Str) and len(node.s) > 100:
                issues.append("Long hardcoded string detected. Consider moving to configuration file.")
                complexity_score += 1
            
            # Check for magic numbers
            if isinstance(node, ast.Num) and isinstance(node.n, (int, float)):
                if node.n > 1000 or (isinstance(node.n, float) and node.n < 0.1):
                    issues.append("Magic number detected. Consider using named constants.")
                    complexity_score += 1
        
        return {
            'issues': issues,
            'suggestions': suggestions,
            'complexity_score': complexity_score
        }
    
    def _analyze_code_patterns(self, code: str) -> Dict:
        """Analyze code patterns for improvement opportunities"""
        issues = []
        suggestions = []
        
        # Check for common anti-patterns
        patterns = [
            (r'import \*', "Wildcard imports detected. Import specific modules instead."),
            (r'except:', "Bare except clause detected. Specify exception types."),
            (r'print\s*\(', "Print statements detected. Consider using logging."),
            (r'global\s+\w+', "Global variables detected. Consider using function parameters or classes."),
            (r'def\s+\w+\s*\([^)]*\):\s*\n\s*pass', "Empty function detected. Add implementation or remove."),
        ]
        
        for pattern, message in patterns:
            if re.search(pattern, code):
                issues.append(message)
        
        # Check for performance issues
        if code.count('for') > code.count('list(') + code.count('map(') + code.count('filter('):
            suggestions.append("Consider using list comprehensions or functional programming for better performance.")
        
        return {
            'issues': issues,
            'suggestions': suggestions
        }
    
    def generate_improvements(self, analysis: Dict) -> List[CodeImprovement]:
        """Generate specific code improvements based on analysis"""
        improvements = []
        
        if not OLLAMA_AVAILABLE:
            self.logger.warning("Ollama not available, using rule-based improvements")
            return self._generate_rule_based_improvements(analysis)
        
        try:
            # Create prompt for Ollama
            prompt = f"""
            Analyze this Python code and suggest specific improvements:
            
            File: {analysis['file_path']}
            Issues found: {analysis['issues']}
            Suggestions: {analysis['suggestions']}
            Complexity score: {analysis['complexity_score']}
            
            Provide specific code improvements in JSON format:
            {{
                "improvements": [
                    {{
                        "type": "performance|readability|maintainability",
                        "description": "What to improve",
                        "original_code": "Code to replace",
                        "improved_code": "Improved code",
                        "confidence": 0.8
                    }}
                ]
            }}
            
            Focus on:
            1. Performance optimizations
            2. Code readability
            3. Maintainability
            4. Best practices
            5. Error handling
            """
            
            # Call Ollama
            response = ollama.chat(model='llama3', messages=[{
                'role': 'user',
                'content': prompt
            }])
            
            # Parse response
            try:
                improvements_data = json.loads(response['message']['content'])
                for imp in improvements_data.get('improvements', []):
                    improvement = CodeImprovement(
                        file_path=analysis['file_path'],
                        improvement_type=imp.get('type', 'general'),
                        description=imp.get('description', ''),
                        original_code=imp.get('original_code', ''),
                        improved_code=imp.get('improved_code', ''),
                        confidence=imp.get('confidence', 0.5)
                    )
                    improvements.append(improvement)
                    
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse Ollama response, using rule-based improvements")
                improvements = self._generate_rule_based_improvements(analysis)
                
        except Exception as e:
            self.logger.error(f"Error generating improvements: {e}")
            improvements = self._generate_rule_based_improvements(analysis)
        
        return improvements
    
    def _generate_rule_based_improvements(self, analysis: Dict) -> List[CodeImprovement]:
        """Generate improvements based on rules when Ollama is not available"""
        improvements = []
        
        for issue in analysis.get('issues', []):
            if "Nested loops" in issue:
                improvements.append(CodeImprovement(
                    file_path=analysis['file_path'],
                    improvement_type="performance",
                    description="Replace nested loops with list comprehension or vectorized operations",
                    original_code="# Nested loops example\nfor i in range(10):\n    for j in range(10):\n        result[i][j] = i + j",
                    improved_code="# Vectorized operation\nimport numpy as np\ni, j = np.meshgrid(range(10), range(10))\nresult = i + j",
                    confidence=0.8
                ))
            
            elif "Long hardcoded string" in issue:
                improvements.append(CodeImprovement(
                    file_path=analysis['file_path'],
                    improvement_type="maintainability",
                    description="Move long strings to configuration file",
                    original_code='long_string = "This is a very long hardcoded string..."',
                    improved_code='from config import LONG_STRING\nlong_string = LONG_STRING',
                    confidence=0.9
                ))
            
            elif "Magic number" in issue:
                improvements.append(CodeImprovement(
                    file_path=analysis['file_path'],
                    improvement_type="readability",
                    description="Replace magic numbers with named constants",
                    original_code="timeout = 30",
                    improved_code="TIMEOUT_SECONDS = 30\ntimeout = TIMEOUT_SECONDS",
                    confidence=0.9
                ))
        
        return improvements
    
    def apply_improvement(self, improvement: CodeImprovement) -> bool:
        """Apply a code improvement"""
        try:
            # Check if this improvement was already applied recently
            file_key = f"{improvement.file_path}_{improvement.description}"
            if file_key in self.improvement_history:
                last_applied = self.improvement_history[file_key]['timestamp']
                # Don't apply the same improvement within 24 hours
                if self._is_recent_timestamp(last_applied):
                    self.logger.info(f"Improvement already applied recently: {improvement.description}")
                    return False
            
            # Read the file
            with open(improvement.file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Apply the improvement (simple string replacement for now)
            if improvement.original_code in code:
                improved_code = code.replace(improvement.original_code, improvement.improved_code)
                
                # Write the improved code
                with open(improvement.file_path, 'w', encoding='utf-8') as f:
                    f.write(improved_code)
                
                # Record the improvement
                self.improvement_history[file_key] = {
                    'timestamp': self._get_current_timestamp(),
                    'improvement': improvement.description,
                    'confidence': improvement.confidence
                }
                self.save_improvement_history()
                
                self.logger.info(f"Applied improvement: {improvement.description}")
                return True
            else:
                self.logger.warning(f"Could not find original code to replace: {improvement.original_code[:50]}...")
                return False
                
        except Exception as e:
            self.logger.error(f"Error applying improvement: {e}")
            return False
    
    def improve_code(self, file_path: str) -> bool:
        """Main function to improve a code file"""
        try:
            self.logger.info(f"Improving code: {file_path}")
            
            # Analyze the code
            analysis = self.analyze_code_quality(file_path)
            
            if not analysis.get('issues') and not analysis.get('suggestions'):
                self.logger.info(f"No improvements needed for {file_path}")
                return True
            
            # Generate improvements
            improvements = self.generate_improvements(analysis)
            
            if not improvements:
                self.logger.info(f"No improvements generated for {file_path}")
                return True
            
            # Apply improvements
            applied_count = 0
            for improvement in improvements:
                if self.apply_improvement(improvement):
                    applied_count += 1
            
            self.logger.info(f"Applied {applied_count}/{len(improvements)} improvements to {file_path}")
            return applied_count > 0
            
        except Exception as e:
            self.logger.error(f"Error improving code {file_path}: {e}")
            return False
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _is_recent_timestamp(self, timestamp_str: str) -> bool:
        """Check if timestamp is recent (within 24 hours)"""
        from datetime import datetime, timedelta
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            return datetime.now() - timestamp < timedelta(hours=24)
        except:
            return False

if __name__ == "__main__":
    # Test the self-improver
    improver = SelfImprover()
    
    # Test with a sample file
    test_file = os.path.join(os.path.dirname(__file__), 'main.py')
    if os.path.exists(test_file):
        success = improver.improve_code(test_file)
        print(f"Improvement test: {'Success' if success else 'Failed'}")
    else:
        print("Test file not found")
