import os
import json
import requests
from memvid import quick_chat
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

def get_chatgpt_pr_response(pr_content, memvid_context, api_key):
    """Get response from ChatGPT using PR content and memvid context"""
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    You are a helpful GitHub pull request assistant. Based on the following context from our knowledge base and the pull request details, provide a helpful review or feedback.

    Knowledge Base Context:
    {memvid_context}

    Pull Request:
    {pr_content}

    Please provide a helpful, constructive response that reviews the pull request. Focus on:
    - Code quality and best practices
    - Potential issues or improvements
    - Alignment with project standards
    - Suggestions for enhancement

    Keep your response concise and actionable.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful GitHub pull request reviewer."},
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

def post_pr_comment(repo_owner, repo_name, pr_number, comment, github_token):
    """Post a comment to the GitHub pull request"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
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
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')
    
    # Check if this is for an issue or PR
    issue_title = os.getenv('ISSUE_TITLE')
    issue_body = os.getenv('ISSUE_BODY') or ""
    issue_number = os.getenv('ISSUE_NUMBER')
    
    pr_title = os.getenv('PR_TITLE')
    pr_body = os.getenv('PR_BODY') or ""
    pr_number = os.getenv('PR_NUMBER')
    pr_action = os.getenv('PR_ACTION')  # e.g., 'opened', 'synchronize', etc.
    
    if not all([github_token, openai_api_key, repo_owner, repo_name]):
        print("Missing required environment variables")
        return
    
    # Load pre-created memvid memory
    video_path, index_path = load_memvid_memory()
    
    # Handle PR if PR data is provided and action is 'opened'
    if pr_title and pr_number and pr_action == 'opened':
        print(f"Processing PR #{pr_number}: {pr_title}")
        
        # Get context from memvid using quick_chat
        pr_content = f"Title: {pr_title}\nBody: {pr_body}"
        query = f"What information is relevant to this pull request: {pr_content}"
        
        # Use quick_chat to get memvid response
        memvid_response = quick_chat(video_path, index_path, query)
        
        print(f"Memvid context: {memvid_response}")
        
        # Get ChatGPT response for PR
        chatgpt_response = get_chatgpt_pr_response(pr_content, memvid_response, openai_api_key)
        
        print(f"ChatGPT PR response: {chatgpt_response}")
        
        # Post comment to GitHub PR
        comment = f"🤖 **Automated PR Review**\n\n{chatgpt_response}\n\n---\n*This review was generated automatically using our AI assistant.*"
        
        if post_pr_comment(repo_owner, repo_name, pr_number, comment, github_token):
            print("Successfully posted comment to PR")
        else:
            print("Failed to post comment to PR")
    
    # Handle issue if issue data is provided
    elif issue_title and issue_number:
        print(f"Processing issue #{issue_number}: {issue_title}")
        
        # Get context from memvid using quick_chat
        issue_content = f"Title: {issue_title}\nBody: {issue_body}"
        query = f"What information is relevant to this issue: {issue_content}"
        
        # Use quick_chat to get memvid response
        memvid_response = quick_chat(video_path, index_path, query)
        
        print(f"Memvid context: {memvid_response}")
        
        # Get ChatGPT response for issue
        chatgpt_response = get_chatgpt_response(issue_content, memvid_response, openai_api_key)
        
        print(f"ChatGPT response: {chatgpt_response}")
        
        # Post comment to GitHub issue
        comment = f"🤖 **Automated Issue Analysis**\n\n{chatgpt_response}\n\n---\n*This response was generated automatically using our AI assistant.*"
        
        if post_issue_comment(repo_owner, repo_name, issue_number, comment, github_token):
            print("Successfully posted comment to issue")
        else:
            print("Failed to post comment to issue")
    else:
        print("No valid issue or PR data provided. Skipping processing.")

if __name__ == "__main__":
    main()
