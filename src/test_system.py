#!/usr/bin/env python3
"""
Comprehensive test script for the Franchise Pricing CRM system
Tests all APIs and functionalities
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"
FRANCHISEE_ID = "2dc82321-5f18-46f6-af0f-2b9a0f84e136"

def test_api_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint and return the result"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        elif method.upper() == 'DELETE':
            response = requests.delete(url)
        
        success = response.status_code == expected_status
        return {
            'success': success,
            'status_code': response.status_code,
            'data': response.json() if response.content else None,
            'error': None if success else f"Expected {expected_status}, got {response.status_code}"
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'data': None,
            'error': str(e)
        }

def run_tests():
    """Run comprehensive tests for all system functionalities"""
    print("🚀 Starting comprehensive system tests...")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Seed Data
    print("\n📊 Testing Seed Data...")
    result = test_api_endpoint('POST', '/seed-data', expected_status=201)
    test_results.append(('Seed Data', result))
    print(f"✅ Seed Data: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 2: Materials API
    print("\n🧱 Testing Materials API...")
    result = test_api_endpoint('GET', '/materials')
    test_results.append(('Get Materials', result))
    print(f"✅ Get Materials: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 3: Difficulty Factors API
    print("\n⚡ Testing Difficulty Factors API...")
    result = test_api_endpoint('GET', '/difficulty-factors')
    test_results.append(('Get Difficulty Factors', result))
    print(f"✅ Get Difficulty Factors: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 4: Pricing Calculation
    print("\n💰 Testing Pricing Calculation...")
    pricing_data = {
        "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
        "quantity": 10,
        "difficulty_id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276"
    }
    result = test_api_endpoint('POST', '/calculate-price', pricing_data)
    test_results.append(('Calculate Price', result))
    print(f"✅ Calculate Price: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 5: Client Management
    print("\n👥 Testing Client Management...")
    
    # Create client
    client_data = {
        "nome": "Test Client",
        "email": "test@example.com",
        "telefone": "(11) 99999-9999",
        "endereco": "Test Address",
        "id_franqueado": FRANCHISEE_ID
    }
    result = test_api_endpoint('POST', '/clients', client_data, expected_status=201)
    test_results.append(('Create Client', result))
    print(f"✅ Create Client: {'PASS' if result['success'] else 'FAIL'}")
    
    client_id = None
    if result['success'] and result['data']:
        client_id = result['data']['client']['id']
    
    # Get clients
    result = test_api_endpoint('GET', f'/clients?franchisee_id={FRANCHISEE_ID}')
    test_results.append(('Get Clients', result))
    print(f"✅ Get Clients: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 6: Dashboard Stats
    print("\n📈 Testing Dashboard Stats...")
    result = test_api_endpoint('GET', f'/dashboard/stats?franchisee_id={FRANCHISEE_ID}')
    test_results.append(('Dashboard Stats', result))
    print(f"✅ Dashboard Stats: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 7: AI Assistant Features
    print("\n🤖 Testing AI Assistant Features...")
    
    # Virtual Assistant
    ai_data = {"question": "Qual a melhor tinta para cozinha?"}
    result = test_api_endpoint('POST', '/ai/virtual-assistant', ai_data)
    test_results.append(('AI Virtual Assistant', result))
    print(f"✅ AI Virtual Assistant: {'PASS' if result['success'] else 'FAIL'}")
    
    # Material Suggestions
    suggestion_data = {
        "project_type": "Reforma de sala",
        "room_type": "sala",
        "budget_range": "medio",
        "style": "moderno"
    }
    result = test_api_endpoint('POST', '/ai/suggest-materials', suggestion_data)
    test_results.append(('AI Material Suggestions', result))
    print(f"✅ AI Material Suggestions: {'PASS' if result['success'] else 'FAIL'}")
    
    # Project Description Generation
    description_data = {
        "materials": [
            {"name": "MDF 15mm", "quantity": "10", "unit": "m²"},
            {"name": "Tinta Acrílica", "quantity": "2", "unit": "L"}
        ],
        "client_info": {"name": "Test Client"},
        "project_type": "Reforma de sala"
    }
    result = test_api_endpoint('POST', '/ai/generate-project-description', description_data)
    test_results.append(('AI Project Description', result))
    print(f"✅ AI Project Description: {'PASS' if result['success'] else 'FAIL'}")
    
    # Pricing Trends Analysis
    trends_data = {"franchisee_id": FRANCHISEE_ID}
    result = test_api_endpoint('POST', '/ai/analyze-pricing-trends', trends_data)
    test_results.append(('AI Pricing Trends', result))
    print(f"✅ AI Pricing Trends: {'PASS' if result['success'] else 'FAIL'}")
    
    # Test 8: Cleanup (Delete test client if created)
    if client_id:
        print("\n🧹 Cleaning up test data...")
        result = test_api_endpoint('DELETE', f'/clients/{client_id}')
        test_results.append(('Delete Test Client', result))
        print(f"✅ Delete Test Client: {'PASS' if result['success'] else 'FAIL'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "PASS" if result['success'] else "FAIL"
        print(f"{test_name:.<40} {status}")
        if result['success']:
            passed += 1
        else:
            failed += 1
            if result['error']:
                print(f"   Error: {result['error']}")
    
    print("-" * 60)
    print(f"Total Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for deployment.")
    else:
        print(f"\n⚠️  {failed} tests failed. Please review the issues above.")
    
    return test_results

if __name__ == "__main__":
    run_tests()
