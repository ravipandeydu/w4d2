#!/usr/bin/env python3
"""
Demo script for Smart Meeting Assistant MCP Server
Shows how to interact with all 8 MCP tools
"""

import json
import asyncio
from datetime import datetime, timedelta, timezone
from src.server import SmartMeetingAssistant

def print_json(data, title=""):
    """Pretty print JSON data"""
    if title:
        print(f"\n📋 {title}")
        print("-" * 50)
    print(json.dumps(data, indent=2, default=str))

def demo_all_tools():
    """Demonstrate all 8 MCP tools with realistic examples"""
    print("🚀 Smart Meeting Assistant MCP Server Demo")
    print("=" * 60)
    
    # Initialize the assistant
    assistant = SmartMeetingAssistant()
    
    # 1. Create Meeting
    print("\n1️⃣ CREATE MEETING")
    meeting_result = assistant.create_meeting(
        title="Product Strategy Session",
        participants=["alice@company.com", "diana@company.com", "frank@company.com"],
        duration=90,
        preferences={
            "agenda": "Discuss Q2 product roadmap and feature priorities",
            "preferred_time": (datetime.now(timezone.utc) + timedelta(days=2, hours=10)).isoformat()
        }
    )
    print_json({
        "success": meeting_result["success"],
        "meeting_id": meeting_result.get("meeting_id"),
        "conflicts_detected": meeting_result.get("conflicts", {}).get("has_conflicts", False),
        "message": meeting_result.get("message")
    }, "Meeting Creation Result")
    
    # 2. Find Optimal Slots
    print("\n2️⃣ FIND OPTIMAL TIME SLOTS")
    slots_result = assistant.find_optimal_slots(
        participants=["alice@company.com", "bob@company.com", "charlie@company.com"],
        duration=60,
        date_range={"days_ahead": 7}
    )
    
    top_slots = slots_result.get("slots", [])[:3]
    print_json({
        "total_slots_found": len(slots_result.get("slots", [])),
        "top_3_recommendations": [
            {
                "time": slot["start_time"][:16],
                "score": slot["score"],
                "available_participants": len(slot["available_participants"])
            } for slot in top_slots
        ]
    }, "Optimal Time Slots")
    
    # 3. Detect Scheduling Conflicts
    print("\n3️⃣ DETECT SCHEDULING CONFLICTS")
    conflict_time = datetime.now(timezone.utc) + timedelta(days=1, hours=14)
    conflicts_result = assistant.detect_scheduling_conflicts(
        user_id="alice@company.com",
        time_range=(conflict_time, conflict_time + timedelta(hours=1))
    )
    
    print_json({
        "user": conflicts_result["user_id"],
        "time_checked": conflicts_result["time_range"][0][:16],
        "has_conflicts": conflicts_result["has_conflicts"],
        "conflict_count": conflicts_result["conflict_count"],
        "conflicts": [{
            "title": c["title"],
            "overlap_minutes": c["overlap_minutes"]
        } for c in conflicts_result.get("conflicts", [])]
    }, "Conflict Detection")
    
    # 4. Analyze Meeting Patterns
    print("\n4️⃣ ANALYZE MEETING PATTERNS")
    patterns_result = assistant.analyze_meeting_patterns(
        user_id="alice@company.com",
        period="month"
    )
    
    analysis = patterns_result.get("analysis", {})
    print_json({
        "total_meetings": analysis.get("total_meetings"),
        "total_hours": analysis.get("total_hours"),
        "meetings_per_day": analysis.get("meetings_per_day"),
        "effectiveness_score": analysis.get("average_effectiveness_score"),
        "most_common_day": max(analysis.get("day_frequency", {}), key=analysis.get("day_frequency", {}).get, default="N/A"),
        "productivity_insights": analysis.get("productivity_insights", [])[:2]
    }, "Meeting Pattern Analysis")
    
    # 5. Generate Agenda Suggestions
    print("\n5️⃣ GENERATE SMART AGENDA")
    agenda_result = assistant.generate_agenda_suggestions(
        meeting_topic="Sprint Retrospective",
        participants=["alice@company.com", "bob@company.com", "grace@company.com", "henry@company.com"]
    )
    
    agenda = agenda_result.get("suggested_agenda", {})
    print_json({
        "meeting_topic": agenda_result["meeting_topic"],
        "estimated_duration": agenda.get("estimated_duration"),
        "agenda_items": [
            {
                "item": item["item"],
                "type": item["type"],
                "time_allocated": agenda.get("time_allocation", {}).get(item["item"], 0)
            } for item in agenda.get("items", [])[:5]
        ],
        "preparation_tips": agenda_result.get("preparation_tips", [])[:3]
    }, "Smart Agenda Generation")
    
    # 6. Calculate Workload Balance
    print("\n6️⃣ CALCULATE WORKLOAD BALANCE")
    workload_result = assistant.calculate_workload_balance([
        "alice@company.com", "bob@company.com", "charlie@company.com", "diana@company.com"
    ])
    
    stats = workload_result.get("team_statistics", {})
    workload_analysis = workload_result.get("workload_analysis", {})
    
    individual_scores = {
        member: data.get("workload_score", 0) 
        for member, data in workload_analysis.items()
    }
    
    print_json({
        "team_size": len(workload_result.get("team_members", [])),
        "avg_daily_hours": stats.get("avg_daily_hours"),
        "avg_workload_score": stats.get("avg_workload_score"),
        "most_loaded": stats.get("max_workload_member"),
        "least_loaded": stats.get("min_workload_member"),
        "individual_scores": individual_scores,
        "recommendations": workload_result.get("balance_recommendations", [])[:2]
    }, "Workload Balance Analysis")
    
    # 7. Score Meeting Effectiveness
    print("\n7️⃣ SCORE MEETING EFFECTIVENESS")
    meeting_ids = list(assistant.meetings.keys())
    if meeting_ids:
        effectiveness_result = assistant.score_meeting_effectiveness(meeting_ids[0])
        
        print_json({
            "meeting_title": effectiveness_result.get("meeting_title"),
            "overall_score": effectiveness_result.get("overall_score"),
            "effectiveness_rating": effectiveness_result.get("effectiveness_rating"),
            "score_breakdown": effectiveness_result.get("score_components", {}),
            "improvement_suggestions": effectiveness_result.get("improvement_suggestions", [])[:3]
        }, "Meeting Effectiveness Score")
    
    # 8. Optimize Meeting Schedule
    print("\n8️⃣ OPTIMIZE MEETING SCHEDULE")
    optimization_result = assistant.optimize_meeting_schedule("alice@company.com")
    
    schedule_analysis = optimization_result.get("current_schedule_analysis", {})
    savings = optimization_result.get("potential_time_savings", {})
    optimizations = optimization_result.get("optimization_recommendations", [])
    
    print_json({
        "current_issues": schedule_analysis.get("issues", []),
        "optimization_count": len(optimizations),
        "potential_time_savings": {
            "hours_per_week": savings.get("time_saved_hours_per_week"),
            "productivity_gain": f"{savings.get('productivity_gain_percent', 0)}%",
            "monthly_benefit": savings.get("estimated_monthly_benefit")
        },
        "top_recommendations": [
            {
                "description": opt["description"],
                "priority": opt["priority"],
                "action": opt["action"]
            } for opt in optimizations[:3]
        ]
    }, "Schedule Optimization")
    
    # Summary
    print("\n" + "=" * 60)
    print("✨ DEMO COMPLETE - All 8 MCP Tools Demonstrated!")
    print("=" * 60)
    print("\n🎯 Key AI Features Showcased:")
    print("   ✓ Intelligent meeting scheduling with conflict detection")
    print("   ✓ AI-powered optimal time slot recommendations")
    print("   ✓ Advanced meeting pattern analysis and insights")
    print("   ✓ Context-aware agenda generation")
    print("   ✓ Smart workload balancing across team members")
    print("   ✓ Automated meeting effectiveness scoring")
    print("   ✓ Personalized schedule optimization")
    print("   ✓ Multi-timezone support and preferences")
    
    print("\n📊 Sample Data Includes:")
    print(f"   • {len(assistant.meetings)} meetings across multiple time zones")
    print(f"   • {len(assistant.user_preferences)} users with different preferences")
    print("   • Various meeting types: standups, planning, reviews, brainstorms")
    print("   • Effectiveness scores and productivity insights")
    
    print("\n🚀 Ready for MCP Integration!")
    print("   Run 'python src/server.py' to start the MCP server")

if __name__ == "__main__":
    demo_all_tools()