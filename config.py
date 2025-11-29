import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 8000))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Authentication
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    EMAIL = os.getenv('EMAIL', '')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    
    # Quiz Configuration
    QUIZ_TIMEOUT = int(os.getenv('QUIZ_TIMEOUT', 170))  # 170 seconds (under 3 min)
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 2))
    
    # Browser Configuration
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'
    BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', 30000))  # 30 seconds
    
    # File Processing
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        if not cls.SECRET_KEY:
            errors.append("SECRET_KEY is required")
        if not cls.EMAIL:
            errors.append("EMAIL is required")
            
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
