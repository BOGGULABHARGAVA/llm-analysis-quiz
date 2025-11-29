"""
Local testing script for LLM Analysis Quiz
"""
import asyncio
import sys
from browser_handler import render_quiz_page, get_browser_handler
from config import Config

async def test_browser():
    """Test browser initialization and page rendering"""
    print("Testing browser initialization...")
    
    try:
        # Test browser handler
        handler = await get_browser_handler()
        print(f"✓ Browser handler initialized: {handler}")
        
        # Test rendering a simple page
        test_url = "https://example.com"
        print(f"\nTesting page rendering: {test_url}")
        html, text = await render_quiz_page(test_url)
        
        print(f"✓ Page rendered successfully")
        print(f"  HTML length: {len(html)} chars")
        print(f"  Text length: {len(text)} chars")
        print(f"  Text preview: {text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_health_check():
    """Test health check endpoint"""
    import aiohttp
    
    print("\n\nTesting health endpoint...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/health') as resp:
                print(f"✓ Status: {resp.status}")
                data = await resp.json()
                print(f"✓ Response: {data}")
                return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("LOCAL TESTING - LLM Analysis Quiz")
    print("=" * 60)
    
    # Test 1: Browser functionality
    browser_ok = await test_browser()
    
    # Test 2: Health endpoint (server must be running)
    health_ok = await test_health_check()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Browser test: {'✓ PASS' if browser_ok else '✗ FAIL'}")
    print(f"Health test: {'✓ PASS' if health_ok else '✗ FAIL (ensure server is running)'}")
    print("=" * 60)
    
    return browser_ok

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
