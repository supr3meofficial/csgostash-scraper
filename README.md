
# csgostash-scraper
Scrapes skin data from [CSGOStash](https://csgostash.com/) and saves it in JSON format.

Current Release: v0.4

What data does it scrape?
--
Cases, Collections and Souvenir Packages and their respective items. \
More to be added.

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

Use the following syntax `python3 main.py`

**Available methods:**
1. Save in a single file
2. Save in separate files

What it looks like
--
**Terminal:**
```sh
$ python3 main.py
Retrieving: MAC-10 | Copper Borre
Retrieving: XM1014 | Frost Borre
Retrieving: CZ75-Auto | Emerald Quartz
Retrieving: SCAR-20 | Brass
..
```
**JSON File:**
```json
{
  "name": "CS:GO Weapon Case",
  "image_url": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5_T3eAQ3i6DMIW0X7ojiwoHax6egMOKGxj4G68Nz3-jCp4itjFWx-ktqfSmtcwqVx6sT/256fx256f",
  "content": {
    "Rare Special Items": [
      {
        "name": "★ Bayonet | Boreal Forest",
        "desc": "It has been painted using a forest camouflage hydrographic.",
        "lore": "The woods can be a dangerous place... never travel alone",
        "can_be_souvenir": false,
        "can_be_stattrak": true,
        "wears": {
          "Factory New": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zAaAJE486zh5S0lfjmNrrdqWdY781lteXA54vwxgCxqBE6Nzv0IIbBdQU6ZAuC-Vm6wu68hMe46MzIzCE26SQk7S3YzECpwUYbTEk7wBI/512fx384f",
          "Minimal Wear": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zAaAJE486zh5S0lfjmNrrdqWdY781lteXA54vwxgCxqBE6Nzv0IIbBdQU6ZAuC-Vm6wu68hMe46MzIzCE26SQk7S3YzECpwUYbTEk7wBI/512fx384f",
          "Field-Tested": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zAaAJE486zh5S0lfjmNrrdqWZU7Mxkh9bN9J7yjRrl_kFrYGjxcNOWewQ3MAmE-FG2yOe7gpW0uZyam3A2siVw7S6MzR3in1gSOUa5wz9E/512fx384f",
          "Well-Worn": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zAaAJE486zh5S0lfjmNrrdqWZU7Mxkh9bN9J7yjRrl_kFrYGjxcNOWewQ3MAmE-FG2yOe7gpW0uZyam3A2siVw7S6MzR3in1gSOUa5wz9E/512fx384f",
          "Battle-Scarred": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zAaAJE486zh5S0lfjmNrrdqWNU6dNoteXA54vwxgDhrxJtMGj7II7GcVI5MgqE-gDsyObng5W_vM-bmyFi6CkitnbayRKpwUYbBWXvKcI/512fx384f"
        }
      } 
...
```

License
--
Released under the [MIT](LICENSE) license.
