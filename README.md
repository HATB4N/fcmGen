# fcmGen
FCM (Firebase Cloud Messaging) token generator.

## Disclaimer
This project is for educational purposes only.

## Credits
This project is a Python port of some of the logic from [microg/GmsCore](https://github.com/microg/GmsCore), and is licensed under the Apache License 2.0.

The following files are from the microG project:
* `fcm_token/data/checkin.proto`
* `fcm_token/data/deviceconfig.proto`

## Prerequisites
- You need to obtain a `build.prop` file from an Android device and place it in the `fcm_token/data` directory. This file is not included in this repository due to potential DMCA issues.
- Fill APP_DETAILS @ `fcm_token/fcm_reg.py`. You can get this from mitmproxy or decompiled code.
```python
APP_DETAILS = {
    "package_name": "YOUR_APP_PACKAGENAME_HERE",
    "sender_id": "YOUR_SENDER_ID_HERE",
    "version": 0, # FIX YOUR_VERSION_HERE(INT)
    "signature_hash": "FIX_TO_YOUR_SIGN_HERE",
}
```

## Usage
```sh
python3 main.py
```

## License
This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
