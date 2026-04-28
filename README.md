# ⚡ PinPulse
[![PyPI version](https://badge.fury.io/py/pinpulse.svg)](https://badge.fury.io/py/pinpulse) \| [Blog](https://fr0stb1rd.gitlab.io/posts/pinpulse-high-performance-async-pin-bruteforce/)

**PinPulse** is a high-performance, asynchronous PIN brute-force tool built with Python. Utilizing `asyncio` and `aiohttp`, it is designed to test the resilience of PIN-based authentication mechanisms through rapid, concurrent HTTP requests.

## ✨ Features
* 🚀 **Asynchronous Architecture:** Built on `aiohttp` for non-blocking network I/O, allowing hundreds of requests per second.
* 📊 **Real-time Progress:** Integrated with `tqdm` to provide a live progress bar, estimated time remaining, and request speed.
* 🛠️ **Deeply Customizable:** Control the PIN parameter name, success status codes, response filtering, and custom User-Agents.
* 🛡️ **Smart Termination:** Automatically halts all active tasks as soon as the correct PIN is identified to save resources and bandwidth.

## 📦 Installation

### 1. Via PyPI (Recommended)
```bash
pip install pinpulse
```

### 2. From Source
```bash
git clone https://github.com/fr0stb1rd/PinPulse.git
cd PinPulse
pip install -r requirements.txt
```

## 🚀 Usage

### Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--url` | `-u` | The target endpoint URL | (Required) |
| `--concurrent` | `-c` | Number of simultaneous requests | `50` |
| `--digits` | `-d` | Number of PIN digits to test | `4` |
| `--parameter` | `-p` | Name of the PIN query parameter | `pin_code` |
| `--status` | `-s` | Expected HTTP status code for success | `200` |
| `--text` | `-t` | Error text to look for in response | `"Incorrect pin code"` |
| `--user-agent` | `-a` | Custom User-Agent string | (Firefox 150) |

### Examples

**Standard 6-digit test with custom parameter:**
```bash
pinpulse -u "https://api.example.com/v1/verify" -d 6 -p "otp"
```

**Bypassing simple WAFs with a custom User-Agent:**
```bash
pinpulse -u "https://target.com/login" -a "MyCustomScanner/1.0" -c 100
```

**Defining success by status code and excluding specific error text:**
```bash
pinpulse -u "https://api.site.com/auth" -s 302 -t "Try Again"
```

## 🛠️ How It Works
PinPulse utilizes an asynchronous `Semaphore` to manage request flow, ensuring maximum throughput without overwhelming the local system's file descriptors. 

For every request, it checks two conditions for a "Success":
1. **HTTP Status Code:** Does the response status match the `--status` flag?
2. **Body Content:** Is the string provided in `--text` **absent** from the response body?

If both conditions are met, the PIN is flagged as correct and the process terminates immediately.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer
This tool is developed for educational purposes and authorized security testing (Pentesting) only. Running this against systems without explicit permission is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.