#!/usr/bin/env bash

SCRIPT_PATH=$(cd `dirname -- $0` && pwd)
SYSTEM_DIR="/etc/systemd/system"
SERVICE_NAME="update_readme.service"
SERVICE_FILE="$SYSTEM_DIR/$SERVICE_NAME"
TEMPLATE_SERVICE_FILE="${SCRIPT_PATH}/$SERVICE_NAME"

TIMER_NAME="update_readme.timer"
TIMER_FILE="$SYSTEM_DIR/$TIMER_NAME"
TEMPLATE_TIMER_FILE="${SCRIPT_PATH}/$TIMER_NAME"

echo "$TEMPLATE_SERVICE_FILE"
echo "$SERVICE_FILE"
echo "$TEMPLATE_TIMER_FILE"
echo "$TIMER_FILE"


sudo touch "$SERVICE_FILE"
sudo chmod 664 "$SERVICE_FILE"

sudo touch "$TIMER_FILE"
sudo chmod 664 "$TIMER_FILE"
# Check if fileA exists
if [ -e "$TEMPLATE_SERVICE_FILE" ]; then
    # Copy the contents of fileA to fileB
    sudo cp "$TEMPLATE_SERVICE_FILE" "$SERVICE_FILE"
    echo "Contents of TEMPLATE_SERVICE_FILE copied to SERVICE_FILE successfully."
else
    echo "Error: TEMPLATE_SERVICE_FILE does not exist in the script directory."
fi

if [ -e "$TEMPLATE_TIMER_FILE" ]; then
    # Copy the contents of fileA to fileB
    sudo cp "$TEMPLATE_TIMER_FILE" "$TIMER_FILE"
    echo "Contents of TEMPLATE_TIMER_FILE copied to TIMER_FILE successfully."
else
    echo "Error: TEMPLATE_TIMER_FILE does not exist in the script directory."
fi

sudo systemctl daemon-reload
sudo systemctl enable "$TIMER_NAME"
sudo systemctl start "$TIMER_NAME"
