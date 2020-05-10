
# csgostash-scraper
Scrapes skin data from [CSGOStash](https://csgostash.com/) and saves it in JSON format.

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
```python
>>> python3 main.py --method 1 --indent 2
This process can take a while, please be patient..
Adding case: Prisma 2 Case [1/33]
Done!
..
```
**File:**
```json
{
  "Prisma 2 Case": [
    {
      "url": "https://csgostash.com/case/303/Prisma-2-Case"
    },
    {
      "image_url": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU1nfbOIj8W7oWzkYLdlPOsMOmIk2kGscAj2erE99Sn2AGw_0M4NW2hIYOLMlhpcmY0CRM/256fx256f"
    },
    {
      "Covert Skins": [
        {
          "title": "M4A1-S | Player Two"
        },
        {
          "image": "https://steamcdn-a.akamaihd.net/apps/730/icons/econ/default_generated/weapon_m4a1_silencer_cu_m4a1s_csgo2048_light_large.6531225ca224416df4dc6aa12c6ecea582b1e110.png"
        },
        {
          "possible_wears": [
            "fn",
            "mw",
            "ft",
            "ww",
            "bs"
          ]
        },
        {
          "desc": "It has been custom painted with bright colors and features animated versions of a GIGN CT and Pop Dog."
        },
        {
          "lore": "Press Start..."
        },
```

License
--
Released under the [GNU](LICENSE) license.
