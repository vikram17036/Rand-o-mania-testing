"""
Example test script for the Rand-o-mania API
Run this after starting the server to test the endpoint.
"""

import requests
import json

BASE_URL = "https://zola-unreasoned-jaleesa.ngrok-free.dev"  # Change to your ngrok URL when ready

def test_health():
    """Test health check endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_calculation():
    """Test the main calculation endpoint with example prompt."""
    print("Testing calculation endpoint...")
    
    prompt = (
        "Generate a random number. If the number is less than 0.5, "
        "multiply it by 0.1234567, otherwise divide it by 1.1234567. "
        "Generate another random number, get the square root of it, "
        "and then multiply it by the previous result."
    )
    
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(
            f"{BASE_URL}/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success!")
            print(f"Result: {data['result']}")
            print(f"Random numbers generated: {len(data['random_integers'])}")
            print(f"Random numbers: {data['random_integers']}")
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the server is running!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_basic_multiplication():
    """Test basic multiplication."""
    print("\nTesting basic multiplication...")
    prompt = "Generate a random number and multiply it by 2.5"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(f"{BASE_URL}/", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Result: {data['result']}, Randoms: {data['random_integers']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_basic_division():
    """Test basic division."""
    print("\nTesting basic division...")
    prompt = "Generate a random number and divide it by 1.5"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(f"{BASE_URL}/", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Result: {data['result']}, Randoms: {data['random_integers']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_square_root():
    """Test square root operation."""
    print("\nTesting square root...")
    prompt = "Generate a random number and get the square root of it"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(f"{BASE_URL}/", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Result: {data['result']}, Randoms: {data['random_integers']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_conditional():
    """Test conditional logic."""
    print("\nTesting conditional logic...")
    prompt = "Generate a random number. If the number is less than 0.5, multiply it by 0.1234567, otherwise divide it by 1.1234567"
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(f"{BASE_URL}/", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Result: {data['result']}, Randoms: {data['random_integers']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_multiple_randoms():
    """Test multiple random numbers."""
    print("\nTesting multiple random numbers...")
    prompt = "Generate a random number and multiply it by 2.5. Then generate another random number and divide the result by it."
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(f"{BASE_URL}/", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Result: {data['result']}, Randoms: {data['random_integers']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Rand-o-mania API Test Script")
    print("=" * 50)
    print()
    
    test_health()
    test_calculation()
    test_basic_multiplication()
    test_basic_division()
    test_square_root()
    test_conditional()
    test_multiple_randoms()

