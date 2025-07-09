#!/bin/bash

# Set strict mode
set -euo pipefail

# Set up environment
RUNDIR=$(pwd)
SCRIPT="$RUNDIR/rungwemopt_script_condor_100perdt.py"
OUTPUTDIR="$RUNDIR/results"
SKYMAP_DIR="$RUNDIR"  # Update if skymaps are in a subdirectory
HEAD="without"
NUM_DAYS=1
NTILES=10

# Loop through all .fits files in SKYMAP_DIR
for SKYMAP in "$SKYMAP_DIR"/*.fits; do
    BASENAME=$(basename "$SKYMAP")

    # Extract coinctime from filename pattern: coinc-<time>-*.fits
    COINC_TIME=$(echo "$BASENAME" | cut -d'-' -f2)

    # Output header and path
    OUTHEADER="${NUM_DAYS}days_moc"
    OUTFILE="$OUTPUTDIR/${HEAD}_LI/${OUTHEADER}/${BASENAME}"

    echo "--------------------------------------------"
    echo "Running on: $BASENAME"
    echo "  Coinc time : $COINC_TIME"
    echo "  Output path: $OUTFILE"
    echo "--------------------------------------------"

    # Call Python script
    python "$SCRIPT" \
        --output-path "$OUTFILE" \
        --Ntiles "$NTILES" \
        --numDays "$NUM_DAYS" \
        --coinc-time "$COINC_TIME" \
        --skymap "$SKYMAP" \
        # --verbose

done
