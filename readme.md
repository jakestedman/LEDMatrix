TODO: dependencies

To run:

After setting up your pi according to the documents in https://github.com/hzeller/rpi-rgb-led-matrix

1. Clone repo
2. Create .env file with your Last FM credentials in the following layout replacing the placeholders with the correct data:

LAST_FM_API_KEY=your-api-key
LAST_FM_SS=your-shared-secret
LAST_FM_USERNAME=your-username
LAST_FM_PASSWORD=your-password

3. Give repo permissions to read/write by running chmod -R 0777 repo-dir
4. Run with python3 main.py