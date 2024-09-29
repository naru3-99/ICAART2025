#!/bin/bash

folder="malware_samples"
password="infected"

if ! command -v 7z &> /dev/null
then
    echo "7z could not be found. Please install 7-Zip."
    exit
fi

for file in "$folder"/*.zip; do
    if [[ -f "$file" ]]; then
        7z x -p"$password" "$file" -o"$folder"
        if [ $? -eq 0 ]; then
            echo "Successfully extracted $file"
        else
            echo "Failed to extract $file"
        fi
    fi
done
