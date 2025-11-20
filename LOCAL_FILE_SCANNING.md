# Local File Scanning for SD Elements Projects

## Overview

The `create_project_from_local_files` tool automatically scans your local workspace to detect technologies, frameworks, and dependencies, then creates an SD Elements project with the detected survey answers.

## How It Works

1. **File Scanning**: Scans common dependency and configuration files:
   - `pyproject.toml` - Python projects
   - `requirements.txt` - Python dependencies
   - `package.json` - Node.js/JavaScript projects
   - `Gemfile` - Ruby projects
   - `pom.xml` - Java/Maven projects
   - `Cargo.toml` - Rust projects
   - `go.mod` - Go projects
   - `composer.json` - PHP projects
   - `Dockerfile` / `docker-compose.yml` - Containerization
   - `.env` files - Environment configuration
   - Code files (`.py`, `.js`, `.ts`, etc.) - Framework detection
   - `README.md` - Project description

2. **Technology Detection**: Identifies:
   - Programming languages (Python, JavaScript, TypeScript, Java, etc.)
   - Frameworks (Django, Flask, React, Express, etc.)
   - Databases (PostgreSQL, MySQL, MongoDB, Redis, etc.)
   - Infrastructure (Docker, Kubernetes, etc.)
   - Data formats (JSON, XML, etc.)

3. **Project Creation**: 
   - Creates or uses an existing application
   - Creates a new project
   - Automatically sets survey answers based on detected technologies
   - Commits the survey draft (by default)

## Usage

### Basic Usage

```python
# In MCP client (Cursor, Claude Desktop, etc.)
"Create an SD Elements project from the files in this workspace"
```

### With Parameters

```json
{
  "workspace_path": "/path/to/workspace",
  "application_name": "My Application",
  "project_name": "My Project",
  "project_description": "Optional description",
  "auto_commit": true
}
```

### Parameters

- `workspace_path` (optional): Path to scan. Defaults to current working directory.
- `application_name` (optional): Name of application to create/use.
- `application_id` (optional): Use existing application by ID.
- `project_name` (optional): Project name. Defaults to workspace directory name.
- `project_description` (optional): Project description. Auto-generated from scan results if not provided.
- `profile_id` (optional): SD Elements profile to use. Auto-selected if not provided.
- `auto_commit` (optional, default: true): Whether to automatically commit the survey draft.
- `reuse_existing_project` (optional, default: false): Reuse existing project with same name.

## Example Workflow

1. **Navigate to your project directory**
2. **Call the tool**:
   ```
   "Create an SD Elements project from local files"
   ```
3. **The tool will**:
   - Scan all relevant files
   - Detect technologies (e.g., Python, Django, PostgreSQL, Docker)
   - Create the application and project
   - Set survey answers automatically
   - Commit the survey draft
   - Return project details and scan results

## Detection Examples

### Python Project with Django

**Files scanned:**
- `pyproject.toml` → Detects Python, Django
- `requirements.txt` → Detects additional dependencies
- Code files → Detects Django imports

**Detected technologies:**
- Python
- Django
- Generic server
- Uses an HTTP-based protocol
- JSON

### Node.js Project with Express

**Files scanned:**
- `package.json` → Detects JavaScript, Express
- Code files → Detects Express imports

**Detected technologies:**
- JavaScript
- Express
- Node.js
- Generic server
- Uses an HTTP-based protocol

### Dockerized Application

**Files scanned:**
- `Dockerfile` → Detects Docker
- `docker-compose.yml` → Detects Docker

**Detected technologies:**
- Docker
- (Plus other detected technologies)

## Limitations

1. **File Scanning**: Limited to first 50 code files to avoid performance issues
2. **Technology Mapping**: Some technologies may not map directly to SD Elements answers
3. **Dependency Parsing**: Simple regex-based parsing for TOML files if `toml` library not available
4. **Framework Detection**: Based on common patterns; may miss custom frameworks

## Comparison with Other Tools

### `create_project_from_code`
- Does NOT scan files
- Returns survey structure for manual review
- Requires manual answer setting and commit

### `create_project_from_local_files` (NEW)
- Automatically scans local files
- Detects technologies automatically
- Sets survey answers automatically
- Commits survey draft automatically (optional)

### `scan_repository` (Repository Scanning)
- Requires GitHub/GitLab connection
- Scans remote repository
- May require authentication
- Server-side scanning (more comprehensive)

## Implementation Details

### File Scanner Module

Located in `src/sde_mcp_server/file_scanner.py`:

- `FileScanner` class: Main scanner implementation
- `scan()` method: Entry point for scanning
- Individual `_scan_*` methods: Scan specific file types
- Technology detection: Keyword matching and pattern recognition

### Technology Mappings

Technologies are mapped to SD Elements answer texts:

```python
tech_mappings = {
    "Python": "Python",
    "Django": "Django",
    "Docker": "Docker",
    # ... etc
}
```

### Survey Answer Setting

Uses `add_survey_answers_by_text` with:
- Fuzzy matching (threshold: 0.75)
- Automatic dependency resolution
- Error handling for unmatched technologies

## Future Enhancements

1. **Better TOML Parsing**: Full TOML library support
2. **More File Types**: Support for additional dependency files
3. **Smarter Detection**: Machine learning-based technology detection
4. **Configuration**: Allow customization of detection rules
5. **Incremental Updates**: Update existing projects with new detections

