# Memvid GitHub Issue Agent

This repository contains a GitHub workflow that automatically processes new issues using pre-encoded memvid memory and ChatGPT to provide intelligent responses.

## How it works

1. **Memory Creation** (done once locally): Run `create_memory.py` to encode knowledge base into memvid format
2. **Issue Processing** (automated): When a new issue is opened, the workflow:
   - Reads the issue title and body
   - Loads the pre-created memvid memory files
   - Uses memvid chat to provide relevant context based on the issue
   - Calls ChatGPT with both issue content and memvid context
   - Posts an automated comment to the issue with the response

## Setup

### 1. Create Memory Files (Run Locally First)

Before committing to the repository, you need to create the memory files:

```bash
# Install memory creation dependencies
pip install -r requirements-memory.txt

# Create the memory files
python create_memory.py
```

This will create `memory.mp4` and `memory_index.json` files that should be committed to the repository.

### 2. Repository Secrets

Set up the following secret in your GitHub repository:

- `OPENAI_API_KEY`: Your OpenAI API key for ChatGPT access

The `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### 3. Permissions

The workflow requires the following permissions:
- `issues: write` - to post comments on issues
- `contents: read` - to read repository contents

These are configured in the workflow file.

## Customization

### Knowledge Base

To update the knowledge base, modify the `chunks` array in `create_memory.py`, then re-run the script and commit the updated memory files.

### Response Format

The ChatGPT response format can be customized by modifying the prompt in the `get_chatgpt_response()` function in `memvid_agent.py`.

## Files

- `create_memory.py` - Script to create memvid memory files (run locally)
- `memvid_agent.py` - Main agent that processes issues (runs in GitHub Actions)
- `.github/workflows/memvid_agent_workflow.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies for the workflow agent
- `requirements-memory.txt` - Python dependencies for memory creation
- `memory.mp4` - Pre-encoded video memory (created by `create_memory.py`)
- `memory_index.json` - Memory index file (created by `create_memory.py`)
- `README.md` - This documentation

## Workflow

1. **Initial Setup**:
   ```bash
   pip install -r requirements-memory.txt
   python create_memory.py
   git add memory.mp4 memory_index.json
   git commit -m "Add pre-encoded memory files"
   git push
   ```

2. **Usage**: Once set up, the workflow automatically runs when new issues are opened

3. **Updating Knowledge Base**:
   ```bash
   # Edit create_memory.py with new knowledge
   python create_memory.py
   git add memory.mp4 memory_index.json
   git commit -m "Update knowledge base"
   git push
   ```
