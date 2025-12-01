#!/bin/bash
# Usage: /scripts/take_ui_snapshot.sh file_name.xml
# Example: /scripts/take_ui_snapshot.sh home_screen.xml

set -e  # exit on error

# Determine script metadata
SCRIPT_NAME="$(basename "$0")"

# Check for argument
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a file name (e.g. /scripts/$SCRIPT_NAME ui_snapshot_name.xml)"
  exit 1
fi

# Extract CLI argument
FILE_NAME="$1"
FILE_NAME_XML="$1.xml"
FILE_NAME_IMG="$1.png"

# Determine script directory (ensures correct path even if run from /)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Define local output directory inside /scripts
OUTPUT_DIR="$SCRIPT_DIR/../../ui_snapshots"

# Create output directory if not exists
mkdir -p "$OUTPUT_DIR"

echo "📱 Dumping UI hierarchy from device..."
adb shell uiautomator dump "/sdcard/$FILE_NAME_XML"

echo "⬇️ Pulling dump file to $FILE_NAME_XML"
adb pull "/sdcard/$FILE_NAME_XML" "$OUTPUT_DIR/"

echo "📸 Capturing device screenshot..."
adb shell screencap -p "/sdcard/$FILE_NAME_IMG"

echo "⬇️ Pulling screenshot to $FILE_NAME_IMG"
adb pull "/sdcard/$FILE_NAME_IMG" "$OUTPUT_DIR/"

echo "✅ Files saved to $OUTPUT_DIR/"
