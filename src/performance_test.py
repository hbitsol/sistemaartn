#!/usr/bin/env python3
"""
Performance test script for the Franchise Pricing CRM system
Tests response times and concurrent requests
"""

import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics

BASE_URL = "http://localhost:5000/api"

def measure_response_time(endpoint, method='GET', data=None):
    """Measure response time for an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    start_time = time.time()
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            'success': response.status_code < 400,
            'response_time': response_time,
            'status_code': response.status_code
        }
    except Exception as e:
        end_time = time.time()
        return {
            'success': False,
            'response_time': (end_time - start_time) * 1000,
            'error': str(e)
        }

def concurrent_test(endpoint, method='GET', data=None, num_requests=10):
    """Test concurrent requests to an endpoint"""
    print(f"\n🔄 Testing {num_requests} concurrent requests to {endpoint}...")
    
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(measure_response_time, endpoint, method, data) 
                  for _ in range(num_requests)]
        
        results = [future.result() for future in futures]
    
    # Calculate statistics
    response_times = [r['response_time'] for r in results if r['success']]
    success_count = sum(1 for r in results if r['success'])
    
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
    else:
        avg_time = min_time = max_time = median_time = 0
    
    print(f"✅ Success Rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")
    print(f"📊 Response Times (ms):")
    print(f"   Average: {avg_time:.2f}")
    print(f"   Median:  {median_time:.2f}")
    print(f"   Min:     {min_time:.2f}")
    print(f"   Max:     {max_time:.2f}")
    
    return {
        'endpoint': endpoint,
        'success_rate': success_count/num_requests,
        'avg_response_time': avg_time,
        'median_response_time': median_time,
        'min_response_time': min_time,
        'max_response_time': max_time
    }

def run_performance_tests():
    """Run comprehensive performance tests"""
    print("🚀 Starting performance tests...")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Materials API
    result = concurrent_test('/materials', 'GET', num_requests=20)
    test_results.append(result)
    
    # Test 2: Difficulty Factors API
    result = concurrent_test('/difficulty-factors', 'GET', num_requests=20)
    test_results.append(result)
    
    # Test 3: Pricing Calculation
    pricing_data = {
        "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
        "quantity": 10,
        "difficulty_id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276"
    }
    result = concurrent_test('/calculate-price', 'POST', pricing_data, num_requests=15)
    test_results.append(result)
    
    # Test 4: Dashboard Stats
    result = concurrent_test('/dashboard/stats?franchisee_id=2dc82321-5f18-46f6-af0f-2b9a0f84e136', 'GET', num_requests=10)
    test_results.append(result)
    
    # Test 5: AI Virtual Assistant
    ai_data = {"question": "Qual a melhor tinta para cozinha?"}
    result = concurrent_test('/ai/virtual-assistant', 'POST', ai_data, num_requests=5)
    test_results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    for result in test_results:
        print(f"\n{result['endpoint']}:")
        print(f"  Success Rate: {result['success_rate']*100:.1f}%")
        print(f"  Avg Response: {result['avg_response_time']:.2f}ms")
        print(f"  Performance: {'🟢 GOOD' if result['avg_response_time'] < 1000 else '🟡 SLOW' if result['avg_response_time'] < 3000 else '🔴 POOR'}")
    
    # Overall assessment
    avg_response_times = [r['avg_response_time'] for r in test_results]
    overall_avg = statistics.mean(avg_response_times)
    
    print(f"\n🎯 Overall Average Response Time: {overall_avg:.2f}ms")
    
    if overall_avg < 1000:
        print("🎉 EXCELLENT performance! System is ready for production.")
    elif overall_avg < 3000:
        print("✅ GOOD performance. System is acceptable for production.")
    else:
        print("⚠️  SLOW performance. Consider optimization before production.")

if __name__ == "__main__":
    run_performance_tests()
