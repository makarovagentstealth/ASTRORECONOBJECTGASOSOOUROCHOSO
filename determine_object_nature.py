import requests
import json

def search_adsabs(query, api_key):
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    params = {
        "q": query,
        "fl": "title,abstract",
        "rows": 10
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao acessar a API do ADS:", response.status_code)
        return None

def determine_nature_of_object(query, api_key):
    results = search_adsabs(query, api_key)
    
    if not results or "response" not in results or "docs" not in results["response"]:
        return "Dados insuficientes para determinar a natureza do objeto."
    
    docs = results["response"]["docs"]
    
    has_natural_satellites = False
    
    for doc in docs:
        title = doc.get("title", [])
        abstract = doc.get("abstract", [])
        
        # Se title e abstract forem listas, junte os elementos em uma string
        if isinstance(title, list):
            title = " ".join(title)
        if isinstance(abstract, list):
            abstract = " ".join(abstract)
        
        if "satellite" in title.lower() or "satellite" in abstract.lower():
            has_natural_satellites = True
            break
    
    if has_natural_satellites:
        return "O objeto provavelmente é um planeta gasoso."
    else:
        return "O objeto provavelmente é um planeta rochoso."

def main():
    # Carregar o payload do arquivo JSON
    with open('payload.json', 'r') as file:
        payload = json.load(file)
    
    # Obter o nome do objeto do payload
    object_name = payload.get('object_name')
    if not object_name:
        print("Nome do objeto astronômico não encontrado no payload.")
        return
    
    # Substitua pela sua chave de API
    api_key = "SUA CHAVE API AQUI"
    
    # Determinar a natureza do objeto
    nature = determine_nature_of_object(object_name, api_key)
    print(nature)

if __name__ == "__main__":
    main()
