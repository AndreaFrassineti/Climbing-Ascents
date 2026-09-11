import json
import os
import requests

USER_SLUG = "andrea-frassineti"
OUTPUT_FILE = "data/ascents.json"
GRAPHQL_URL = "https://www.8a.nu/api/graphql"


def fetch_ascents_by_category(user_slug, category):
  query = """
    query GetAscents($userSlug: String!, $category: String) {
      ascents(userSlug: $userSlug, category: $category, pageIndex: 0, pageSize: 1000) {
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
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      ),
      "Content-Type": "application/json",
  }
  payload = {
      "query": query,
      "variables": {"userSlug": user_slug, "category": category},
  }

  try:
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    if response.status_code == 200:
      res_data = response.json()
      if "errors" in res_data:
        print(
            f"Errore GraphQL per la categoria '{category}':"
            f" {res_data['errors']}"
        )
        return []
      data_field = res_data.get("data", {}).get("ascents")
      if data_field and "ascents" in data_field:
        return data_field["ascents"] or []
    else:
      print(
          f"Errore HTTP {response.status_code} durante il recupero di"
          f" '{category}'"
      )
  except Exception as e:
    print(f"Eccezione durante la richiesta per '{category}': {e}")

  return []


if __name__ == "__main__":
  os.makedirs("data", exist_ok=True)

  all_ascents = []

  # Recupera separatamente le vie da falesia e i blocchi da boulder
  for category in ["sportclimbing", "bouldering"]:
    ascents = fetch_ascents_by_category(USER_SLUG, category)
    print(f"Trovate {len(ascents)} ascensioni per '{category}'")
    all_ascents.extend(ascents)

  print(f"Totale ascensioni recuperate: {len(all_ascents)}")

  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_ascents, f, ensure_ascii=False, indent=2)

  print(f"File salvato correttamente in {OUTPUT_FILE}")
