#!/usr/bin/env python3
"""
Comprehensive stress test for LLM implementation with complex NLP queries
"""

import time
import json
from src.LLM_Implementaion import llm_implementation

def stress_test_llm():
    """Stress test the LLM implementation with various complex NLP queries"""
    
    print("🚀 COMPREHENSIVE LLM STRESS TEST")
    print("=" * 80)
    
    # Complex test queries covering different patterns and complexity levels
    test_queries = [
        # Basic queries
        "Show all cases",
        "List my accounts", 
        "Get contact information",
        
        # Time-based queries
        "Show cases created today",
        "List accounts modified last week",
        "Get leads from this month",
        "Find opportunities closed yesterday",
        "Display tasks due next week",
        
        # Multi-filter queries
        "Show high priority cases with status New",
        "List active accounts in North region",
        "Get closed opportunities worth over 50000",
        "Find urgent tasks assigned to John Smith",
        
        # Complex relationship queries
        "Show cases for account Vinod with high priority",
        "List all contacts from accounts in California",
        "Get opportunities for accounts managed by Sarah",
        "Find cases related to product issues for VIP customers",
        
        # Aggregation queries
        "Count total cases by status",
        "Sum revenue from closed opportunities",
        "Average case resolution time by priority",
        "Show top 5 performing sales reps",
        
        # Complex time and filter combinations
        "Show my top 10 cases created in last month for account Vinod with status as New and priority as High",
        "List all urgent support tickets opened this week for enterprise customers",
        "Get high-value opportunities closing this quarter in the West region",
        "Find overdue tasks for critical accounts assigned to the support team",
        
        # Edge cases and challenging queries
        "Show me everything about customer Microsoft",
        "List all data related to product launches",
        "Get complete information for account ID 12345",
        "Find all records containing the word 'urgent'",
        
        # Ambiguous queries
        "Show recent activity",
        "List important items",
        "Get pending requests",
        "Find updated records",
        
        # Complex business logic
        "Show cases that have been open for more than 30 days with no activity",
        "List accounts with no opportunities created in last 6 months",
        "Get contacts who haven't been contacted in 90 days",
        "Find duplicate leads based on email and company",
        
        # Multi-entity complex queries
        "Show cases with related accounts, contacts, and activities",
        "List opportunities with associated products, quotes, and competitors",
        "Get accounts with their primary contacts, open cases, and revenue",
        "Find leads with matching accounts and their conversion status"
    ]
    
    print(f"Testing {len(test_queries)} complex queries...")
    print("=" * 80)
    
    results = []
    total_time = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i:2d}: {query[:60]}{'...' if len(query) > 60 else ''}")
        
        start_time = time.time()
        success = False
        error_msg = ""
        intent_data = None
        
        try:
            intent_data = llm_implementation(query)
            processing_time = time.time() - start_time
            total_time += processing_time
            
            # Validate the response
            if intent_data and isinstance(intent_data, dict):
                has_intent = bool(intent_data.get("intent"))
                has_payload = bool(intent_data.get("payload"))
                
                if has_intent and has_payload:
                    success = True
                    intent = intent_data["intent"]
                    payload = intent_data["payload"]
                    
                    print(f"   ✅ SUCCESS ({processing_time:.3f}s)")
                    print(f"      Intent: {intent.get('intent', 'Unknown')} | Entity: {intent.get('entity', 'Unknown')}")
                    print(f"      Operation: {payload.get('operation', 'Unknown')} | Filters: {len(payload.get('filters', {}).get('conditions', []))}")
                else:
                    error_msg = f"Missing intent: {has_intent}, payload: {has_payload}"
            else:
                error_msg = "Invalid response format"
                
        except Exception as e:
            processing_time = time.time() - start_time
            total_time += processing_time
            error_msg = str(e)
        
        if not success:
            print(f"   ❌ FAILED ({processing_time:.3f}s): {error_msg}")
        
        # Store result
        results.append({
            "query": query,
            "success": success,
            "time": processing_time,
            "error": error_msg if not success else "",
            "intent_data": intent_data if success else None
        })
        
        # Brief pause to avoid overwhelming the system
        time.sleep(0.1)
    
    # Calculate statistics
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    success_rate = len(successful) / len(results) * 100
    avg_time = total_time / len(results)
    
    print(f"\n📊 STRESS TEST RESULTS")
    print("=" * 80)
    print(f"Total Queries:     {len(results)}")
    print(f"Successful:        {len(successful)} ✅")
    print(f"Failed:            {len(failed)} ❌")
    print(f"Success Rate:      {success_rate:.1f}%")
    print(f"Average Time:      {avg_time:.3f} seconds")
    print(f"Total Time:        {total_time:.3f} seconds")
    
    if successful:
        successful_times = [r["time"] for r in successful]
        print(f"Fastest Success:   {min(successful_times):.3f} seconds")
        print(f"Slowest Success:   {max(successful_times):.3f} seconds")
    
    # Show failed queries
    if failed:
        print(f"\n❌ FAILED QUERIES ({len(failed)}):")
        print("-" * 50)
        for result in failed:
            print(f"   • {result['query'][:60]}{'...' if len(result['query']) > 60 else ''}")
            print(f"     Error: {result['error'][:80]}{'...' if len(result['error']) > 80 else ''}")
    
    # Show success categories
    print(f"\n✅ SUCCESS ANALYSIS:")
    print("-" * 50)
    
    # Group by query complexity
    basic_queries = [r for r in successful if len(r["query"].split()) <= 5]
    medium_queries = [r for r in successful if 6 <= len(r["query"].split()) <= 12]
    complex_queries = [r for r in successful if len(r["query"].split()) > 12]
    
    print(f"Basic Queries (≤5 words):     {len(basic_queries)}/{len([r for r in results if len(r['query'].split()) <= 5])}")
    print(f"Medium Queries (6-12 words):  {len(medium_queries)}/{len([r for r in results if 6 <= len(r['query'].split()) <= 12])}")
    print(f"Complex Queries (>12 words):  {len(complex_queries)}/{len([r for r in results if len(r['query'].split()) > 12])}")
    
    # Analyze intent types
    intent_types = {}
    for result in successful:
        if result["intent_data"] and result["intent_data"].get("intent"):
            intent_type = result["intent_data"]["intent"].get("intent", "Unknown")
            intent_types[intent_type] = intent_types.get(intent_type, 0) + 1
    
    print(f"\n🎯 INTENT TYPE DISTRIBUTION:")
    for intent_type, count in sorted(intent_types.items()):
        print(f"   {intent_type}: {count}")
    
    return results, success_rate

