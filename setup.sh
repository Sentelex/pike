#!/bin/bash

# Pike setup script

echo "🔧 Setting up Pike environment..."

# Install Node.js via NVM
if ! command -v nvm &> /dev/null
then
  echo "📥 Installing NVM..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

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
