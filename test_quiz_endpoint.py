"""
Test quiz endpoint locally
"""
import asyncio
import json
from quiz_solver import QuizSolver

async def test_quiz_solving():
    """Test the full quiz solving flow"""
    print("=" * 60)
    print("TESTING QUIZ SOLVER")
    print("=" * 60)
    
    # Test configuration
    email = "23f2003741@ds.study.iitm.ac.in"
    secret = "Bhargava123"
    quiz_url = "https://tds-llm-analysis.s-anand.net/demo"
    
    print(f"\nTest parameters:")
    print(f"  Email: {email}")
    print(f"  Secret: {secret}")
    print(f"  Quiz URL: {quiz_url}")
    
    try:
        solver = QuizSolver()
        print(f"\n✓ QuizSolver initialized")
        
        print(f"\nSolving quiz... (this may take 1-2 minutes)")
        result = await solver.solve_quiz(email, secret, quiz_url)
        
        print(f"\n{'=' * 60}")
        print("RESULT:")
        print(f"{'=' * 60}")
        print(json.dumps(result, indent=2))
        
        if result.get("status") == "success":
            print(f"\n✓ Quiz solved successfully!")
            return True
        else:
            print(f"\n✗ Quiz solving failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_quiz_solving())
    exit(0 if result else 1)