def analyze_date_issue():
    """Analyze why the system is showing 2023 dates"""
    
    print(f"\n🔍 INVESTIGATING DATE ISSUE")
    print("=" * 80)
    print(f"Current Date: {time.strftime('%Y-%m-%d')}")
    print(f"Expected Year: 2025")
    
    # Test date-specific queries
    date_queries = [
        "Show cases created today",
        "List accounts from last month", 
        "Get opportunities closing this year",
        "Find tasks due next week"
    ]
    
    print(f"\nTesting date-related queries...")
    
    for query in date_queries:
        print(f"\n📅 Query: {query}")
        try:
            result = llm_implementation(query)
            if result and result.get("intent"):
                intent = result["intent"]
                if "timeRange" in intent:
                    time_range = intent["timeRange"]
                    print(f"   Time Range: {time_range}")
                    
                    # Extract year from timeRange
                    if "from" in time_range:
                        from_date = time_range["from"]
                        if "2023" in from_date:
                            print(f"   ⚠️  ISSUE: Found 2023 in date: {from_date}")
                        else:
                            print(f"   ✅ Date looks correct: {from_date}")
                else:
                    print(f"   No timeRange in intent")
            else:
                print(f"   Failed to get intent")
                
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    print("Starting comprehensive stress test...")
    print(f"Current Date: September 26, 2025")
    print(f"Testing LLM implementation with complex NLP queries\n")
    
    # Run stress test
    results, success_rate = stress_test_llm()
    
    # Investigate date issue
    analyze_date_issue()
    
    print(f"\n🎯 SUMMARY:")
    print(f"Overall Success Rate: {success_rate:.1f}%")
    if success_rate >= 80:
        print("🚀 EXCELLENT: System performing very well!")
    elif success_rate >= 60:
        print("👍 GOOD: System performing adequately")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Success rate below expectations")
    
    print(f"\n📋 Recommendations:")
    if success_rate < 100:
        print("• Review failed queries for pattern analysis")
        print("• Consider improving error handling for edge cases")
    print("• Investigate and fix the 2023 date issue")
    print("• Consider adding more specific entity recognition")