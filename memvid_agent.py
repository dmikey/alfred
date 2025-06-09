import os
import json
import requests
from memvid import MemvidChat
from openai import OpenAI

def load_memvid_memory():
    """Load pre-created memvid memory files"""
    video_path = "memory.mp4"
    index_path = "memory_index.json"
    
    # Verify memory files exist
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Memory video file not found: {video_path}")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Memory index file not found: {index_path}")
    
    print(f"Loading memory from {video_path} and {index_path}")
    return video_path, index_path

def get_chatgpt_response(issue_content, memvid_context, api_key):
    """Get response from ChatGPT using issue content and memvid context"""
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    You are a helpful GitHub issue assistant. Based on the following context from our knowledge base and the user's issue, provide a helpful response.

    Knowledge Base Context:
    {memvid_context}

    User Issue:
    {issue_content}

    Please provide a helpful, concise response that addresses the user's issue. If you can suggest solutions or next steps, please include them.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful GitHub issue assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def post_issue_comment(repo_owner, repo_name, issue_number, comment, github_token):
    """Post a comment to the GitHub issue"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201

def main():
    # Get environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    issue_title = os.getenv('ISSUE_TITLE')
    issue_body = os.getenv('ISSUE_BODY') or ""
    issue_number = os.getenv('ISSUE_NUMBER')
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')
    
    if not all([github_token, openai_api_key, issue_title, issue_number, repo_owner, repo_name]):
        print("Missing required environment variables")
        return
    
    print(f"Processing issue #{issue_number}: {issue_title}")
    
    # Load pre-created memvid memory
    video_path, index_path = load_memvid_memory()
    
    # Get context from memvid
    chat = MemvidChat(video_path, index_path)
    chat.start_session()
    
    # Query memvid for relevant context
    issue_content = f"Title: {issue_title}\nBody: {issue_body}"
    memvid_response = chat.chat(f"What information is relevant to this issue: {issue_content}")
    
    print(f"Memvid context: {memvid_response}")
    
    # Get ChatGPT response
    chatgpt_response = get_chatgpt_response(issue_content, memvid_response, openai_api_key)
    
    print(f"ChatGPT response: {chatgpt_response}")
    
    # Post comment to GitHub issue
    comment = f"🤖 **Automated Issue Analysis**\n\n{chatgpt_response}\n\n---\n*This response was generated automatically using our AI assistant.*"
    
    if post_issue_comment(repo_owner, repo_name, issue_number, comment, github_token):
        print("Successfully posted comment to issue")
    else:
        print("Failed to post comment to issue")

if __name__ == "__main__":
    main()
