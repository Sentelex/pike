#!/bin/bash

# Node v18 or greater
minimum_node_version=18

# Python 3.10 or greater
minimum_python_major=3
minimum_python_minor=10
minimum_python="$minimum_python_major.$minimum_python_minor"

PIKE_root=$PWD
BE_root="$PIKE_root/backend"
FE_root="$PIKE_root/frontend"

node_version() {
  if command -v node &> /dev/null; then
    version=$(node -v | sed 's/[^0-9]*\([0-9]*\).*/\1/')
    echo $version
  fi
}

python_version() {
  if command -v python3 &> /dev/null; then
    version=$(python3 --version | sed 's/[^0-9]*\([0-9]*\)\.\([0-9]*\).*/\1.\2/')
    echo $version
  fi
}

split_version() {
  local version="$1"
  IFS='.' read -r major minor <<< "$version"
  echo "$major $minor"
}

install_local_node() {
  echo "📥 Installing a local copy of NVM..."
  NVM_DIR="${FE_root}/.nvm"
  mkdir -p $NVM_DIR
  echo "Using NVM installation directory ${NVM_DIR}."
  # PROFILE command keeps local installation from placing this NVM dir in login
  #   .shellrc
  PROFILE=/dev/null NVM_DIR="$NVM_DIR" bash -c "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"
  export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${NVM_DIR}" || printf %s "${XDG_CONFIG_HOME}/nvm")"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  echo "📦 Installing local version of Node.js v18..."
  nvm install 18
  nvm use 18
}

install_python_venv() {
  # Incoming argument has the validated version of python.
  echo "🐍 Setting up backend environment..."
  $1 -m venv $BE_root/.venv
  source $BE_root/.venv/bin/activate
  pip install -r $BE_root/requirements.txt
  deactivate
  cd ..
}

build_start_script() {
echo '#!/bin/bash' >& ${PIKE_root}/start.sh
echo "NVM_DIR=${NVM_DIR}" >> ${PIKE_root}/start.sh
echo 'export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${NVM_DIR}" || printf %s "${XDG_CONFIG_HOME}/nvm")"' >> ${PIKE_root}/start.sh
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ${PIKE_root}/start.sh
echo '
echo "🚀 Starting Pike..."

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
' >> ${PIKE_root}/start.sh
chmod 540 ${PIKE_root}/start.sh

}

# Check to see if node is already installed and, if so, what version we have.
node_major=$(node_version)
if [[ -z "$node_major" ]]; then
  echo "Node is not installed."
  install_local_node
else
  if [[ $node_major -lt $minimum_node_version ]]; then
    echo "Node version $node_major found."
    echo "  Version requires must be >= $minimum_node_version."
    install_local_node
  else
   echo "Node version >= $minimum_node_version found."
   echo "  Using system node version."
  fi
fi

# Either way we should now be ready to install frontend dependencies
echo "📁 Setting up frontend..."
cd frontend || exit
npm install
cd ..

python_major_minor=$(python_version)
read python_major python_minor <<< $(split_version "$python_major_minor")

if [[ -z "$python_major_minor" || $python_major < $minimum_python_major ]]; then
  echo "Could not find a version of python$minimum_python_major to run backend."
  echo "  Minimum python version required = $minimum_python ."
  exit 0
else
  if [[ $python_minor < $minimum_python_minor ]]; then
    echo "Found an executable for python $python_major_minor ."
    echo "  However, the minimum version required is python $minimum_python ."
    echo "  Please update your python version and try again."
    exit 0
  else
    install_python_venv python$python_major_minor
  fi
fi

build_start_script

echo "✅ Setup complete!"
