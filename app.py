"""
Flask API server for LLM Analysis Quiz
"""
import asyncio
import logging
from flask import Flask, request, jsonify
from config import Config
from quiz_solver import QuizSolver
from utils import (
    is_valid_url,
    is_valid_email,
    format_error_response,
    format_success_response,
    log_request
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Validate configuration on startup
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "LLM Analysis Quiz Solver",
        "version": "1.0.0",
        "endpoints": {
            "quiz": "/quiz (POST)",
            "health": "/ (GET)"
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "openai_configured": bool(Config.OPENAI_API_KEY),
        "secret_configured": bool(Config.SECRET_KEY)
    }), 200


@app.route('/quiz', methods=['POST'])
def handle_quiz():
    """
    Main endpoint for receiving quiz requests
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "secret": "user_secret",
        "url": "https://example.com/quiz-123"
    }
    """
    try:
        # Validate JSON payload
        if not request.is_json:
            logger.warning("Invalid request: not JSON")
            return format_error_response("Request must be JSON", 400)
        
        data = request.get_json()
        
        # Validate required fields
        email = data.get('email')
        secret = data.get('secret')
        quiz_url = data.get('url')
        
        if not all([email, secret, quiz_url]):
            logger.warning("Invalid request: missing required fields")
            return format_error_response(
                "Missing required fields: email, secret, url", 
                400
            )
        
        # Validate email format
        if not is_valid_email(email):
            logger.warning(f"Invalid email format: {email}")
            return format_error_response("Invalid email format", 400)
        
        # Validate URL format
        if not is_valid_url(quiz_url):
            logger.warning(f"Invalid URL format: {quiz_url}")
            return format_error_response("Invalid URL format", 400)
        
        # Validate secret
        if secret != Config.SECRET_KEY:
            logger.warning(f"Invalid secret for email: {email}")
            return format_error_response("Invalid secret", 403)
        
        # Log the request
        log_request(email, quiz_url, "received")
        
        # Process the quiz asynchronously
        logger.info(f"Starting quiz solver for {quiz_url}")
        
        # Run the async quiz solver
        result = asyncio.run(solve_quiz_async(email, secret, quiz_url))
        
        if result.get('status') in ['completed', 'partial']:
            return format_success_response({
                "message": "Quiz solving initiated",
                "url": quiz_url,
                "result": result
            })
        else:
            return format_error_response(
                f"Quiz solving failed: {result.get('error', 'Unknown error')}", 
                500
            )
        
    except Exception as e:
        logger.error(f"Error handling quiz request: {e}", exc_info=True)
        return format_error_response(f"Internal server error: {str(e)}", 500)


async def solve_quiz_async(email: str, secret: str, quiz_url: str):
    """Async wrapper for quiz solving"""
    try:
        solver = QuizSolver()
        result = await solver.solve_quiz(email, secret, quiz_url)
        return result
    except Exception as e:
        logger.error(f"Error in quiz solver: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "status": "error"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "status": "error"
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting Flask app on {Config.HOST}:{Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    
    # Run the Flask app
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
