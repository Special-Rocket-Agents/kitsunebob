# kitsunebob
Single-server personal Discord bot for my server.
## Requirements
`sudo apt install python3-discord` or `pip3 install discord` iirc

There is a `config.json` that you need to create *yourself*
and the format goes like this:
```json
{
    "token": "",
    "log_id": "",
    "guild_id": ""
}
```

`token`: your bot's token, duh

`log_id`: This is the channel that reported messages are sent to, you can report a message by right clicking the message > Apps > Report (with Kitsune's profile photo)

> Have I mentioned that this channel needs to be private?

`guild_id`: this is your server's ID.

All these secrets can be obtained by activating developer mode on discord

## IMPORTANT: Slash command overrides:
There are moderator commands that should not be accessible to everyone, to natively prevent abuse:

1. go to server settings
2. click on Integrations
3. scroll down until you find Kitsune Bob
4. make sure these commands are tweaked so that only highly trusted administrators can run it.
   - `/emergency_shutdown`: Shuts down and exits the script. This is the last resort when you (for any reason) can't access the hosting and shut down yourself
   - `/send`: This allows the bot to send **any text**, this can be surely abused so give access to trusted members, not everyone.
   - *The Report Button*: Make sure these can be only used in genuine discussion channels so that people don't randomly report announcements or your own message.

## so...
I have~n't~ made the effort to publicize it... ~*yet*~

~That means there are some holes and placeholders I have to fill.~

And another todo:
~Make the token's place somewhere outside of the main code so that it can be git ignored~
