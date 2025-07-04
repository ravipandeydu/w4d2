# Smart Meeting Assistant MCP Server

An AI-powered Model Context Protocol (MCP) server for intelligent meeting scheduling and management. This server provides advanced features like conflict detection, optimal time slot recommendations, meeting pattern analysis, and productivity insights.

## Features

### 🤖 AI-Powered Scheduling
- **Intelligent Conflict Detection**: Automatically identifies scheduling conflicts across participants
- **Optimal Time Recommendations**: AI-driven suggestions for the best meeting times based on participant availability and preferences
- **Smart Agenda Generation**: Context-aware agenda creation based on meeting topics and participant history

### 📊 Meeting Analytics
- **Pattern Analysis**: Comprehensive analysis of meeting behaviors and trends
- **Effectiveness Scoring**: Automated scoring of meeting productivity with improvement suggestions
- **Workload Balancing**: Team meeting load distribution analysis and optimization

### ⚡ Schedule Optimization
- **Personal Schedule Optimization**: Tailored recommendations for individual schedule improvements
- **Time Block Management**: Intelligent suggestions for focused work periods
- **Meeting Duration Optimization**: AI-powered duration recommendations

## MCP Tools

The server implements 8 core MCP tools:

1. **`create_meeting`** - Schedule new meetings with AI conflict detection
2. **`find_optimal_slots`** - Get AI-powered time slot recommendations
3. **`detect_scheduling_conflicts`** - Identify scheduling conflicts for users
4. **`analyze_meeting_patterns`** - Analyze meeting behaviors and trends
5. **`generate_agenda_suggestions`** - Create smart meeting agendas
6. **`calculate_workload_balance`** - Analyze team meeting load distribution
7. **`score_meeting_effectiveness`** - Score and improve meeting productivity
8. **`optimize_meeting_schedule`** - Get personalized schedule optimization recommendations

## Sample Data

The server comes pre-loaded with:
- **65+ sample meetings** across different time zones and meeting types
- **8 users** with diverse preferences and time zones:
  - Alice (New York) - Team Lead
  - Bob (Los Angeles) - Developer
  - Charlie (London) - Designer
  - Diana (Tokyo) - Product Manager
  - Eve (Sydney) - Marketing
  - Frank (Chicago) - Operations
  - Grace (Berlin) - Engineer
  - Henry (Singapore) - QA Lead

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server**:
   ```bash
   python src/server.py
   ```

## Usage Examples

### Creating a Meeting
```json
{
  "tool": "create_meeting",
  "arguments": {
    "title": "Project Kickoff",
    "participants": ["alice@company.com", "bob@company.com", "charlie@company.com"],
    "duration": 60,
    "preferences": {
      "preferred_time": "2024-02-01T14:00:00Z",
      "agenda": "Discuss project goals and timeline"
    }
  }
}
```

### Finding Optimal Time Slots
```json
{
  "tool": "find_optimal_slots",
  "arguments": {
    "participants": ["alice@company.com", "diana@company.com", "frank@company.com"],
    "duration": 90,
    "date_range": {
      "days_ahead": 7
    }
  }
}
```

### Analyzing Meeting Patterns
```json
{
  "tool": "analyze_meeting_patterns",
  "arguments": {
    "user_id": "alice@company.com",
    "period": "month"
  }
}
```

### Generating Smart Agendas
```json
{
  "tool": "generate_agenda_suggestions",
  "arguments": {
    "meeting_topic": "Sprint Planning",
    "participants": ["alice@company.com", "bob@company.com", "grace@company.com"]
  }
}
```

## AI Features in Detail

### Intelligent Scheduling Algorithm
The AI considers multiple factors when recommending meeting times:
- **Participant availability** across different time zones
- **Preferred working hours** for each participant
- **Meeting load balancing** to avoid overloading individuals
- **Productivity patterns** (e.g., avoiding lunch hours, preferring mid-week)
- **Break time requirements** between consecutive meetings

### Meeting Effectiveness Scoring
Meetings are scored based on:
- **Duration efficiency** (optimal length for meeting type)
- **Participant engagement** (group size optimization)
- **Agenda adherence** (structured vs. ad-hoc meetings)
- **Outcome clarity** (clear action items and follow-ups)
- **Time management** (scheduled during productive hours)

### Workload Analysis
The system analyzes:
- **Meeting frequency** and duration per person
- **Meeting type distribution** (standups, planning, reviews, etc.)
- **Time zone impact** on meeting participation
- **Work-life balance** indicators
- **Team collaboration patterns**

## Architecture

### Core Components
- **SmartMeetingAssistant**: Main business logic class
- **Meeting**: Data model for meeting information
- **UserPreferences**: User-specific scheduling preferences
- **MCP Server**: Protocol implementation for tool exposure

### Data Models
```python
@dataclass
class Meeting:
    id: str
    title: str
    participants: List[str]
    start_time: datetime
    end_time: datetime
    timezone_str: str
    organizer: str
    # ... additional fields

@dataclass
class UserPreferences:
    user_id: str
    preferred_meeting_hours: Tuple[int, int]
    timezone_str: str
    max_daily_meetings: int
    # ... additional preferences
```

## Configuration

The server can be customized by modifying:
- **User preferences** in the `_initialize_sample_data()` method
- **Scoring algorithms** in the effectiveness calculation methods
- **Optimization parameters** in the scheduling algorithms

## Performance Considerations

- **In-memory storage**: Current implementation uses in-memory data structures
- **Scalability**: Designed for teams of 10-50 people
- **Response time**: Most operations complete in <100ms
- **Memory usage**: Approximately 10-20MB for 1000+ meetings

## Future Enhancements

- **Database integration** for persistent storage
- **Calendar system integration** (Google Calendar, Outlook)
- **Machine learning models** for improved predictions
- **Real-time notifications** for schedule changes
- **Mobile app integration** via MCP protocol
- **Advanced analytics dashboard**

## Contributing

To extend the server:
1. Add new tools by implementing handler functions
2. Extend the `SmartMeetingAssistant` class with new methods
3. Update the MCP tool definitions in `handle_list_tools()`
4. Add comprehensive error handling and validation

## License

This project is provided as an educational example for MCP server development.

## Support

For questions or issues:
- Review the code documentation
- Check the sample data format in `data/sample_content.json`
- Examine the tool schemas in the server implementation

---

**Built with the Model Context Protocol (MCP) for seamless AI integration**