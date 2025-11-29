"""
Quick check if Render deployment has the latest fixes
"""
import requests
import json
from datetime import datetime

RENDER_URL = "https://llm-analysis-quiz-z1m2.onrender.com"

def check_deployment():
    """Check if the latest deployment is live"""
    print("=" * 70)
    print("RENDER DEPLOYMENT STATUS CHECK")
    print("=" * 70)
    print(f"Time: {datetime.now()}")
    print(f"URL: {RENDER_URL}")
    print()
    
    # Test 1: Health endpoint
    print("1. Testing /health endpoint...")
    try:
        resp = requests.get(f"{RENDER_URL}/health", timeout=10)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   ✗ Error: {resp.text}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    print()
    
    # Test 2: Quick quiz test (will fail but shows if browser is available)
    print("2. Testing /quiz endpoint (quick browser check)...")
    try:
        payload = {
            "email": "23f2003741@ds.study.iitm.ac.in",
            "secret": "Bhargava123",
            "url": "https://tds-llm-analysis.s-anand.net/demo"
        }
        resp = requests.post(
            f"{RENDER_URL}/quiz",
            json=payload,
            timeout=180
        )
        print(f"   Status: {resp.status_code}")
        data = resp.json()
        
        if "browser" in str(data).lower() or "executable" in str(data).lower():
            print("   ✗ BROWSER ERROR STILL PRESENT!")
            print(f"   Error: {data.get('error', '')[:200]}")
            print("\n   ACTION: Manual redeploy needed on Render!")
            return False
        elif data.get("status") == "success":
            print("   ✓ SUCCESS! Quiz solved!")
            return True
        elif "quota" in str(data).lower() or "rate" in str(data).lower():
            print("   ⚠ API quota issue (but browser works!)")
            print("   ✓ Deployment is good, just need OpenAI credits")
            return True
        else:
            print(f"   Response: {json.dumps(data, indent=2)}")
            return False
            
    except requests.Timeout:
        print("   ⏱ Timeout (may be processing, try again)")
        return None
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    result = check_deployment()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if result is True:
        print("✓ Deployment is WORKING correctly!")
        print("  Browser is installed and functional")
        print("  Ready for quiz evaluation")
    elif result is False:
        print("✗ Deployment has ISSUES")
        print("  Action needed: Trigger manual redeploy on Render")
        print("  See: RENDER_MANUAL_DEPLOY.md")
    else:
        print("⚠ Status UNCLEAR")
        print("  Service may still be deploying")
        print("  Wait 2-3 minutes and run this script again")
    
    print("=" * 70)
