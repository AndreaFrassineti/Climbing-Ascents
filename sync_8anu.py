import json
import os
import requests

# Inserisci il tuo slug esatto dall'URL di 8a.nu (https://www.8a.nu/user/IL-TUO-SLUG)
USER_SLUG = "andrea-frassineti"

OUTPUT_FILE = "data/ascents.json"
GRAPHQL_URL = "https://www.8a.nu/api/graphql"


def fetch_8anu_ascents(user_slug):
  query = """
    query GetAscents($userSlug: String!) {
      ascents(userSlug: $userSlug, pageIndex: 0, pageSize: 2000) {
        ascents {
          id
          routeName
          cragName
          sectorName
          difficulty
          date
          type
          flag
          comment
          rating
        }
      }
    }
    """
  headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
  try:
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"userSlug": user_slug}},
        headers=headers,
    )
    if response.status_code == 200:
      data = response.json()
      return data.get("data", {}).get("ascents", {}).get("ascents", [])
    else:
      print(f"Errore HTTP: {response.status_code}")
      return []
  except Exception as e:
    print(f"Errore durante la richiesta: {e}")
    return []


if __name__ == "__main__":
  os.makedirs("data", exist_ok=True)
  ascents = fetch_8anu_ascents(USER_SLUG)

  print(f"Trovate {len(ascents)} ascensioni per lo user '{USER_SLUG}'")

  # Forziamo la creazione del file JSON per garantire il commit su Git
  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(ascents, f, ensure_ascii=False, indent=2)

  print(f"File creato con successo in {OUTPUT_FILE}")
