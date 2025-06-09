"""
Script to create and encode memvid memory from knowledge base.
Run this script locally before committing to create the memory files.
"""

from memvid import MemvidEncoder

def create_knowledge_base():
    """Create video memory from knowledge base chunks"""
    # Expand this with your actual knowledge base content
    chunks = [
        "Our project provides automated issue analysis and response capabilities",
        "We use AI to understand and respond to user issues effectively", 
        "The system can provide helpful guidance and solutions for common problems",
        "We maintain documentation and best practices for issue resolution",
        "Historical issue patterns help improve our response quality",
        "Common troubleshooting steps include checking logs, verifying configuration, and testing connectivity",
        "Performance issues often relate to memory usage, database queries, or network latency",
        "Security concerns should be addressed immediately with proper authentication and authorization",
        "Documentation should be kept up to date and easily accessible to users",
        "Code quality is maintained through proper testing, code reviews, and continuous integration"
    ]
    
    print("Creating memvid encoder...")
    encoder = MemvidEncoder()
    
    print(f"Adding {len(chunks)} knowledge chunks...")
    encoder.add_chunks(chunks)
    
    print("Building video memory...")
    encoder.build_video("memory.mp4", "memory_index.json")
    
    print("✅ Memory files created successfully!")
    print("Files created: memory.mp4, memory_index.json")
    print("These files should be committed to the repository.")

if __name__ == "__main__":
    create_knowledge_base()
