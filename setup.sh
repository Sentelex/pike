#!/bin/bash

# Pike setup script
echo "🔧 Setting up Pike environment..."

# Set up local NVM directory
export PIKE_ROOT_DIR="$(pwd)"
export NVM_DIR="${PIKE_ROOT_DIR}/.nvm"

# Install NVM locally if not already installed
if [ ! -d "$NVM_DIR" ]; then
  echo "📥 Installing NVM locally..."
  mkdir -p "$NVM_DIR"
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | NVM_DIR="$NVM_DIR" bash
fi

# Load NVM
export NVM_DIR="${PIKE_ROOT_DIR}/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js v18 using local NVM
echo "📦 Installing Node.js v18..."
nvm install 18
nvm use 18

# Install frontend dependencies
echo "📁 Setting up frontend..."
cd frontend || exit
npm install
cd ..

# Set up Python virtual environment
echo "🐍 Setting up backend environment..."
cd backend || exit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

echo "✅ Setup complete!"
