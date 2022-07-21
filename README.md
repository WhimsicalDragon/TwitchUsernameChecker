# Twitch SMS Notifications

This is a simple python program that check if a twitch username is avalible every half hour.

---
## Author

WhimsicalDragon1337 [Twitter](https://twitter.com/Whimsical1337)
This was made specifically for Miu: [Twitch](https://www.twitch.tv/miwupy) [Twitter](https://twitter.com/Miwupy). If you'd like to commission me for a code project you can reach out to me on twitter!
You could've watched me code this live at [Twitch](https://www.twitch.tv/whimsicaldragon1337) ~~if my internet had been working when I was coding this~~

---
## Usage

To use this you will need a few api keys.

1. Get your Twitch Client ID and Client Secret: [Link](https://dev.twitch.tv/docs/api/get-started)
2. Enter these details as well into a config.py file.
3. Run the program. It will automatically check if the username is availble every half hour. If the username is avaible it will print a message stating that the user does not exist as well as a confidence level.

---
## Details & Caveats

This program makes a twitch API call every 30 minutes. If the hosting machine goes offline it will stop making calls and if twitch dies it will probably stop working.

---
## Support

I am a starving graduate student. Please give me money so I can keep coding dumb stuff. Also if I get enough money I can host this as webapp so you don't have to run it yourself! You can do that [here](https://ko-fi.com/whimsicaldragon1337)