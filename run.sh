#!/bin/bash

# Set library paths for WeasyPrint dependencies
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Run the main script
python3 main.py "$@"