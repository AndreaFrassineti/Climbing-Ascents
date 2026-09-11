import json
import os
import requests

USER_SLUG = "andrea-frassineti"
OUTPUT_FILE = "data/ascents.json"
COOKIE = os.environ.get("EIGHT_A_COOKIE", "")

def fetch_ascents_by_category(user_slug, category):
    all_category_ascents = []
    page_index = 0
    page_size = 50

    while True:
        url = f"https://www.8a.nu/api/unification/ascent/v1/web/users/{user_slug}/ascents"
        params = {
            "category": category,
            "pageIndex": page_index,
            "pageSize": page_size,
            "sortField": "grade_desc",
            "timeFilter": 0,
            "gradeFilter": 0,
            "includeProjects": "false",
            "showRepeats": "false",
            "showDuplicates": "false"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 OPR/135.0.0.0",
            "Accept": "*/*",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": f"https://www.8a.nu/user/{user_slug}/{category}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        
        if COOKIE:
            headers["Cookie"] = COOKIE

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                ascents = data.get("ascents", [])
                
                if not ascents:
                    break
                
                all_category_ascents.extend(ascents)
                
                if len(ascents) < page_size:
                    break
                
                page_index += 1
            else:
                print(f"Errore HTTP {response.status_code} durante il recupero di '{category}' (pagina {page_index})")
                break
        except Exception as e:
            print(f"Eccezione durante la richiesta per '{category}': {e}")
            break

    return all_category_ascents

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    total_ascents = []

    for category in ["sportclimbing", "bouldering"]:
        ascents = fetch_ascents_by_category(USER_SLUG, category)
        print(f"Trovate {len(ascents)} ascensioni per '{category}'")
        total_ascents.extend(ascents)

    print(f"Totale ascensioni recuperate: {len(total_ascents)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(total_ascents, f, ensure_ascii=False, indent=2)

    print(f"File salvato correttamente in {OUTPUT_FILE}")
