TODO: dependencies

To run:

After setting up your pi according to the documents in https://github.com/hzeller/rpi-rgb-led-matrix

1. Clone repo
2. Create .env file with your Last FM credentials in the following layout replacing the placeholders with the correct data:

LAST_FM_API_KEY=your-api-key
LAST_FM_SS=your-shared-secret
LAST_FM_USERNAME=your-username
LAST_FM_PASSWORD=your-password

3. Give repo permissions to read/write by running chmod -R 744 repo-dir
4. Run with python3 main.py


To launch on startup of Pi (with DietPi installed):

1. Navigate to /lib/systemd/system
2. Create a service file with "sudo nano your-name.service"
3. Type in the following
   
    [Unit]
    Description=your-description
    After=local-fs.target network.target
    
    [Service]
    ExecStart=/path/to/your/python3 /path/to/App.py
    WorkingDirectory=/path/to/your/working/directory
    User=root
    ReadWritePaths=/path/to/your/working/directory

    [Install]
    WantedBy=multi-user.target

4. Give .service file 644 permissions with "chmod 644 your-service-name.service"
5. Restart daemon with "sudo systemctl daemon-reload"
6. Enable service to launch when device boots with "sudo systemctl enable your-service-name.service"
7. Start service with "sudo systemctl start your-service-name.service"
