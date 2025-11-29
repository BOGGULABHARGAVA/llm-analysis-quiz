"""
Quiz solver with LLM integration for intelligent problem-solving
"""
import asyncio
import logging
import re
import time
from typing import Any, Dict, Optional
import requests
from openai import OpenAI
from config import Config
from browser_handler import render_quiz_page
from data_processor import DataProcessor
from utils import (
    decode_base64, 
    extract_base64_from_html, 
    is_valid_url,
    safe_json_loads,
    log_request,
    log_response
)

logger = logging.getLogger(__name__)


class QuizSolver:
    """Solves quiz tasks using LLM and data processing"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.data_processor = DataProcessor()
        self.quiz_history = []
        
    def create_analysis_prompt(self, quiz_content: str, context: Dict = None) -> str:
        """
        Create a detailed prompt for the LLM to analyze the quiz
        
        Args:
            quiz_content: The rendered quiz page content
            context: Additional context (downloaded files, previous attempts, etc.)
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert data analyst solving a quiz task. Analyze the following quiz content and provide a solution.

QUIZ CONTENT:
{quiz_content}

"""
        
        if context:
            if 'file_data' in context:
                prompt += f"\nFILE DATA:\n{context['file_data']}\n"
            
            if 'previous_attempts' in context:
                prompt += f"\nPREVIOUS ATTEMPTS (FAILED):\n{context['previous_attempts']}\n"
        
        prompt += """
INSTRUCTIONS:
1. Read the quiz question carefully
2. Identify what needs to be done (download file, analyze data, create visualization, etc.)
3. Identify the submit URL and required payload format
4. Provide the exact answer in the required format
5. Be precise with numbers, strings, and data types

Your response must be a JSON object with this structure:
{
    "task_type": "description of the task (e.g., 'sum column in PDF table')",
    "file_url": "URL of file to download (if any)" or null,
    "submit_url": "URL where answer should be submitted",
    "answer": <the actual answer - can be number, string, boolean, or object>,
    "reasoning": "brief explanation of your solution"
}

