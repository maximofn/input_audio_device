# Input audio device manager

🔊 Input audio device manager for Ubuntu: The Ultimate manager of audio devices. Manage what device is set as output device. This user-friendly and efficient application is fully integrated with the latest Ubuntu operating system. Get live updates and optimize your development tasks. Download now and take control of your input audio devices today!

![cpu monitor](cpu_monitor.gif)

## About CPU Monitor
CPU Monitor is an intuitive tool designed for developers and professionals who need to keep an eye on their CPU health in real time. It integrates seamlessly with the Ubuntu menu bar, providing essential information at your fingertips.

## Key Features
 * Real-time Monitoring: View CPU temperature, all updated live.
 * Optimized for Ubuntu: Crafted to integrate flawlessly with the latest Ubuntu OS.

## Installation

### Clone the repository

```bash
git clone https://github.com/maximofn/cpu_monitor.git
```

or with `ssh`

```bash
git clone git@github.com:maximofn/cpu_monitor.git
```

### Install the dependencies

Make sure that you do not have any `venv` or `conda` environment installed.

```bash
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
if command -v conda &>/dev/null; then
    conda deactivate
fi
```

Now install the dependencies

```bash
sudo apt install lm-sensors
```

Select YES to all questions

```bash
sudo sensors-detect
```

Install psensor

```bash
sudo apt install psensor
```

## Execution at start-up

```bash
add_to_startup.sh
```

Then when you restart your computer, the CPU Monitor will start automatically.

## Support

Consider giving a **☆ Star** to this repository, if you also want to invite me for a coffee, click on the following button

[![BuyMeACoffee](https://img.shields.io/badge/Buy_Me_A_Coffee-support_my_work-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white&labelColor=101010)](https://www.buymeacoffee.com/maximofn)