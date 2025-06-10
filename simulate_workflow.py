#!/usr/bin/env python3
"""
Simulate GitHub issue workflow locally
This simulates what happens when a GitHub issue is created
"""

import os
from memvid_agent import main as memvid_main

def simulate_memvid_agent_with_fake_github(title, body="", repo_owner="test-owner", repo_name="test-repo", issue_number="123"):
    """
    Simulate the memvid agent workflow by temporarily modifying the GitHub posting behavior
    """
    
    print(f"🎭 Simulating GitHub Issue #{issue_number}")
    print(f"Title: {title}")
    print(f"Body: {body}")
    print(f"Repo: {repo_owner}/{repo_name}")
    print("-" * 50)
    
    # Set environment variables (same as GitHub Actions would)
    env_vars = {
        'ISSUE_TITLE': title,
        'ISSUE_BODY': body,
        'ISSUE_NUMBER': issue_number,
        'REPO_OWNER': repo_owner,
        'REPO_NAME': repo_name,
        'GITHUB_TOKEN': 'fake-token-for-testing',  # We won't actually post
    }
    
    # Get OpenAI key from environment
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        env_vars['OPENAI_API_KEY'] = openai_key
    else:
        print("⚠️  No OpenAI API key found in environment")
        env_vars['OPENAI_API_KEY'] = 'fake-key-for-testing'
    
    # Backup original environment
    original_env = {}
    for key in env_vars:
        original_env[key] = os.getenv(key)
    
    try:
        # Set test environment variables
        for key, value in env_vars.items():
            os.environ[key] = value
        
        print("🚀 Running memvid agent workflow...")
        
        # Temporarily monkey-patch the post_issue_comment function to simulate posting
        import memvid_agent
        original_post_function = memvid_agent.post_issue_comment
        
        def fake_post_issue_comment(repo_owner, repo_name, issue_number, comment, github_token):
            """Simulate posting to GitHub without actually doing it"""
            print(f"\n📝 Comment that would be posted to GitHub Issue #{issue_number}:")
            print(f"Repository: {repo_owner}/{repo_name}")
            print(f"Comment:\n{comment}")
            print("\n✅ (Simulated) Successfully posted comment to issue")
            return True
        
        # Replace the function temporarily
        memvid_agent.post_issue_comment = fake_post_issue_comment
        
        try:
            # Run the actual memvid agent main function
            memvid_main()
        except Exception as e:
            print(f"❌ Error running memvid agent: {e}")
        finally:
            # Restore original function
            memvid_agent.post_issue_comment = original_post_function
        
        print("\n✅ Simulation complete!")
        
    finally:
        # Restore original environment
        for key, original_value in original_env.items():
            if original_value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = original_value

def main_simulation():
    """Run predefined test scenarios"""
    
    test_scenarios = [
        {
            "title": "Installation help needed",
            "body": "I'm having trouble installing the dependencies. Can someone help me?",
        },
        {
            "title": "How to create memory files?",
            "body": "I want to set up my own memvid memory but I'm not sure how to do it.",
        },
        {
            "title": "API integration question",
            "body": "How do I integrate this with my existing API? What are the requirements?",
        }
    ]
    
    print("🎪 GitHub Issue Workflow Simulation")
    print("=" * 50)
    print("This simulates the complete workflow that runs when GitHub issues are created.\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"Scenario {i}/{len(test_scenarios)}")
        simulate_memvid_agent_with_fake_github(scenario["title"], scenario["body"])
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main_simulation()
