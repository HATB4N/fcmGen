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
You need to obtain a `build.prop` file from an Android device and place it in the `fcm_token/data` directory. This file is not included in this repository due to potential DMCA issues.

## Usage
```sh
python3 main.py
```

## License
This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
