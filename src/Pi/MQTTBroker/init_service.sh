#!/usr/bin/env bash

SCRIPT_PATH=$(cd `dirname -- $0` && pwd)
SERVICE_DIR="/etc/systemd/system"
SERVICE_NAME="broker.service"
SERVICE_FILE="$SERVICE_DIR/$SERVICE_NAME"
TEMPLATE_FILE="${SCRIPT_PATH}/$SERVICE_NAME"
#echo "$TEMPLATE_FILE"
#echo "$SERVICE_FILE"

sudo touch "$SERVICE_FILE"
sudo chmod 664 "$SERVICE_FILE"
# Check if fileA exists
if [ -e "$TEMPLATE_FILE" ]; then
    # Copy the contents of fileA to fileB
    sudo cp "$TEMPLATE_FILE" "$SERVICE_FILE"
    echo "Contents of TEMPLATE_FILE copied to SERVICE_FILE successfully."
else
    echo "Error: TEMPLATE_FILE does not exist in the script directory."
fi
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"
