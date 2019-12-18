### Build

```docker build -t tg-expose .```

### Register app

Get app id and api hash from https://my.telegram.org/

### Run 
```docker run --rm -p 5432:5432 -e API_HASH=... -e APP_ID=... tg-expose```


### Use
```localhost:5432/messages?token=...&chat=-1001453972607&to=51```

```localhost:5432/members?token=...&chat=-1001453972607```