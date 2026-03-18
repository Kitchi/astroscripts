#!/usr/bin/env bash
# Quick IO throughput benchmark: write then read a 1 GB file.
# Usage: bash bench_io.sh [/path/to/test/dir]

set -e
DIR="${1:-.}"
FILE="$DIR/.bench_io_1G.tmp"
BS="1M"
COUNT=1024

echo "=== IO Benchmark (1 GB, bs=$BS) ==="
echo "Target: $FILE"
echo ""

# Drop caches if root (Linux only)
if [ "$(uname)" = "Linux" ] && [ "$(id -u)" -eq 0 ]; then
    sync && echo 3 > /proc/sys/vm/drop_caches
    echo "(caches dropped)"
fi

# Write
echo "--- Write ---"
dd if=/dev/zero of="$FILE" bs=$BS count=$COUNT conv=fdatasync 2>&1 | tail -1

# Drop caches between read/write if possible
if [ "$(uname)" = "Linux" ] && [ "$(id -u)" -eq 0 ]; then
    sync && echo 3 > /proc/sys/vm/drop_caches
fi

# Read
echo "--- Read ---"
dd if="$FILE" of=/dev/null bs=$BS 2>&1 | tail -1

# Cleanup
rm -f "$FILE"
echo ""
echo "Done."
