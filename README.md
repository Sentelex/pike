# pike
Personal Interactive Knowledge Exploration


# Installation
## Frontend
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 18
    nvm use 18
    cd frontend
    npm i
    npm run start-dev

To access the frontend, navigate to:
     http://localhost:8080

## Backend
    Create a virtual environment for your python interpreter to run the backend:
