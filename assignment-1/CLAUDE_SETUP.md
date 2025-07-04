# Claude Desktop MCP Server Setup - Troubleshooting Guide

This guide helps you resolve "MCP server failed" errors when connecting the Document Analyzer to Claude Desktop.

## 🚨 Common Claude Desktop Issues & Solutions

### Issue 1: Incorrect Configuration File Location

**Problem**: Claude can't find your configuration file.

**Solution**: Ensure you're editing the correct config file:

#### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Linux
```
~/.config/Claude/claude_desktop_config.json
```

### Issue 2: Incorrect JSON Configuration

**Problem**: Malformed JSON in configuration file.

**Correct Configuration**:
```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\server.py"],
      "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
    }
  }
}
```

**Important Notes**:
- Use **double backslashes** (`\\`) in Windows paths
- Use **absolute paths**, not relative paths
- Ensure proper JSON syntax (commas, quotes, brackets)

### Issue 3: Python Path Issues

**Problem**: Claude can't find Python or the script.

**Solutions**:

#### Option A: Use Full Python Path
```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "C:\\Python311\\python.exe",
      "args": ["C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\server.py"],
      "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
    }
  }
}
```

#### Option B: Use Virtual Environment Python
```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\.venv\\Scripts\\python.exe",
      "args": ["server.py"],
      "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
    }
  }
}
```

### Issue 4: Missing Dependencies

**Problem**: MCP package not installed.

**Solution**: Install in the correct environment

#### If using system Python:
```bash
pip install mcp aiofiles
```

#### If using virtual environment:
```bash
# Navigate to project directory
cd C:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Issue 5: Server Script Issues

**Problem**: Server script has errors or doesn't start properly.

**Diagnostic Steps**:

#### Step 1: Test Server Manually
```bash
# Navigate to project directory
cd C:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1

# Test with system Python
python server.py

# Or test with virtual environment
.venv\Scripts\activate
python server.py
```

#### Step 2: Check for Errors
If you see errors, common fixes:

**Import Error**:
```bash
pip install mcp aiofiles
```

**Path Error**:
- Ensure you're in the correct directory
- Check file permissions

#### Step 3: Test Core Functionality
```bash
# Test without MCP dependency
python standalone_test.py
```

## 🔧 Step-by-Step Setup Process

### Step 1: Verify Project Setup

1. **Check file structure**:
   ```
   assignment-1/
   ├── server.py
   ├── requirements.txt
   ├── .venv/
   └── other files...
   ```

2. **Verify server.py exists and is executable**:
   ```bash
   python server.py
   ```

### Step 2: Install Dependencies Properly

1. **Create/activate virtual environment**:
   ```bash
   cd C:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import mcp; print('MCP installed successfully')"
   ```

### Step 3: Create Correct Claude Configuration

1. **Find Claude config file**:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Create the file if it doesn't exist

2. **Add configuration** (choose one option):

   **Option A: Using Virtual Environment (Recommended)**:
   ```json
   {
     "mcpServers": {
       "document-analyzer": {
         "command": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\.venv\\Scripts\\python.exe",
         "args": ["server.py"],
         "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
       }
     }
   }
   ```

   **Option B: Using System Python**:
   ```json
   {
     "mcpServers": {
       "document-analyzer": {
         "command": "python",
         "args": ["C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\server.py"],
         "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
       }
     }
   }
   ```

### Step 4: Restart Claude Desktop

1. **Completely close Claude Desktop**
2. **Restart the application**
3. **Check for the server in Claude's interface**

## 🔍 Advanced Troubleshooting

### Enable Debug Logging

Modify `server.py` to add logging:

```python
# Add at the top of server.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
```

### Check Claude Desktop Logs

#### Windows
```
%APPDATA%\Claude\logs
```

#### macOS
```
~/Library/Logs/Claude
```

### Test with Alternative Configuration

If the server still fails, try this minimal configuration:

```json
{
  "mcpServers": {
    "test-server": {
      "command": "python",
      "args": ["-c", "print('Hello from MCP'); import time; time.sleep(60)"],
      "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
    }
  }
}
```

If this works, the issue is with your server script. If this doesn't work, the issue is with Claude's MCP configuration.

## 🛠️ Quick Fixes Checklist

- [ ] **File paths**: Use absolute paths with double backslashes
- [ ] **JSON syntax**: Validate JSON format
- [ ] **Python installation**: Verify Python is accessible
- [ ] **Dependencies**: Install `mcp` and `aiofiles`
- [ ] **Virtual environment**: Activate if using .venv
- [ ] **File permissions**: Ensure server.py is readable
- [ ] **Claude restart**: Restart Claude Desktop after config changes
- [ ] **Config location**: Verify correct config file location

## 📋 Working Configuration Template

Copy this exact configuration, replacing paths with your actual paths:

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1\\.venv\\Scripts\\python.exe",
      "args": ["server.py"],
      "cwd": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1",
      "env": {
        "PYTHONPATH": "C:\\Users\\Admin\\Documents\\misogiai\\week-4\\w4d2\\assignment-1"
      }
    }
  }
}
```

## 🆘 Still Having Issues?

1. **Test the server independently**:
   ```bash
   python server.py
   ```

2. **Check Python and MCP installation**:
   ```bash
   python --version
   pip list | findstr mcp
   ```

3. **Verify file structure and permissions**

4. **Try the minimal test configuration above**

5. **Check Claude Desktop logs for specific error messages**

The most common issue is incorrect file paths in the configuration. Ensure you're using the exact absolute paths to your files with proper escaping for Windows paths.