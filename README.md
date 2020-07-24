
# csgostash-scraper
Scrapes skin data from [CSGOStash](https://csgostash.com/) and saves it in JSON format.

How does it work?
--
Data is scraped from CSGOStash and transformed into specific objects, which are then saved onto pickles for easy loading onto projects (like my [Neon's Case Opening feature](https://github.com/supr3meofficial/neon/blob/V3-develop/cogs/caseopening.py))

Installation
--
1. **Install Python 3**

This is required to run the scraper.

2. **Set up venv**

Just do `python3 -m venv venv`

3. **Install dependencies**

This is `pip install -U -r requirements.txt`

4. **Run the script**

Use the following syntax `python3 main.py --method 1 --indent 2`

**Available methods:**
1. Save in a single file
2. Save in separate files

What it looks like
--
**Command-line:**
```cmd
>>> python3 main.py --method 1 --indent 2
This process can take a while, please be patient..
Adding case: Prisma 2 Case [1/33]
Done!
..
```
**File:**
```json
"CS:GO Weapon Case": {
  "url": "https://csgostash.com/case/1/CS:GO-Weapon-Case",
  "image_url": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5_T3eAQ3i6DMIW0X7ojiwoHax6egMOKGxj4G68Nz3-jCp4itjFWx-ktqfSmtcwqVx6sT/256fx256f",
  "content": {
    "Covert Skins": [
      {
        "title": "AWP | Lightning Strike",
        "url": "https://csgostash.com/skin/79/AWP-Lightning-Strike",
        "image": "https://steamcdn-a.akamaihd.net/apps/730/icons/econ/default_generated/weapon_awp_am_lightning_awp_light_large.3761894103ee0fec90af459928635933ba27e36d.png",
        "possible_wears": {
          "fn": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAZt7P_BdjVW4tW4k7-KgOfLP7LWnn9u5MRjjeyPptuj2Qzt_0JsYDymJNDAIQ8-MA7U_1i3w-bphpO1v56bmHBk7yMksWGdwUJq4NI0lg/512fx384f",
          "mw": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAZt7P_BdjVW4tW4k7-KgOfLP7LWnn9u5MRjjeyPptuj2Qzt_0JsYDymJNDAIQ8-MA7U_1i3w-bphpO1v56bmHBk7yMksWGdwUJq4NI0lg/512fx384f"
        },
        "desc": "It has been painted with a lightning strike motif using anodizing effect paints over a metallic base coat.",
        "lore": "Sometimes you don't need to strike the same place twice"
      }
    ],
```

License
--
Released under the [MIT](LICENSE) license.
