#!/bin/bash
# Setup script for local testing

echo "🔧 Setting up local testing environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run tests:"
echo "  source venv/bin/activate"
echo "  python test_local.py"
echo ""
echo "For interactive testing:"
echo "  python test_local.py interactive"
echo ""
echo "Optional: Set OPENAI_API_KEY environment variable to test ChatGPT integration"
