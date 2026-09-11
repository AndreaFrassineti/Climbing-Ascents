import json
import os
import requests

USER_SLUG = "andrea-frassineti"  # Sostituisci con il tuo username 8a.nu
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
  response = requests.post(
      GRAPHQL_URL,
      json={"query": query, "variables": {"userSlug": user_slug}},
      headers=headers,
  )

  if response.status_code == 200:
    data = response.json()
    return data.get("data", {}).get("ascents", {}).get("ascents", [])
  else:
    print(f"Errore nel recupero dati: {response.status_code}")
    return []


if __name__ == "__main__":
  os.makedirs("data", exist_ok=True)
  ascents = fetch_8anu_ascents(USER_SLUG)
  if ascents:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      json.dump(ascents, f, ensure_ascii=False, indent=2)
    print(
        f"Sincronizzazione completata: {len(ascents)} ascensioni salvate in"
        f" {OUTPUT_FILE}"
    )
