import json
import os
import requests

USER_SLUG = "andrea-frassineti"
OUTPUT_FILE = "data/ascents.json"

def fetch_ascents_by_category(user_slug, category):
    # Nuovo endpoint REST di 8a.nu
    url = f"https://www.8a.nu/api/users/{user_slug}/ascents"
    params = {
        "category": category,
        "pageIndex": 0,
        "pageSize": 1000
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("ascents", [])
        else:
            print(f"Errore HTTP {response.status_code} durante il recupero di '{category}'")
            return []
    except Exception as e:
        print(f"Eccezione durante la richiesta per '{category}': {e}")
        return []

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    all_ascents = []

    for category in ["sportclimbing", "bouldering"]:
        ascents = fetch_ascents_by_category(USER_SLUG, category)
        print(f"Trovate {len(ascents)} ascensioni per '{category}'")
        all_ascents.extend(ascents)

    print(f"Totale ascensioni recuperate: {len(all_ascents)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_ascents, f, ensure_ascii=False, indent=2)

    print(f"File salvato correttamente in {OUTPUT_FILE}")
