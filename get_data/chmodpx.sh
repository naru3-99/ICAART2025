#!/bin/bash

folder="malware_samples"

for file in "$folder"/*; do
    if [[ -f "$file" ]]; then
        chmod +x "$file"
    fi
done
