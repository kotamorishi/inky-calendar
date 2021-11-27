This folder contains Google calendar integration.

Steps

# 1.Set up your google calendar.
This calendar app require "readonly".

# 2.Generate credentials.json for it.
NEVER share the file with anyone.

# 3.Install dependencies
Run these 2 commands.
```bash
pip3 install google-api-python-client
pip3 install google_auth_oauthlib
```

# 4.Run
Run this command or you might want to update when google calendar is updated.
The calendar API returns latest update time.

```bash
python3 inky-gcalendar.py
```

When the first run, you might need to open up the browser for authorization.
Once you obtain the access to your calendar, this script save the token into ```token.json``` 

NOTE : If someone got your "token.json" file, they can access to your calender.
