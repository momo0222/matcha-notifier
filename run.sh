#!/bin/bash
echo ">>>Cron ran at $(date)" >> log.txt
echo "=== Matcha checker started at $(date) ==="

# Go to your project directory
cd /home/joyraspberrypi/Desktop/matcha-notifier || exit 1

git fetch origin
git reset --hard origin/main

# Run the checker script
/usr/bin/python3 /home/joyraspberrypi/Desktop/matcha-notifier/matcha-checker.py

# Commit and push if status.json changed

/usr/bin/git add .
/usr/bin/git commit -m "Auto update status.json from Raspberry Pi" || echo "No changes to commit"
/usr/bin/git push

