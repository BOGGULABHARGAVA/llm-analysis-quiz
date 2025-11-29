"""
Utility functions for the LLM Analysis Quiz application
"""
import base64
import io
import json
import logging
import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def is_valid_url(url: str) -> bool:
    """Validate if a string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_email(email: str) -> bool:
    """Validate if a string is a valid email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def extract_base64_from_html(html: str) -> Optional[str]:
    """Extract base64 content from HTML atob() calls"""
    try:
        # Look for atob(`...`) pattern
        pattern = r'atob\([`\'"]([A-Za-z0-9+/=\s]+)[`\'"]\)'
        matches = re.findall(pattern, html)
        
        if matches:
            # Return the first match, cleaned
            return matches[0].replace('\n', '').replace(' ', '')
        
        # Also check for direct base64 strings
        pattern2 = r'data:([^;]+);base64,([A-Za-z0-9+/=]+)'
        matches2 = re.findall(pattern2, html)
        
        if matches2:
            return matches2[0][1]
            
        return None
    except Exception as e:
        logger.error(f"Error extracting base64: {e}")
        return None


def decode_base64(encoded: str) -> Optional[str]:
    """Decode base64 string to text"""
    try:
        # Clean the string
        encoded = encoded.strip().replace('\n', '').replace(' ', '')
        
        # Decode
        decoded_bytes = base64.b64decode(encoded)
        decoded_str = decoded_bytes.decode('utf-8')
        
        return decoded_str
    except Exception as e:
        logger.error(f"Error decoding base64: {e}")
        return None


def encode_base64(data: bytes) -> str:
    """Encode bytes to base64 string"""
    try:
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding base64: {e}")
        return ""


def create_data_uri(data: bytes, mime_type: str) -> str:
    """Create a data URI from bytes"""
    try:
        b64 = encode_base64(data)
        return f"data:{mime_type};base64,{b64}"
    except Exception as e:
        logger.error(f"Error creating data URI: {e}")
        return ""


def safe_json_loads(text: str) -> Optional[Dict]:
    """Safely parse JSON string"""
    try:
        return json.loads(text)
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return None


def safe_json_dumps(data: Any, indent: int = 2) -> str:
    """Safely convert to JSON string"""
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error converting to JSON: {e}")
        return "{}"


def extract_number(text: str) -> Optional[float]:
    """Extract first number from text"""
    try:
        # Remove commas and extract number
        text = text.replace(',', '')
        matches = re.findall(r'-?\d+\.?\d*', text)
        
        if matches:
            return float(matches[0])
        
        return None
    except Exception as e:
        logger.error(f"Error extracting number: {e}")
        return None


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "... (truncated)"


def clean_html(html: str) -> str:
    """Remove script tags and clean HTML"""
    try:
        # Remove script tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove style tags
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        return html.strip()
    except Exception as e:
        logger.error(f"Error cleaning HTML: {e}")
        return html


def format_error_response(message: str, status_code: int = 400) -> tuple:
    """Format error response for Flask"""
    return {
        "error": message,
        "status": "error"
    }, status_code


def format_success_response(data: Dict, status_code: int = 200) -> tuple:
    """Format success response for Flask"""
    response = {
        "status": "success",
        **data
    }
    return response, status_code


def log_request(email: str, url: str, action: str = "received"):
    """Log incoming request"""
    logger.info(f"Request {action} - Email: {email}, URL: {url}")


def log_response(email: str, url: str, success: bool, message: str = ""):
    """Log response"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Response {status} - Email: {email}, URL: {url}, Message: {message}")
