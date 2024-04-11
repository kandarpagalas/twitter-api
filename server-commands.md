# twitter-api
```bash
xvfb-run --auto-servernum uvicorn src.main:app --host 0.0.0.0 --port 8000
```

```bash
sudo nano /etc/systemd/system/twitter-api.service
```

```properties
[Unit]
Description=My Twitter Api
After=network.target
[Service]
User=kandarpa
Group=www-data
WorkingDirectory=/home/kandarpa/twitter-api
Environment="PATH=/home/kandarpa/twitter-api/venv/bin"
ExecStart="uvicorn src.main:app --host 0.0.0.0 --port 8000"
[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start twitter-api
sudo systemctl enable twitter-api
# to stop the server
sudo systemctl stop twitter-api
```

"uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"