CRITICAL: Ensure the answer is in the exact format requested (number, string, boolean, base64 URI, etc.)
"""
        
        return prompt
    
    async def analyze_quiz(self, quiz_url: str) -> Dict[str, Any]:
        """
        Analyze a quiz page and extract task details
        
        Args:
            quiz_url: URL of the quiz page
            
        Returns:
            Dictionary with task analysis
        """
        try:
            # Render the page with JavaScript execution
            html_content, text_content = await render_quiz_page(quiz_url)
            
            # Try to extract base64 encoded content
            base64_content = extract_base64_from_html(html_content)
            if base64_content:
                decoded_content = decode_base64(base64_content)
                if decoded_content:
                    text_content = decoded_content
                    logger.info("Successfully decoded base64 content from page")
            
            logger.info(f"Quiz content length: {len(text_content)} chars")
            
            # Use LLM to analyze the quiz
            prompt = self.create_analysis_prompt(text_content)
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful data analysis assistant that provides structured JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content
            logger.info(f"LLM Response: {llm_response[:500]}...")
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                analysis = safe_json_loads(json_match.group())
                if analysis:
                    return analysis
            
            # If JSON parsing failed, try to extract manually
            logger.warning("Failed to parse JSON, attempting manual extraction")
            return self._manual_extract(text_content)
            
        except Exception as e:
            logger.error(f"Error analyzing quiz: {e}")
            raise
    
    def _manual_extract(self, content: str) -> Dict[str, Any]:
        """Manually extract quiz information if LLM fails"""
        result = {
            "task_type": "unknown",
            "file_url": None,
            "submit_url": None,
            "answer": None,
            "reasoning": "Manual extraction fallback"
        }
        
        # Extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            if 'submit' in url.lower():
                result['submit_url'] = url
            elif any(ext in url.lower() for ext in ['.pdf', '.csv', '.xlsx', '.json', '.png', '.jpg']):
                result['file_url'] = url
        
        return result
    
    async def process_file(self, file_url: str) -> Dict[str, Any]:
        """
        Download and process a file from URL
        
        Args:
            file_url: URL of the file to download
            
        Returns:
            Dictionary with processed file data
        """
        try:
            logger.info(f"Processing file: {file_url}")
            
            # Download file
            content = self.data_processor.download_file(file_url)
            if not content:
                return {"error": "Failed to download file"}
            
            # Determine file type and process accordingly
            file_type = self._detect_file_type(file_url, content)
            logger.info(f"Detected file type: {file_type}")
            
            result = {"file_type": file_type, "file_url": file_url}
            
            if file_type == 'pdf':
                text = self.data_processor.read_pdf(content)
                result['text'] = text
                result['summary'] = text[:5000] if text else None
                
            elif file_type == 'csv':
                df = self.data_processor.read_csv(content)
                if df is not None:
                    result['data'] = self.data_processor.dataframe_to_dict(df)
                    result['analysis'] = self.data_processor.analyze_dataframe(df)
                    result['dataframe'] = df  # Keep for further processing
                    
            elif file_type == 'excel':
                df = self.data_processor.read_excel(content)
                if df is not None:
                    result['data'] = self.data_processor.dataframe_to_dict(df)
                    result['analysis'] = self.data_processor.analyze_dataframe(df)
                    result['dataframe'] = df
                    
            elif file_type == 'json':
                data = self.data_processor.read_json(content)
                result['data'] = data
                
            elif file_type == 'image':
                image = self.data_processor.read_image(content)
                if image:
                    result['image_size'] = image.size
                    result['image_mode'] = image.mode
                    result['image'] = image
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return {"error": str(e)}
    
    def _detect_file_type(self, url: str, content: bytes) -> str:
        """Detect file type from URL or content"""
        url_lower = url.lower()
        
        if url_lower.endswith('.pdf'):
            return 'pdf'
        elif url_lower.endswith('.csv'):
            return 'csv'
        elif url_lower.endswith(('.xlsx', '.xls')):
            return 'excel'
        elif url_lower.endswith('.json'):
            return 'json'
        elif url_lower.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return 'image'
        
        # Try to detect from content
        if content[:4] == b'%PDF':
            return 'pdf'
        elif content[:2] == b'PK':  # ZIP format (Excel)
            return 'excel'
        
        return 'unknown'
    
    async def solve_quiz(self, email: str, secret: str, quiz_url: str) -> Dict[str, Any]:
        """
        Main method to solve a complete quiz chain
        
        Args:
            email: User email
            secret: User secret key
            quiz_url: Starting quiz URL
            
        Returns:
            Dictionary with results
        """
        start_time = time.time()
        current_url = quiz_url
        attempts = 0
        max_attempts = 5
        
        log_request(email, quiz_url, "started")
        
        try:
            while current_url and (time.time() - start_time) < Config.QUIZ_TIMEOUT:
                attempts += 1
                
                if attempts > max_attempts:
                    logger.warning(f"Max attempts ({max_attempts}) reached")
                    break
                
                logger.info(f"Attempt {attempts}: Solving {current_url}")
                
                # Analyze the quiz
                analysis = await self.analyze_quiz(current_url)
                logger.info(f"Analysis: {analysis}")
                
                # Process file if needed
                file_data = None
                if analysis.get('file_url'):
                    file_data = await self.process_file(analysis['file_url'])
                    
                    # If we have structured data, ask LLM to compute the answer
                    if 'analysis' in file_data or 'data' in file_data:
                        analysis = await self._compute_answer_with_llm(analysis, file_data)
                
                # Submit the answer
                submit_url = analysis.get('submit_url')
                answer = analysis.get('answer')
                
                if not submit_url or answer is None:
                    logger.error("Missing submit URL or answer")
                    break
                
                response = self._submit_answer(email, secret, current_url, answer, submit_url)
                logger.info(f"Submit response: {response}")
                
                # Check if correct and get next URL
                if response.get('correct'):
                    logger.info("Answer correct!")
                    next_url = response.get('url')
                    
                    if next_url and is_valid_url(next_url):
                        current_url = next_url
                        logger.info(f"Moving to next quiz: {next_url}")
                    else:
                        logger.info("Quiz chain complete!")
                        log_response(email, quiz_url, True, "All quizzes solved")
                        return {
                            "status": "completed",
                            "attempts": attempts,
                            "time_taken": time.time() - start_time
                        }
                else:
                    reason = response.get('reason', 'Unknown error')
                    logger.warning(f"Answer incorrect: {reason}")
                    
                    # Check if we should retry or move on
                    next_url = response.get('url')
                    if next_url and is_valid_url(next_url) and next_url != current_url:
                        logger.info(f"Moving to next quiz despite error: {next_url}")
                        current_url = next_url
                    else:
                        # Retry with additional context
                        logger.info("Retrying with error context...")
                        # Could add retry logic here with error context
                
                # Small delay between attempts
                await asyncio.sleep(1)
            
            elapsed = time.time() - start_time
            log_response(email, quiz_url, False, f"Completed {attempts} attempts in {elapsed:.2f}s")
            
            return {
                "status": "partial" if attempts > 0 else "failed",
                "attempts": attempts,
                "time_taken": elapsed
            }
            
        except Exception as e:
            logger.error(f"Error in solve_quiz: {e}")
            log_response(email, quiz_url, False, str(e))
            raise
    
    async def _compute_answer_with_llm(self, analysis: Dict, file_data: Dict) -> Dict:
        """Use LLM to compute answer based on file data"""
        try:
            prompt = f"""Based on the quiz task and file data below, compute the exact answer.

TASK: {analysis.get('task_type', 'unknown')}

FILE DATA:
{file_data.get('analysis', file_data.get('data', 'No data'))}

QUESTION CONTEXT:
{analysis.get('reasoning', 'No context')}

Provide the exact answer as a JSON object:
{{
    "answer": <the computed answer>,
    "explanation": "brief explanation"
}}
"""
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a precise data analyst. Provide exact numerical answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            
            if json_match:
                result = safe_json_loads(json_match.group())
                if result and 'answer' in result:
                    analysis['answer'] = result['answer']
                    logger.info(f"LLM computed answer: {result['answer']}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error computing answer with LLM: {e}")
            return analysis
    
    def _submit_answer(self, email: str, secret: str, quiz_url: str, 
                      answer: Any, submit_url: str) -> Dict:
        """Submit answer to the quiz endpoint"""
        try:
            payload = {
                "email": email,
                "secret": secret,
                "url": quiz_url,
                "answer": answer
            }
            
            logger.info(f"Submitting to {submit_url}: {payload}")
            
            response = requests.post(
                submit_url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting answer: {e}")
            return {"correct": False, "reason": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error submitting answer: {e}")
            return {"correct": False, "reason": str(e)}
