#!/usr/bin/env python3
"""
Smart Meeting Assistant MCP Server
AI-powered meeting scheduling and management system
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import uuid
import random
from collections import defaultdict

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-meeting-assistant")

@dataclass
class Meeting:
    id: str
    title: str
    participants: List[str]
    start_time: datetime
    end_time: datetime
    timezone_str: str
    organizer: str
    agenda: Optional[str] = None
    location: Optional[str] = None
    meeting_type: str = "regular"
    effectiveness_score: Optional[float] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

@dataclass
class UserPreferences:
    user_id: str
    preferred_meeting_hours: Tuple[int, int]  # (start_hour, end_hour)
    timezone_str: str
    max_daily_meetings: int = 8
    preferred_meeting_duration: int = 60  # minutes
    break_time_between_meetings: int = 15  # minutes
    work_days: List[int] = None  # 0=Monday, 6=Sunday
    
    def __post_init__(self):
        if self.work_days is None:
            self.work_days = [0, 1, 2, 3, 4]  # Monday to Friday

class SmartMeetingAssistant:
    def __init__(self):
        self.meetings: Dict[str, Meeting] = {}
        self.user_preferences: Dict[str, UserPreferences] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample meeting data and user preferences"""
        # Sample users with different timezones
        users = [
            ("alice@company.com", "America/New_York", (9, 17)),
            ("bob@company.com", "America/Los_Angeles", (8, 16)),
            ("charlie@company.com", "Europe/London", (9, 18)),
            ("diana@company.com", "Asia/Tokyo", (9, 17)),
            ("eve@company.com", "Australia/Sydney", (8, 16)),
            ("frank@company.com", "America/Chicago", (9, 17)),
            ("grace@company.com", "Europe/Berlin", (8, 17)),
            ("henry@company.com", "Asia/Singapore", (9, 18))
        ]
        
        # Initialize user preferences
        for user_id, tz, hours in users:
            self.user_preferences[user_id] = UserPreferences(
                user_id=user_id,
                preferred_meeting_hours=hours,
                timezone_str=tz,
                max_daily_meetings=random.randint(6, 10),
                preferred_meeting_duration=random.choice([30, 45, 60, 90])
            )
        
        # Generate 60+ sample meetings
        meeting_types = ["standup", "planning", "review", "brainstorm", "1on1", "all-hands"]
        base_time = datetime.now(timezone.utc) - timedelta(days=30)
        
        for i in range(65):  # Generate 65 meetings
            meeting_id = str(uuid.uuid4())
            participants = random.sample([u[0] for u in users], random.randint(2, 5))
            organizer = participants[0]
            
            # Random meeting time within the last 30 days or next 30 days
            days_offset = random.randint(-30, 30)
            hour = random.randint(8, 17)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = base_time + timedelta(days=days_offset, hours=hour, minutes=minute)
            duration = random.choice([30, 45, 60, 90, 120])
            end_time = start_time + timedelta(minutes=duration)
            
            meeting = Meeting(
                id=meeting_id,
                title=f"{random.choice(meeting_types).title()} Meeting {i+1}",
                participants=participants,
                start_time=start_time,
                end_time=end_time,
                timezone_str=self.user_preferences[organizer].timezone_str,
                organizer=organizer,
                meeting_type=random.choice(meeting_types),
                effectiveness_score=random.uniform(3.0, 9.5)
            )
            
            self.meetings[meeting_id] = meeting
    
    def create_meeting(self, title: str, participants: List[str], duration: int, 
                      preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a new meeting with conflict detection"""
        try:
            meeting_id = str(uuid.uuid4())
            organizer = participants[0] if participants else "unknown@company.com"
            
            # Get preferred time from preferences or use default
            preferred_time = preferences.get("preferred_time")
            if preferred_time:
                start_time = datetime.fromisoformat(preferred_time)
            else:
                # Find optimal time slot
                optimal_slots = self.find_optimal_slots(participants, duration, 
                                                       {"days_ahead": 7})
                if optimal_slots["slots"]:
                    start_time = datetime.fromisoformat(optimal_slots["slots"][0]["start_time"])
                else:
                    start_time = datetime.now(timezone.utc) + timedelta(days=1, hours=10)
            
            end_time = start_time + timedelta(minutes=duration)
            
            # Check for conflicts
            conflicts = self.detect_scheduling_conflicts(organizer, 
                                                       (start_time, end_time))
            
            meeting = Meeting(
                id=meeting_id,
                title=title,
                participants=participants,
                start_time=start_time,
                end_time=end_time,
                timezone_str=self.user_preferences.get(organizer, 
                                                      UserPreferences(organizer, (9, 17), "UTC")).timezone_str,
                organizer=organizer,
                agenda=preferences.get("agenda")
            )
            
            self.meetings[meeting_id] = meeting
            
            return {
                "success": True,
                "meeting_id": meeting_id,
                "meeting": asdict(meeting),
                "conflicts": conflicts,
                "message": "Meeting created successfully" if not conflicts["has_conflicts"] 
                          else "Meeting created with conflicts detected"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_optimal_slots(self, participants: List[str], duration: int, 
                          date_range: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered optimal time slot recommendations"""
        try:
            days_ahead = date_range.get("days_ahead", 7)
            start_date = datetime.now(timezone.utc).date()
            end_date = start_date + timedelta(days=days_ahead)
            
            optimal_slots = []
            
            # Analyze each day in the range
            current_date = start_date
            while current_date <= end_date:
                # Skip weekends for most users
                if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                    day_slots = self._find_day_optimal_slots(participants, duration, current_date)
                    optimal_slots.extend(day_slots)
                current_date += timedelta(days=1)
            
            # Sort by score (highest first)
            optimal_slots.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "success": True,
                "slots": optimal_slots[:10],  # Return top 10 slots
                "total_analyzed": len(optimal_slots),
                "participants": participants,
                "duration_minutes": duration
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _find_day_optimal_slots(self, participants: List[str], duration: int, 
                               date: datetime.date) -> List[Dict[str, Any]]:
        """Find optimal slots for a specific day"""
        slots = []
        
        # Check each hour from 8 AM to 6 PM
        for hour in range(8, 18):
            for minute in [0, 30]:  # Check every 30 minutes
                start_time = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
                start_time = start_time.replace(tzinfo=timezone.utc)
                end_time = start_time + timedelta(minutes=duration)
                
                # Calculate score for this time slot
                score = self._calculate_slot_score(participants, start_time, end_time)
                
                if score > 0:  # Only include viable slots
                    slots.append({
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "score": score,
                        "available_participants": self._get_available_participants(participants, start_time, end_time)
                    })
        
        return slots
    
    def _calculate_slot_score(self, participants: List[str], start_time: datetime, 
                             end_time: datetime) -> float:
        """Calculate optimization score for a time slot"""
        score = 100.0  # Base score
        
        # Check participant availability
        available_count = 0
        for participant in participants:
            if self._is_participant_available(participant, start_time, end_time):
                available_count += 1
            else:
                score -= 30  # Heavy penalty for unavailable participants
        
        # Bonus for all participants available
        if available_count == len(participants):
            score += 50
        
        # Check if time is within preferred hours
        hour = start_time.hour
        if 9 <= hour <= 16:  # Peak productivity hours
            score += 20
        elif 8 <= hour <= 17:  # Good hours
            score += 10
        else:
            score -= 20  # Outside normal hours
        
        # Avoid lunch time (12-13)
        if 12 <= hour < 13:
            score -= 15
        
        # Prefer certain days (Tuesday-Thursday are often better)
        weekday = start_time.weekday()
        if weekday in [1, 2, 3]:  # Tuesday, Wednesday, Thursday
            score += 10
        elif weekday in [0, 4]:  # Monday, Friday
            score += 5
        
        return max(0, score)
    
    def _is_participant_available(self, participant: str, start_time: datetime, 
                                 end_time: datetime) -> bool:
        """Check if participant is available during the time slot"""
        for meeting in self.meetings.values():
            if participant in meeting.participants:
                # Check for overlap
                if (start_time < meeting.end_time and end_time > meeting.start_time):
                    return False
        return True
    
    def _get_available_participants(self, participants: List[str], start_time: datetime, 
                                   end_time: datetime) -> List[str]:
        """Get list of available participants for a time slot"""
        available = []
        for participant in participants:
            if self._is_participant_available(participant, start_time, end_time):
                available.append(participant)
        return available
    
    def detect_scheduling_conflicts(self, user_id: str, 
                                   time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Detect scheduling conflicts for a user"""
        try:
            start_time, end_time = time_range
            conflicts = []
            
            for meeting in self.meetings.values():
                if user_id in meeting.participants:
                    # Check for overlap
                    if (start_time < meeting.end_time and end_time > meeting.start_time):
                        conflicts.append({
                            "meeting_id": meeting.id,
                            "title": meeting.title,
                            "start_time": meeting.start_time.isoformat(),
                            "end_time": meeting.end_time.isoformat(),
                            "overlap_minutes": self._calculate_overlap_minutes(start_time, end_time, 
                                                                             meeting.start_time, meeting.end_time)
                        })
            
            return {
                "success": True,
                "user_id": user_id,
                "time_range": [start_time.isoformat(), end_time.isoformat()],
                "has_conflicts": len(conflicts) > 0,
                "conflicts": conflicts,
                "conflict_count": len(conflicts)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_overlap_minutes(self, start1: datetime, end1: datetime, 
                                  start2: datetime, end2: datetime) -> int:
        """Calculate overlap in minutes between two time ranges"""
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        if overlap_start < overlap_end:
            return int((overlap_end - overlap_start).total_seconds() / 60)
        return 0
    
    def analyze_meeting_patterns(self, user_id: str, period: str) -> Dict[str, Any]:
        """Analyze meeting patterns and behavior"""
        try:
            # Filter meetings for the user and period
            user_meetings = [m for m in self.meetings.values() if user_id in m.participants]
            
            if period == "week":
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)
            elif period == "month":
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
            else:  # "all"
                cutoff_date = datetime.min.replace(tzinfo=timezone.utc)
            
            period_meetings = [m for m in user_meetings if m.start_time >= cutoff_date]
            
            # Calculate patterns
            total_meetings = len(period_meetings)
            total_hours = sum((m.end_time - m.start_time).total_seconds() / 3600 
                            for m in period_meetings)
            
            # Meeting frequency by day of week
            day_frequency = defaultdict(int)
            hour_frequency = defaultdict(int)
            duration_distribution = defaultdict(int)
            meeting_type_frequency = defaultdict(int)
            
            for meeting in period_meetings:
                day_frequency[meeting.start_time.strftime("%A")] += 1
                hour_frequency[meeting.start_time.hour] += 1
                duration_minutes = int((meeting.end_time - meeting.start_time).total_seconds() / 60)
                duration_distribution[duration_minutes] += 1
                meeting_type_frequency[meeting.meeting_type] += 1
            
            # Calculate average effectiveness score
            effectiveness_scores = [m.effectiveness_score for m in period_meetings 
                                  if m.effectiveness_score is not None]
            avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
            
            # Productivity insights
            insights = self._generate_productivity_insights(period_meetings, user_id)
            
            return {
                "success": True,
                "user_id": user_id,
                "period": period,
                "analysis": {
                    "total_meetings": total_meetings,
                    "total_hours": round(total_hours, 2),
                    "average_meeting_duration": round(total_hours * 60 / total_meetings, 1) if total_meetings > 0 else 0,
                    "meetings_per_day": round(total_meetings / 7 if period == "week" else total_meetings / 30, 1),
                    "day_frequency": dict(day_frequency),
                    "hour_frequency": dict(hour_frequency),
                    "duration_distribution": dict(duration_distribution),
                    "meeting_type_frequency": dict(meeting_type_frequency),
                    "average_effectiveness_score": round(avg_effectiveness, 2),
                    "productivity_insights": insights
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_productivity_insights(self, meetings: List[Meeting], user_id: str) -> List[str]:
        """Generate AI-powered productivity insights"""
        insights = []
        
        if not meetings:
            return ["No meetings found for analysis."]
        
        # Analyze meeting load
        total_hours = sum((m.end_time - m.start_time).total_seconds() / 3600 for m in meetings)
        if total_hours > 20:  # More than 20 hours per week/month
            insights.append("High meeting load detected. Consider consolidating or declining non-essential meetings.")
        
        # Analyze meeting times
        early_meetings = sum(1 for m in meetings if m.start_time.hour < 9)
        late_meetings = sum(1 for m in meetings if m.start_time.hour >= 17)
        
        if early_meetings > len(meetings) * 0.3:
            insights.append("Many early morning meetings. Consider if these align with peak productivity hours.")
        
        if late_meetings > len(meetings) * 0.2:
            insights.append("Frequent late meetings detected. This may impact work-life balance.")
        
        # Analyze effectiveness scores
        effectiveness_scores = [m.effectiveness_score for m in meetings if m.effectiveness_score is not None]
        if effectiveness_scores:
            avg_score = sum(effectiveness_scores) / len(effectiveness_scores)
            if avg_score < 6.0:
                insights.append("Meeting effectiveness is below average. Consider improving agenda preparation and time management.")
            elif avg_score > 8.0:
                insights.append("Excellent meeting effectiveness! Keep up the good practices.")
        
        # Analyze meeting duration patterns
        long_meetings = sum(1 for m in meetings if (m.end_time - m.start_time).total_seconds() > 3600)
        if long_meetings > len(meetings) * 0.4:
            insights.append("Many long meetings detected. Consider breaking them into shorter, focused sessions.")
        
        return insights
    
    def generate_agenda_suggestions(self, meeting_topic: str, participants: List[str]) -> Dict[str, Any]:
        """Generate smart agenda suggestions based on topic and participants"""
        try:
            # Analyze past meetings with similar participants
            participant_meetings = [m for m in self.meetings.values() 
                                  if any(p in m.participants for p in participants)]
            
            # Generate agenda based on meeting topic and patterns
            agenda_items = self._generate_agenda_items(meeting_topic, participants, participant_meetings)
            
            # Estimate time allocation
            time_allocation = self._estimate_time_allocation(agenda_items)
            
            # Generate meeting preparation suggestions
            preparation_tips = self._generate_preparation_tips(meeting_topic, participants)
            
            return {
                "success": True,
                "meeting_topic": meeting_topic,
                "participants": participants,
                "suggested_agenda": {
                    "items": agenda_items,
                    "estimated_duration": sum(time_allocation.values()),
                    "time_allocation": time_allocation
                },
                "preparation_tips": preparation_tips,
                "success_factors": [
                    "Start and end on time",
                    "Keep discussions focused on agenda items",
                    "Assign clear action items with owners",
                    "Follow up within 24 hours"
                ]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_agenda_items(self, topic: str, participants: List[str], 
                              past_meetings: List[Meeting]) -> List[Dict[str, str]]:
        """Generate agenda items based on topic and context"""
        topic_lower = topic.lower()
        
        # Base agenda structure
        agenda_items = [
            {"item": "Welcome and introductions", "type": "opening", "description": "Brief introductions if needed"},
            {"item": "Meeting objectives", "type": "overview", "description": "Review goals and expected outcomes"}
        ]
        
        # Topic-specific agenda items
        if "planning" in topic_lower or "strategy" in topic_lower:
            agenda_items.extend([
                {"item": "Current status review", "type": "review", "description": "Assess current progress and challenges"},
                {"item": "Goal setting and priorities", "type": "planning", "description": "Define objectives and key priorities"},
                {"item": "Resource allocation", "type": "planning", "description": "Discuss budget, timeline, and team assignments"},
                {"item": "Risk assessment", "type": "analysis", "description": "Identify potential risks and mitigation strategies"}
            ])
        
        elif "review" in topic_lower or "retrospective" in topic_lower:
            agenda_items.extend([
                {"item": "Achievements and wins", "type": "review", "description": "Celebrate successes and positive outcomes"},
                {"item": "Challenges and lessons learned", "type": "review", "description": "Discuss obstacles and key learnings"},
                {"item": "Process improvements", "type": "improvement", "description": "Identify areas for optimization"},
                {"item": "Action items for next period", "type": "planning", "description": "Define next steps and responsibilities"}
            ])
        
        elif "brainstorm" in topic_lower or "ideation" in topic_lower:
            agenda_items.extend([
                {"item": "Problem definition", "type": "framing", "description": "Clearly define the challenge or opportunity"},
                {"item": "Idea generation", "type": "brainstorming", "description": "Open brainstorming session - all ideas welcome"},
                {"item": "Idea evaluation", "type": "analysis", "description": "Assess and prioritize generated ideas"},
                {"item": "Next steps selection", "type": "decision", "description": "Choose ideas to pursue and assign owners"}
            ])
        
        elif "standup" in topic_lower or "sync" in topic_lower:
            agenda_items.extend([
                {"item": "Round-robin updates", "type": "update", "description": "Each participant shares progress and blockers"},
                {"item": "Blocker resolution", "type": "problem-solving", "description": "Address any impediments or challenges"},
                {"item": "Coordination needs", "type": "coordination", "description": "Identify collaboration opportunities"}
            ])
        
        else:  # Generic meeting
            agenda_items.extend([
                {"item": "Main discussion topics", "type": "discussion", "description": "Core agenda items for the meeting"},
                {"item": "Decision points", "type": "decision", "description": "Items requiring group decisions"},
                {"item": "Information sharing", "type": "information", "description": "Updates and announcements"}
            ])
        
        # Always end with action items and next steps
        agenda_items.extend([
            {"item": "Action items and owners", "type": "action", "description": "Assign specific tasks with clear ownership"},
            {"item": "Next meeting and follow-up", "type": "closing", "description": "Schedule follow-up and confirm next steps"}
        ])
        
        return agenda_items
    
    def _estimate_time_allocation(self, agenda_items: List[Dict[str, str]]) -> Dict[str, int]:
        """Estimate time allocation for agenda items"""
        time_allocation = {}
        
        # Time estimates by item type (in minutes)
        type_durations = {
            "opening": 5,
            "overview": 5,
            "review": 10,
            "planning": 15,
            "analysis": 12,
            "improvement": 10,
            "framing": 8,
            "brainstorming": 20,
            "decision": 10,
            "update": 15,
            "problem-solving": 12,
            "coordination": 8,
            "discussion": 15,
            "information": 8,
            "action": 10,
            "closing": 5
        }
        
        for item in agenda_items:
            item_type = item.get("type", "discussion")
            time_allocation[item["item"]] = type_durations.get(item_type, 10)
        
        return time_allocation
    
    def _generate_preparation_tips(self, topic: str, participants: List[str]) -> List[str]:
        """Generate meeting preparation suggestions"""
        tips = [
            "Send agenda 24-48 hours in advance",
            "Include any pre-reading materials or documents",
            "Test technology and meeting links beforehand",
            "Prepare key questions to guide discussion"
        ]
        
        if len(participants) > 5:
            tips.append("Consider assigning a facilitator for large group dynamics")
            tips.append("Use structured discussion formats (e.g., round-robin)")
        
        topic_lower = topic.lower()
        if "decision" in topic_lower:
            tips.append("Prepare decision criteria and evaluation framework")
            tips.append("Gather relevant data and analysis beforehand")
        
        if "brainstorm" in topic_lower:
            tips.append("Set ground rules for creative thinking")
            tips.append("Prepare stimulus materials or examples")
        
        return tips
    
    def calculate_workload_balance(self, team_members: List[str]) -> Dict[str, Any]:
        """Calculate meeting workload distribution across team members"""
        try:
            # Analyze meeting load for each team member
            workload_data = {}
            
            for member in team_members:
                member_meetings = [m for m in self.meetings.values() if member in m.participants]
                
                # Calculate metrics for the last 30 days
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
                recent_meetings = [m for m in member_meetings if m.start_time >= cutoff_date]
                
                total_hours = sum((m.end_time - m.start_time).total_seconds() / 3600 
                                for m in recent_meetings)
                
                # Calculate daily averages
                daily_avg_meetings = len(recent_meetings) / 30
                daily_avg_hours = total_hours / 30
                
                # Meeting types distribution
                meeting_types = defaultdict(int)
                for meeting in recent_meetings:
                    meeting_types[meeting.meeting_type] += 1
                
                workload_data[member] = {
                    "total_meetings_30d": len(recent_meetings),
                    "total_hours_30d": round(total_hours, 2),
                    "daily_avg_meetings": round(daily_avg_meetings, 2),
                    "daily_avg_hours": round(daily_avg_hours, 2),
                    "meeting_types": dict(meeting_types),
                    "workload_score": self._calculate_workload_score(daily_avg_hours, daily_avg_meetings)
                }
            
            # Calculate team statistics
            team_stats = self._calculate_team_workload_stats(workload_data)
            
            # Generate balance recommendations
            recommendations = self._generate_workload_recommendations(workload_data, team_stats)
            
            return {
                "success": True,
                "team_members": team_members,
                "workload_analysis": workload_data,
                "team_statistics": team_stats,
                "balance_recommendations": recommendations,
                "analysis_period": "Last 30 days"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_workload_score(self, daily_hours: float, daily_meetings: float) -> float:
        """Calculate workload score (0-100, higher = more overloaded)"""
        # Base score from meeting hours (target: 2-3 hours/day)
        hours_score = min(daily_hours / 4.0 * 100, 100)  # 4+ hours = 100% score
        
        # Additional score from meeting frequency (target: 3-4 meetings/day)
        meetings_score = min(daily_meetings / 6.0 * 100, 100)  # 6+ meetings = 100% score
        
        # Weighted combination
        return round((hours_score * 0.7 + meetings_score * 0.3), 1)
    
    def _calculate_team_workload_stats(self, workload_data: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate team-wide workload statistics"""
        if not workload_data:
            return {}
        
        hours_list = [data["daily_avg_hours"] for data in workload_data.values()]
        meetings_list = [data["daily_avg_meetings"] for data in workload_data.values()]
        scores_list = [data["workload_score"] for data in workload_data.values()]
        
        return {
            "avg_daily_hours": round(sum(hours_list) / len(hours_list), 2),
            "avg_daily_meetings": round(sum(meetings_list) / len(meetings_list), 2),
            "avg_workload_score": round(sum(scores_list) / len(scores_list), 1),
            "max_workload_member": max(workload_data.keys(), key=lambda k: workload_data[k]["workload_score"]),
            "min_workload_member": min(workload_data.keys(), key=lambda k: workload_data[k]["workload_score"]),
            "workload_variance": round(self._calculate_variance(scores_list), 1)
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def _generate_workload_recommendations(self, workload_data: Dict[str, Dict], 
                                         team_stats: Dict[str, Any]) -> List[str]:
        """Generate workload balancing recommendations"""
        recommendations = []
        
        if not workload_data or not team_stats:
            return recommendations
        
        # Check for overloaded members
        overloaded = [member for member, data in workload_data.items() 
                     if data["workload_score"] > 70]
        
        underloaded = [member for member, data in workload_data.items() 
                      if data["workload_score"] < 30]
        
        if overloaded:
            recommendations.append(f"High workload detected for: {', '.join(overloaded)}. Consider redistributing meetings.")
        
        if underloaded and overloaded:
            recommendations.append(f"Consider shifting some meetings from {', '.join(overloaded)} to {', '.join(underloaded)}.")
        
        # Check variance
        if team_stats.get("workload_variance", 0) > 400:  # High variance
            recommendations.append("High workload variance across team. Work on more even distribution.")
        
        # Check average team load
        avg_score = team_stats.get("avg_workload_score", 0)
        if avg_score > 60:
            recommendations.append("Team overall meeting load is high. Consider meeting-free time blocks.")
        elif avg_score < 20:
            recommendations.append("Team meeting load is low. Consider if more collaboration is needed.")
        
        # Meeting type recommendations
        all_meeting_types = defaultdict(int)
        for data in workload_data.values():
            for meeting_type, count in data["meeting_types"].items():
                all_meeting_types[meeting_type] += count
        
        if all_meeting_types.get("standup", 0) > len(workload_data) * 10:  # More than 10 standups per person
            recommendations.append("High number of standup meetings. Consider consolidating or reducing frequency.")
        
        return recommendations
    
    def score_meeting_effectiveness(self, meeting_id: str) -> Dict[str, Any]:
        """Score meeting effectiveness and provide improvement suggestions"""
        try:
            if meeting_id not in self.meetings:
                return {"success": False, "error": "Meeting not found"}
            
            meeting = self.meetings[meeting_id]
            
            # Calculate effectiveness score based on multiple factors
            score_components = self._calculate_effectiveness_components(meeting)
            
            # Overall score (weighted average)
            weights = {
                "duration_efficiency": 0.25,
                "participant_engagement": 0.20,
                "agenda_adherence": 0.20,
                "outcome_clarity": 0.20,
                "time_management": 0.15
            }
            
            overall_score = sum(score_components[component] * weight 
                              for component, weight in weights.items())
            
            # Generate improvement suggestions
            suggestions = self._generate_improvement_suggestions(score_components, meeting)
            
            # Update meeting effectiveness score
            self.meetings[meeting_id].effectiveness_score = overall_score
            
            return {
                "success": True,
                "meeting_id": meeting_id,
                "meeting_title": meeting.title,
                "overall_score": round(overall_score, 2),
                "score_components": {k: round(v, 2) for k, v in score_components.items()},
                "effectiveness_rating": self._get_effectiveness_rating(overall_score),
                "improvement_suggestions": suggestions,
                "benchmarks": {
                    "excellent": ">= 8.0",
                    "good": "6.0 - 7.9",
                    "needs_improvement": "< 6.0"
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_effectiveness_components(self, meeting: Meeting) -> Dict[str, float]:
        """Calculate individual effectiveness score components"""
        duration_minutes = (meeting.end_time - meeting.start_time).total_seconds() / 60
        
        # Duration efficiency (optimal: 30-60 minutes)
        if 30 <= duration_minutes <= 60:
            duration_efficiency = 9.0
        elif 15 <= duration_minutes < 30 or 60 < duration_minutes <= 90:
            duration_efficiency = 7.0
        elif duration_minutes < 15 or duration_minutes > 120:
            duration_efficiency = 4.0
        else:
            duration_efficiency = 6.0
        
        # Participant engagement (based on group size)
        participant_count = len(meeting.participants)
        if 2 <= participant_count <= 6:
            participant_engagement = 8.5
        elif participant_count <= 10:
            participant_engagement = 7.0
        else:
            participant_engagement = 5.5  # Large meetings often have lower engagement
        
        # Agenda adherence (simulated based on meeting type)
        agenda_scores = {
            "standup": 8.5,  # Usually well-structured
            "1on1": 8.0,    # Personal, focused
            "planning": 7.5, # Can go off-track
            "review": 7.0,   # Sometimes lengthy
            "brainstorm": 6.5, # Creative, less structured
            "all-hands": 6.0  # Often informational
        }
        agenda_adherence = agenda_scores.get(meeting.meeting_type, 7.0)
        
        # Outcome clarity (simulated based on meeting type and duration)
        if meeting.meeting_type in ["standup", "1on1", "review"]:
            outcome_clarity = 8.0
        elif duration_minutes > 90:
            outcome_clarity = 5.5  # Long meetings often lack clear outcomes
        else:
            outcome_clarity = 7.0
        
        # Time management (based on start time and duration)
        start_hour = meeting.start_time.hour
        if 9 <= start_hour <= 16:  # Good meeting hours
            time_management = 8.0
        elif 8 <= start_hour <= 17:
            time_management = 7.0
        else:
            time_management = 5.0  # Early morning or late meetings
        
        # Adjust for very long meetings
        if duration_minutes > 120:
            time_management -= 2.0
        
        return {
            "duration_efficiency": max(1.0, duration_efficiency),
            "participant_engagement": max(1.0, participant_engagement),
            "agenda_adherence": max(1.0, agenda_adherence),
            "outcome_clarity": max(1.0, outcome_clarity),
            "time_management": max(1.0, time_management)
        }
    
    def _get_effectiveness_rating(self, score: float) -> str:
        """Convert numerical score to rating"""
        if score >= 8.0:
            return "Excellent"
        elif score >= 6.0:
            return "Good"
        elif score >= 4.0:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _generate_improvement_suggestions(self, score_components: Dict[str, float], 
                                        meeting: Meeting) -> List[str]:
        """Generate specific improvement suggestions based on scores"""
        suggestions = []
        duration_minutes = (meeting.end_time - meeting.start_time).total_seconds() / 60
        
        # Duration efficiency suggestions
        if score_components["duration_efficiency"] < 6.0:
            if duration_minutes > 90:
                suggestions.append("Consider breaking long meetings into shorter, focused sessions")
            elif duration_minutes < 15:
                suggestions.append("Very short meetings may benefit from asynchronous communication instead")
        
        # Participant engagement suggestions
        if score_components["participant_engagement"] < 7.0:
            if len(meeting.participants) > 8:
                suggestions.append("Large meetings can reduce engagement. Consider smaller working groups")
            suggestions.append("Use interactive formats like round-robin or breakout sessions")
        
        # Agenda adherence suggestions
        if score_components["agenda_adherence"] < 7.0:
            suggestions.append("Prepare and share a detailed agenda 24-48 hours in advance")
            suggestions.append("Assign a facilitator to keep discussions on track")
        
        # Outcome clarity suggestions
        if score_components["outcome_clarity"] < 7.0:
            suggestions.append("End meetings with clear action items and owners")
            suggestions.append("Send follow-up summary within 24 hours")
        
        # Time management suggestions
        if score_components["time_management"] < 7.0:
            suggestions.append("Schedule meetings during peak productivity hours (9 AM - 4 PM)")
            if duration_minutes > 60:
                suggestions.append("Include breaks for meetings longer than 60 minutes")
        
        # General suggestions for low overall scores
        overall_score = sum(score_components.values()) / len(score_components)
        if overall_score < 6.0:
            suggestions.append("Consider if this meeting could be replaced with asynchronous communication")
            suggestions.append("Implement a meeting effectiveness feedback system")
        
        return suggestions
    
    def optimize_meeting_schedule(self, user_id: str) -> Dict[str, Any]:
        """Provide schedule optimization recommendations"""
        try:
            # Get user's meetings and preferences
            user_meetings = [m for m in self.meetings.values() if user_id in m.participants]
            user_prefs = self.user_preferences.get(user_id)
            
            if not user_prefs:
                return {"success": False, "error": "User preferences not found"}
            
            # Analyze current schedule
            schedule_analysis = self._analyze_current_schedule(user_meetings, user_prefs)
            
            # Generate optimization recommendations
            optimizations = self._generate_schedule_optimizations(schedule_analysis, user_prefs)
            
            # Calculate potential time savings
            time_savings = self._calculate_potential_savings(optimizations)
            
            return {
                "success": True,
                "user_id": user_id,
                "current_schedule_analysis": schedule_analysis,
                "optimization_recommendations": optimizations,
                "potential_time_savings": time_savings,
                "implementation_priority": self._prioritize_optimizations(optimizations)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _analyze_current_schedule(self, meetings: List[Meeting], 
                                 prefs: UserPreferences) -> Dict[str, Any]:
        """Analyze current meeting schedule patterns"""
        if not meetings:
            return {"total_meetings": 0, "issues": []}
        
        # Recent meetings (last 30 days)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
        recent_meetings = [m for m in meetings if m.start_time >= cutoff_date]
        
        issues = []
        
        # Check meeting density
        daily_meetings = defaultdict(int)
        for meeting in recent_meetings:
            date_key = meeting.start_time.date()
            daily_meetings[date_key] += 1
        
        heavy_days = sum(1 for count in daily_meetings.values() if count > prefs.max_daily_meetings)
        if heavy_days > 0:
            issues.append(f"Heavy meeting days detected: {heavy_days} days exceed preferred limit")
        
        # Check meeting times vs preferences
        off_hours_meetings = sum(1 for m in recent_meetings 
                               if not (prefs.preferred_meeting_hours[0] <= m.start_time.hour <= prefs.preferred_meeting_hours[1]))
        
        if off_hours_meetings > len(recent_meetings) * 0.2:
            issues.append(f"Many meetings outside preferred hours: {off_hours_meetings} meetings")
        
        # Check for back-to-back meetings
        back_to_back = self._count_back_to_back_meetings(recent_meetings, prefs.break_time_between_meetings)
        if back_to_back > len(recent_meetings) * 0.3:
            issues.append(f"Frequent back-to-back meetings: {back_to_back} instances")
        
        # Check meeting duration vs preferences
        long_meetings = sum(1 for m in recent_meetings 
                          if (m.end_time - m.start_time).total_seconds() / 60 > prefs.preferred_meeting_duration * 1.5)
        
        if long_meetings > len(recent_meetings) * 0.3:
            issues.append(f"Many meetings exceed preferred duration: {long_meetings} meetings")
        
        return {
            "total_meetings": len(recent_meetings),
            "avg_daily_meetings": round(len(recent_meetings) / 30, 1),
            "heavy_meeting_days": heavy_days,
            "off_hours_meetings": off_hours_meetings,
            "back_to_back_meetings": back_to_back,
            "long_meetings": long_meetings,
            "issues": issues
        }
    
    def _count_back_to_back_meetings(self, meetings: List[Meeting], min_break: int) -> int:
        """Count back-to-back meetings with insufficient break time"""
        if len(meetings) < 2:
            return 0
        
        # Sort meetings by start time
        sorted_meetings = sorted(meetings, key=lambda m: m.start_time)
        
        back_to_back_count = 0
        for i in range(len(sorted_meetings) - 1):
            current_end = sorted_meetings[i].end_time
            next_start = sorted_meetings[i + 1].start_time
            
            break_minutes = (next_start - current_end).total_seconds() / 60
            if 0 <= break_minutes < min_break:
                back_to_back_count += 1
        
        return back_to_back_count
    
    def _generate_schedule_optimizations(self, analysis: Dict[str, Any], 
                                       prefs: UserPreferences) -> List[Dict[str, Any]]:
        """Generate specific schedule optimization recommendations"""
        optimizations = []
        
        # Address heavy meeting days
        if analysis.get("heavy_meeting_days", 0) > 0:
            optimizations.append({
                "type": "meeting_distribution",
                "priority": "high",
                "description": "Redistribute meetings to avoid overloaded days",
                "action": "Move some meetings from heavy days to lighter days",
                "estimated_benefit": "Reduce daily meeting fatigue and improve focus"
            })
        
        # Address off-hours meetings
        if analysis.get("off_hours_meetings", 0) > 0:
            optimizations.append({
                "type": "time_alignment",
                "priority": "medium",
                "description": "Align meetings with preferred working hours",
                "action": f"Reschedule meetings to {prefs.preferred_meeting_hours[0]}:00-{prefs.preferred_meeting_hours[1]}:00",
                "estimated_benefit": "Improve meeting engagement and work-life balance"
            })
        
        # Address back-to-back meetings
        if analysis.get("back_to_back_meetings", 0) > 0:
            optimizations.append({
                "type": "buffer_time",
                "priority": "high",
                "description": "Add buffer time between meetings",
                "action": f"Ensure {prefs.break_time_between_meetings} minutes between consecutive meetings",
                "estimated_benefit": "Reduce context switching and allow for preparation time"
            })
        
        # Address long meetings
        if analysis.get("long_meetings", 0) > 0:
            optimizations.append({
                "type": "duration_optimization",
                "priority": "medium",
                "description": "Optimize meeting durations",
                "action": f"Target {prefs.preferred_meeting_duration} minutes per meeting",
                "estimated_benefit": "Improve focus and reduce meeting fatigue"
            })
        
        # General optimizations
        if analysis.get("avg_daily_meetings", 0) > 4:
            optimizations.append({
                "type": "meeting_reduction",
                "priority": "medium",
                "description": "Reduce overall meeting load",
                "action": "Evaluate necessity of recurring meetings and decline optional ones",
                "estimated_benefit": "Increase focused work time and productivity"
            })
        
        # Time blocking suggestion
        optimizations.append({
            "type": "time_blocking",
            "priority": "low",
            "description": "Implement focused work blocks",
            "action": "Block 2-3 hour periods for deep work without meetings",
            "estimated_benefit": "Improve productivity and reduce fragmentation"
        })
        
        return optimizations
    
    def _calculate_potential_savings(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate potential time and productivity savings"""
        # Estimate time savings based on optimization types
        savings_estimates = {
            "meeting_distribution": {"time_saved_hours_week": 2, "productivity_gain_percent": 15},
            "time_alignment": {"time_saved_hours_week": 1, "productivity_gain_percent": 10},
            "buffer_time": {"time_saved_hours_week": 3, "productivity_gain_percent": 20},
            "duration_optimization": {"time_saved_hours_week": 4, "productivity_gain_percent": 25},
            "meeting_reduction": {"time_saved_hours_week": 5, "productivity_gain_percent": 30},
            "time_blocking": {"time_saved_hours_week": 6, "productivity_gain_percent": 35}
        }
        
        total_time_saved = 0
        total_productivity_gain = 0
        
        for opt in optimizations:
            opt_type = opt["type"]
            if opt_type in savings_estimates:
                total_time_saved += savings_estimates[opt_type]["time_saved_hours_week"]
                total_productivity_gain += savings_estimates[opt_type]["productivity_gain_percent"]
        
        # Cap the gains (diminishing returns)
        total_time_saved = min(total_time_saved, 15)  # Max 15 hours per week
        total_productivity_gain = min(total_productivity_gain, 50)  # Max 50% gain
        
        return {
            "time_saved_hours_per_week": total_time_saved,
            "productivity_gain_percent": total_productivity_gain,
            "focus_time_gained_hours_week": round(total_time_saved * 0.8, 1),
            "estimated_monthly_benefit": f"{total_time_saved * 4} hours of reclaimed time"
        }
    
    def _prioritize_optimizations(self, optimizations: List[Dict[str, Any]]) -> List[str]:
        """Prioritize optimizations by impact and ease of implementation"""
        high_priority = [opt["description"] for opt in optimizations if opt["priority"] == "high"]
        medium_priority = [opt["description"] for opt in optimizations if opt["priority"] == "medium"]
        low_priority = [opt["description"] for opt in optimizations if opt["priority"] == "low"]
        
        prioritized = []
        if high_priority:
            prioritized.append(f"High Priority: {', '.join(high_priority)}")
        if medium_priority:
            prioritized.append(f"Medium Priority: {', '.join(medium_priority)}")
        if low_priority:
            prioritized.append(f"Low Priority: {', '.join(low_priority)}")
        
        return prioritized

# Initialize the assistant
assistant = SmartMeetingAssistant()

# Create the MCP server
server = Server("smart-meeting-assistant")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="create_meeting",
            description="Schedule a new meeting with AI-powered conflict detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Meeting title"},
                    "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant email addresses"},
                    "duration": {"type": "integer", "description": "Meeting duration in minutes"},
                    "preferences": {"type": "object", "description": "Meeting preferences (preferred_time, agenda, etc.)"}
                },
                "required": ["title", "participants", "duration"]
            },
        ),
        types.Tool(
            name="find_optimal_slots",
            description="Find AI-powered optimal time slot recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant email addresses"},
                    "duration": {"type": "integer", "description": "Meeting duration in minutes"},
                    "date_range": {"type": "object", "description": "Date range preferences (days_ahead, start_date, end_date)"}
                },
                "required": ["participants", "duration", "date_range"]
            },
        ),
        types.Tool(
            name="detect_scheduling_conflicts",
            description="Detect scheduling conflicts for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User email address"},
                    "time_range": {"type": "array", "items": {"type": "string"}, "description": "Time range as [start_time, end_time] in ISO format"}
                },
                "required": ["user_id", "time_range"]
            },
        ),
        types.Tool(
            name="analyze_meeting_patterns",
            description="Analyze meeting patterns and behavior for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User email address"},
                    "period": {"type": "string", "enum": ["week", "month", "all"], "description": "Analysis period"}
                },
                "required": ["user_id", "period"]
            },
        ),
        types.Tool(
            name="generate_agenda_suggestions",
            description="Generate smart agenda suggestions for a meeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "meeting_topic": {"type": "string", "description": "Main topic or purpose of the meeting"},
                    "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant email addresses"}
                },
                "required": ["meeting_topic", "participants"]
            },
        ),
        types.Tool(
            name="calculate_workload_balance",
            description="Calculate meeting workload distribution across team members",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_members": {"type": "array", "items": {"type": "string"}, "description": "List of team member email addresses"}
                },
                "required": ["team_members"]
            },
        ),
        types.Tool(
            name="score_meeting_effectiveness",
            description="Score meeting effectiveness and provide improvement suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "meeting_id": {"type": "string", "description": "Meeting ID to analyze"}
                },
                "required": ["meeting_id"]
            },
        ),
        types.Tool(
            name="optimize_meeting_schedule",
            description="Provide schedule optimization recommendations for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User email address"}
                },
                "required": ["user_id"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """
    Handle tool calls for the Smart Meeting Assistant.
    """
    try:
        if name == "create_meeting":
            result = assistant.create_meeting(
                arguments["title"],
                arguments["participants"],
                arguments["duration"],
                arguments.get("preferences", {})
            )
        elif name == "find_optimal_slots":
            result = assistant.find_optimal_slots(
                arguments["participants"],
                arguments["duration"],
                arguments["date_range"]
            )
        elif name == "detect_scheduling_conflicts":
            time_range = tuple(datetime.fromisoformat(t) for t in arguments["time_range"])
            result = assistant.detect_scheduling_conflicts(
                arguments["user_id"],
                time_range
            )
        elif name == "analyze_meeting_patterns":
            result = assistant.analyze_meeting_patterns(
                arguments["user_id"],
                arguments["period"]
            )
        elif name == "generate_agenda_suggestions":
            result = assistant.generate_agenda_suggestions(
                arguments["meeting_topic"],
                arguments["participants"]
            )
        elif name == "calculate_workload_balance":
            result = assistant.calculate_workload_balance(
                arguments["team_members"]
            )
        elif name == "score_meeting_effectiveness":
            result = assistant.score_meeting_effectiveness(
                arguments["meeting_id"]
            )
        elif name == "optimize_meeting_schedule":
            result = assistant.optimize_meeting_schedule(
                arguments["user_id"]
            )
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    
    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="smart-meeting-assistant",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())