#!/bin/bash

echo "🚀 Starting Pike..."

# Load local NVM
export PIKE_ROOT_DIR="$(pwd)"
export NVM_DIR="${PIKE_ROOT_DIR}/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18

# Start backend
cd backend || exit
source .venv/bin/activate
python pike.py &
BACKEND_PID=$!
cd ..

# Start frontend
cd frontend || exit
npm run start-dev &
FRONTEND_PID=$!
cd ..

# Wait for processes
echo "🌐 Frontend: http://localhost:8080"
echo "🛠 Backend running in background (PID $BACKEND_PID)"

wait $FRONTEND_PID
