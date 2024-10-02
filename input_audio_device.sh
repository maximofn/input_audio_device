#!/usr/bin/bash
# Get script path
SCRIPT_PATH=$(dirname $0)
/usr/bin/python3 $SCRIPT_PATH/input_audio_device.py >input_audio_device.log 2>input_audio_device_error.log