#!/bin/bash

# Define variables
REPO_URL="https://github.com/Vivekpsps3/Thinkerbot"
DEPLOY_DIR="~/Deployments/Thinkerbot"
LOG_FILE="~/Deployments/log.log"

# Function to log messages
log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# Function to perform deployment
deploy() {
    log_message "Starting deployment..."

    # Navigate to deployment directory
    cd "$DEPLOY_DIR" || { log_message "Error: Deployment directory not found."; exit 1; }

    # Pull the latest changes from GitHub
    git pull origin master >> "$LOG_FILE" 2>&1 || { log_message "Error: Failed to pull latest changes from GitHub."; exit 1; }

    # Additional deployment steps (e.g., install dependencies, restart services)
    # Example:
    # npm install
    # pm2 restart your_app_name

    log_message "Deployment successful."
}

# Main script execution
deploy
