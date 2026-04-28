# ⚡ PinPulse
[![PyPI version](https://badge.fury.io/py/pinpulse.svg)](https://badge.fury.io/py/pinpulse)

**PinPulse** is a high-performance, asynchronous PIN brute-force tool built with Python. Utilizing `asyncio` and `aiohttp`, it is designed to test the resilience of PIN-based authentication mechanisms through rapid, concurrent HTTP requests.

## ✨ Features
* 🚀 **Asynchronous Architecture:** Built on `aiohttp` for non-blocking network I/O, allowing hundreds of requests per second.
* 📊 **Real-time Progress:** Integrated with `tqdm` to provide a live progress bar, estimated time remaining, and request speed.
* 🛠️ **Fully Parameterized:** Easily adjust the target URL, concurrency limits, and PIN digit length directly from the terminal.
* 🛡️ **Smart Termination:** Automatically halts all active tasks as soon as the correct PIN is identified to save resources.

## 📦 Installation

### 1. Via PyPI (Recommended)
The easiest way to install PinPulse is directly via pip. This will add the `pinpulse` command to your system PATH.
```bash
pip install pinpulse
```

### 2. From Source (Manual)
If you want to run the latest development version or modify the code:
```bash
git clone https://github.com/fr0stb1rd/PinPulse.git
cd PinPulse
pip install -r requirements.txt
```
*(Note: Requires Python 3.8+)*

## 🚀 Usage

If installed via **PyPI**, you can run it directly:
```bash
pinpulse -u "http://target-site.com/verify"
```

If running from **Source**:
```bash
python -m pinpulse -u "http://target-site.com/verify"
```

### Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--url` | `-u` | The target endpoint URL | (Required) |
| `--concurrent` | `-c` | Number of simultaneous requests | 50 |
| `--digits` | `-d` | Number of PIN digits to test | 4 |

### Examples

**Testing for a 6-digit PIN:**
```bash
pinpulse -u "https://api.example.com/v1/auth" -d 6
```

**Aggressive testing with 100 concurrent workers:**
```bash
pinpulse -u "https://api.example.com/v1/auth" -c 100
```

## 🛠️ How It Works
PinPulse uses an asynchronous `Semaphore` to manage request flow. This ensures that the tool respects your system's limits while maintaining maximum throughput. The script evaluates the HTTP response body for specific failure strings (e.g., "Incorrect pin code") to determine success or failure.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer
This tool is developed for educational purposes and authorized security testing (Pentesting) only. Running this against systems without explicit permission is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

