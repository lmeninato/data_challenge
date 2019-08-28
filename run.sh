#!/bin/bash

if [ "$1" = "-t" ]; then
  echo "Timing report creation..."
  time python3 ./src/write_data.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv
else
  python3 ./src/write_data.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv
fi