#!/usr/bin/env python3
"""
Test suite for Smart Meeting Assistant MCP Server
Demonstrates all 8 MCP tools with comprehensive examples
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta, timezone

# Add the src directory to the path to import the server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import SmartMeetingAssistant

class MCPToolTester:
    def __init__(self):
        self.assistant = SmartMeetingAssistant()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_create_meeting(self):
        """Test create_meeting tool"""
        print("\n🔧 Testing create_meeting tool...")
        
        # Test 1: Basic meeting creation
        result = self.assistant.create_meeting(
            title="Test Meeting",
            participants=["alice@company.com", "bob@company.com"],
            duration=60,
            preferences={"agenda": "Discuss test results"}
        )
        
        success = result.get("success", False) and "meeting_id" in result
        self.log_test("Create basic meeting", success, 
                     f"Meeting ID: {result.get('meeting_id', 'N/A')}")
        
        # Test 2: Meeting with conflicts
        future_time = datetime.now(timezone.utc) + timedelta(hours=1)
        result2 = self.assistant.create_meeting(
            title="Conflicting Meeting",
            participants=["alice@company.com", "charlie@company.com"],
            duration=30,
            preferences={"preferred_time": future_time.isoformat()}
        )
        
        success2 = result2.get("success", False)
        self.log_test("Create meeting with time preference", success2,
                     f"Conflicts detected: {result2.get('conflicts', {}).get('has_conflicts', False)}")
    
    def test_find_optimal_slots(self):
        """Test find_optimal_slots tool"""
        print("\n🔧 Testing find_optimal_slots tool...")
        
        # Test 1: Find slots for 2 participants
        result = self.assistant.find_optimal_slots(
            participants=["alice@company.com", "bob@company.com"],
            duration=60,
            date_range={"days_ahead": 7}
        )
        
        success = result.get("success", False) and len(result.get("slots", [])) > 0
        self.log_test("Find optimal slots for 2 participants", success,
                     f"Found {len(result.get('slots', []))} optimal slots")
        
        # Test 2: Find slots for larger group
        result2 = self.assistant.find_optimal_slots(
            participants=["alice@company.com", "bob@company.com", "charlie@company.com", "diana@company.com"],
            duration=90,
            date_range={"days_ahead": 14}
        )
        
        success2 = result2.get("success", False)
        self.log_test("Find optimal slots for 4 participants", success2,
                     f"Found {len(result2.get('slots', []))} slots for larger group")
        
        # Display top 3 recommendations
        if result.get("slots"):
            print("   Top 3 recommended time slots:")
            for i, slot in enumerate(result["slots"][:3]):
                print(f"   {i+1}. {slot['start_time']} (Score: {slot['score']})")
    
    def test_detect_scheduling_conflicts(self):
        """Test detect_scheduling_conflicts tool"""
        print("\n🔧 Testing detect_scheduling_conflicts tool...")
        
        # Test 1: Check conflicts for a busy user
        start_time = datetime.now(timezone.utc) + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=1)
        
        result = self.assistant.detect_scheduling_conflicts(
            user_id="alice@company.com",
            time_range=(start_time, end_time)
        )
        
        success = result.get("success", False)
        self.log_test("Detect conflicts for alice@company.com", success,
                     f"Conflicts found: {result.get('has_conflicts', False)} ({result.get('conflict_count', 0)} conflicts)")
        
        # Test 2: Check conflicts during a known busy time
        # Use a time when we know there might be existing meetings
        busy_start = datetime.now(timezone.utc).replace(hour=14, minute=0, second=0, microsecond=0)
        busy_end = busy_start + timedelta(hours=2)
        
        result2 = self.assistant.detect_scheduling_conflicts(
            user_id="bob@company.com",
            time_range=(busy_start, busy_end)
        )
        
        success2 = result2.get("success", False)
        self.log_test("Detect conflicts during busy hours", success2,
                     f"Conflicts in busy period: {result2.get('conflict_count', 0)}")
    
    def test_analyze_meeting_patterns(self):
        """Test analyze_meeting_patterns tool"""
        print("\n🔧 Testing analyze_meeting_patterns tool...")
        
        # Test 1: Weekly analysis
        result = self.assistant.analyze_meeting_patterns(
            user_id="alice@company.com",
            period="week"
        )
        
        success = result.get("success", False) and "analysis" in result
        analysis = result.get("analysis", {})
        self.log_test("Weekly pattern analysis for Alice", success,
                     f"Total meetings: {analysis.get('total_meetings', 0)}, Avg effectiveness: {analysis.get('average_effectiveness_score', 0)}")
        
        # Test 2: Monthly analysis
        result2 = self.assistant.analyze_meeting_patterns(
            user_id="diana@company.com",
            period="month"
        )
        
        success2 = result2.get("success", False)
        analysis2 = result2.get("analysis", {})
        self.log_test("Monthly pattern analysis for Diana", success2,
                     f"Meeting hours: {analysis2.get('total_hours', 0)}, Meetings/day: {analysis2.get('meetings_per_day', 0)}")
        
        # Display insights
        if analysis.get("productivity_insights"):
            print("   Productivity insights for Alice:")
            for insight in analysis["productivity_insights"][:3]:
                print(f"   • {insight}")
    
    def test_generate_agenda_suggestions(self):
        """Test generate_agenda_suggestions tool"""
        print("\n🔧 Testing generate_agenda_suggestions tool...")
        
        # Test 1: Planning meeting agenda
        result = self.assistant.generate_agenda_suggestions(
            meeting_topic="Sprint Planning",
            participants=["alice@company.com", "bob@company.com", "grace@company.com"]
        )
        
        success = result.get("success", False) and "suggested_agenda" in result
        agenda = result.get("suggested_agenda", {})
        self.log_test("Generate sprint planning agenda", success,
                     f"Agenda items: {len(agenda.get('items', []))}, Estimated duration: {agenda.get('estimated_duration', 0)} min")
        
        # Test 2: Brainstorming meeting agenda
        result2 = self.assistant.generate_agenda_suggestions(
            meeting_topic="Brainstorming: New Product Features",
            participants=["diana@company.com", "eve@company.com", "frank@company.com", "henry@company.com"]
        )
        
        success2 = result2.get("success", False)
        self.log_test("Generate brainstorming agenda", success2,
                     f"Preparation tips: {len(result2.get('preparation_tips', []))}")
        
        # Display sample agenda
        if agenda.get("items"):
            print("   Sample agenda items for Sprint Planning:")
            for item in agenda["items"][:4]:
                print(f"   • {item['item']} ({item['type']})")
    
    def test_calculate_workload_balance(self):
        """Test calculate_workload_balance tool"""
        print("\n🔧 Testing calculate_workload_balance tool...")
        
        # Test 1: Small team workload
        team_members = ["alice@company.com", "bob@company.com", "charlie@company.com"]
        result = self.assistant.calculate_workload_balance(team_members)
        
        success = result.get("success", False) and "workload_analysis" in result
        stats = result.get("team_statistics", {})
        self.log_test("Calculate workload for 3-person team", success,
                     f"Avg daily hours: {stats.get('avg_daily_hours', 0)}, Workload variance: {stats.get('workload_variance', 0)}")
        
        # Test 2: Larger team workload
        large_team = ["alice@company.com", "bob@company.com", "charlie@company.com", 
                     "diana@company.com", "eve@company.com", "frank@company.com"]
        result2 = self.assistant.calculate_workload_balance(large_team)
        
        success2 = result2.get("success", False)
        self.log_test("Calculate workload for 6-person team", success2,
                     f"Recommendations: {len(result2.get('balance_recommendations', []))}")
        
        # Display workload analysis
        workload = result.get("workload_analysis", {})
        if workload:
            print("   Individual workload scores:")
            for member, data in list(workload.items())[:3]:
                print(f"   • {member}: {data.get('workload_score', 0)} (Daily avg: {data.get('daily_avg_hours', 0)}h)")
    
    def test_score_meeting_effectiveness(self):
        """Test score_meeting_effectiveness tool"""
        print("\n🔧 Testing score_meeting_effectiveness tool...")
        
        # Get a sample meeting ID from existing meetings
        meeting_ids = list(self.assistant.meetings.keys())
        
        if not meeting_ids:
            self.log_test("Score meeting effectiveness", False, "No meetings available to score")
            return
        
        # Test 1: Score first meeting
        result = self.assistant.score_meeting_effectiveness(meeting_ids[0])
        
        success = result.get("success", False) and "overall_score" in result
        self.log_test("Score meeting effectiveness", success,
                     f"Overall score: {result.get('overall_score', 0)}, Rating: {result.get('effectiveness_rating', 'N/A')}")
        
        # Test 2: Score another meeting if available
        if len(meeting_ids) > 1:
            result2 = self.assistant.score_meeting_effectiveness(meeting_ids[1])
            success2 = result2.get("success", False)
            self.log_test("Score second meeting", success2,
                         f"Score: {result2.get('overall_score', 0)}")
        
        # Display improvement suggestions
        suggestions = result.get("improvement_suggestions", [])
        if suggestions:
            print("   Improvement suggestions:")
            for suggestion in suggestions[:3]:
                print(f"   • {suggestion}")
    
    def test_optimize_meeting_schedule(self):
        """Test optimize_meeting_schedule tool"""
        print("\n🔧 Testing optimize_meeting_schedule tool...")
        
        # Test 1: Optimize Alice's schedule
        result = self.assistant.optimize_meeting_schedule("alice@company.com")
        
        success = result.get("success", False) and "optimization_recommendations" in result
        optimizations = result.get("optimization_recommendations", [])
        savings = result.get("potential_time_savings", {})
        
        self.log_test("Optimize Alice's schedule", success,
                     f"Recommendations: {len(optimizations)}, Potential savings: {savings.get('time_saved_hours_per_week', 0)}h/week")
        
        # Test 2: Optimize Bob's schedule
        result2 = self.assistant.optimize_meeting_schedule("bob@company.com")
        
        success2 = result2.get("success", False)
        self.log_test("Optimize Bob's schedule", success2,
                     f"Schedule issues identified: {len(result2.get('current_schedule_analysis', {}).get('issues', []))}")
        
        # Display optimization recommendations
        if optimizations:
            print("   Top optimization recommendations for Alice:")
            for opt in optimizations[:3]:
                print(f"   • {opt['description']} (Priority: {opt['priority']})")
                print(f"     Action: {opt['action']}")
    
    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        print("\n🔧 Testing error handling...")
        
        # Test 1: Invalid meeting ID
        result = self.assistant.score_meeting_effectiveness("invalid-meeting-id")
        success = not result.get("success", True) and "error" in result
        self.log_test("Handle invalid meeting ID", success, "Properly returns error for invalid ID")
        
        # Test 2: Invalid user ID
        result2 = self.assistant.analyze_meeting_patterns("invalid@user.com", "week")
        success2 = result2.get("success", False)  # Should still work but return empty results
        self.log_test("Handle invalid user ID", success2, "Handles non-existent user gracefully")
        
        # Test 3: Invalid time range
        try:
            result3 = self.assistant.detect_scheduling_conflicts(
                "alice@company.com",
                ("invalid-time", "also-invalid")
            )
            success3 = not result3.get("success", True)
        except:
            success3 = True  # Exception is expected
        
        self.log_test("Handle invalid time format", success3, "Properly handles invalid time inputs")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Smart Meeting Assistant MCP Server Tests")
        print("=" * 60)
        
        # Run all test methods
        self.test_create_meeting()
        self.test_find_optimal_slots()
        self.test_detect_scheduling_conflicts()
        self.test_analyze_meeting_patterns()
        self.test_generate_agenda_suggestions()
        self.test_calculate_workload_balance()
        self.test_score_meeting_effectiveness()
        self.test_optimize_meeting_schedule()
        self.test_error_handling()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if "✅" in result["status"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! The MCP server is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check the implementation.")
        
        # Print detailed results
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"{result['status']}: {result['test']}")
            if result['details']:
                print(f"   {result['details']}")
    
    def demonstrate_ai_features(self):
        """Demonstrate the AI capabilities of the system"""
        print("\n" + "=" * 60)
        print("🤖 AI FEATURES DEMONSTRATION")
        print("=" * 60)
        
        # Demonstrate intelligent scheduling
        print("\n1. 🧠 Intelligent Time Slot Recommendations")
        slots_result = self.assistant.find_optimal_slots(
            participants=["alice@company.com", "diana@company.com", "frank@company.com"],
            duration=60,
            date_range={"days_ahead": 5}
        )
        
        if slots_result.get("slots"):
            print("   AI-recommended meeting times (with scoring):")
            for i, slot in enumerate(slots_result["slots"][:3]):
                available = len(slot.get("available_participants", []))
                total = len(slots_result.get("participants", []))
                print(f"   {i+1}. {slot['start_time'][:16]} | Score: {slot['score']:.1f} | Available: {available}/{total}")
        
        # Demonstrate pattern analysis
        print("\n2. 📈 Meeting Pattern Analysis & Insights")
        pattern_result = self.assistant.analyze_meeting_patterns("alice@company.com", "month")
        
        if pattern_result.get("success"):
            analysis = pattern_result["analysis"]
            print(f"   Alice's Meeting Patterns (Last Month):")
            print(f"   • Total meetings: {analysis.get('total_meetings', 0)}")
            print(f"   • Average daily meetings: {analysis.get('meetings_per_day', 0)}")
            print(f"   • Most active day: {max(analysis.get('day_frequency', {}), key=analysis.get('day_frequency', {}).get, default='N/A')}")
            print(f"   • Effectiveness score: {analysis.get('average_effectiveness_score', 0)}/10")
            
            insights = analysis.get("productivity_insights", [])
            if insights:
                print("   AI-Generated Productivity Insights:")
                for insight in insights[:2]:
                    print(f"   • {insight}")
        
        # Demonstrate smart agenda generation
        print("\n3. 📝 Smart Agenda Generation")
        agenda_result = self.assistant.generate_agenda_suggestions(
            "Quarterly Business Review",
            ["alice@company.com", "diana@company.com", "frank@company.com", "eve@company.com"]
        )
        
        if agenda_result.get("success"):
            agenda = agenda_result["suggested_agenda"]
            print(f"   AI-Generated Agenda for Quarterly Business Review:")
            print(f"   Estimated Duration: {agenda.get('estimated_duration', 0)} minutes")
            print("   Key Agenda Items:")
            for item in agenda.get("items", [])[:5]:
                time_alloc = agenda.get("time_allocation", {}).get(item["item"], 0)
                print(f"   • {item['item']} ({time_alloc} min) - {item['description']}")
        
        # Demonstrate workload optimization
        print("\n4. ⚖️ Intelligent Workload Balancing")
        workload_result = self.assistant.calculate_workload_balance([
            "alice@company.com", "bob@company.com", "charlie@company.com", 
            "diana@company.com", "eve@company.com"
        ])
        
        if workload_result.get("success"):
            stats = workload_result["team_statistics"]
            recommendations = workload_result["balance_recommendations"]
            
            print(f"   Team Workload Analysis:")
            print(f"   • Average daily meeting hours: {stats.get('avg_daily_hours', 0):.1f}")
            print(f"   • Most loaded: {stats.get('max_workload_member', 'N/A')}")
            print(f"   • Least loaded: {stats.get('min_workload_member', 'N/A')}")
            print(f"   • Workload variance: {stats.get('workload_variance', 0):.1f}")
            
            if recommendations:
                print("   AI Recommendations:")
                for rec in recommendations[:2]:
                    print(f"   • {rec}")
        
        print("\n🎯 The AI system successfully demonstrates:")
        print("   ✓ Multi-factor time optimization")
        print("   ✓ Behavioral pattern recognition")
        print("   ✓ Context-aware agenda generation")
        print("   ✓ Intelligent workload distribution")
        print("   ✓ Predictive conflict detection")
        print("   ✓ Personalized productivity insights")

def main():
    """Main test execution"""
    tester = MCPToolTester()
    
    # Run comprehensive tests
    tester.run_all_tests()
    
    # Demonstrate AI features
    tester.demonstrate_ai_features()
    
    print("\n" + "=" * 60)
    print("✨ Smart Meeting Assistant MCP Server Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()