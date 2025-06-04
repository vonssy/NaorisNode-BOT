# Naoris Node Protocol BOT
Naoris Node Protocol BOT

- Register Here : [Naoris Protocol Testnet](https://naorisprotocol.network/testnet)
- Dwonload Wallet: [Naoris Protocol Wallet](https://chromewebstore.google.com/detail/naoris-protocol-wallet/dbgibbbeebmbmmhmebogidfbfehejgfo)
- Dwonload Extension: [Naoris Protocol Browser Security Node](https://chromewebstore.google.com/detail/naoris-protocol-browser-s/cpikalnagknmlfhnilhfelifgbollmmp)
- Use Code `TRASzfGgEMFGHj9K`

## Features

  - Auto Get Account Information
  - Auto Run With [Monosans](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) Proxy - `Choose 1`
  - Auto Run With Private Proxy - `Choose 2`
  - Auto Run Without Proxy - `Choose 3`
  - Auto Rotate Invalid Proxies - `y` or `n`
  - Auto Add to Whitelisted
  - Auto Activating Protection
  - Auto Send Ping Every 10 Seconds
  - Auto Send Initiate Message Production Every 10 Minutes
  - Multi Accounts With Threads

- Note: Points Not Increase? pending bruh. please be patient.

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/vonssy/NaorisNode-BOT.git
   ```
   ```bash
   cd NaorisNode-BOT
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Configuration

### Screenshots

<div style="text-align: center;">
  <img src="image.png" alt="Image" width="500"/>
</div>

- **accounts.json:** You will find the file `accounts.json` inside the project directory. Make sure `accounts.json` contains data that matches the format expected by the script. Here are examples of file formats:
  ```json
    [
        {
            "Address": "your_naoris_wallet_address_1",
            "deviceHash": "your_device_hash"
        },
        {
            "Address": "your_naoris_wallet_address_2",
            "deviceHash": "your_device_hash"
        }
    ]
  ```

- **proxy.txt:** You will find the file `proxy.txt` inside the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Run

```bash
python bot.py #or python3 bot.py
```

## Buy Me a Coffee

- **EVM:** 0xe3c9ef9a39e9eb0582e5b147026cae524338521a
- **TON:** UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB
- **SOL:** E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf
- **SUI:** 0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

**vonssy**