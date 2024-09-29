#!/bin/bash

folder="malware_samples"

for file in "$folder"/*; do
    if [[ -f "$file" ]]; then
        if file "$file" | grep -q "64-bit"; then
            echo "$file is 64-bit"
        else
            echo "$file is not 64-bit, deleting..."
            rm "$file"
        fi
    fi
done
