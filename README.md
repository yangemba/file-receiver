# File Reciever
The application will receive file and send some common statistics

## Installation
Python 3.7

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install file-receiver.

```bash
pip install - r requirements.txt
```
Application will be listening on port 8888


## Run via Docker
(required docker-compose)

```bash
docker build -t file_receiver .
```

```bash
docker-compose up
```
Application will be listening on port 8484

## Usage

To send file use POST requests "http://localhost:8484/?uuid=ryryrurur22":
  

    POST /?uuid=ryryrurur22 HTTP/1.1
    Host: localhost:8888
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
    cache-control: no-cache    
    Content-Disposition: form-data; name="file"; filename="/home/yanhemba/workspase/text.txt
    
    responses: 200 OK
               400 Bad  

To get statistics on uuid use GET requests http://localhost:8484/?uuid=ryryrurur22:

    GET /?uuid=ryryrurur22 HTTP/1.1
    Host: localhost:8888
    Content-Type: application/x-www-form-urlencoded
    cache-control: no-cache
    Postman-Token: 6f97e518-72cb-43d0-9ee9-1d6170179e63
    
     responses: 200 OK
                {
    "text.txt_2019-10-1612:06:36.722139": {
        "mean": {
            "XY": 12,
            "XX": 6.75,
            "XW": 34
        },
        "mode": {
            "XY": 12,
            "XX": 0,
            "XW": 34
        }
    }
}   400 Bad  
                
    
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
