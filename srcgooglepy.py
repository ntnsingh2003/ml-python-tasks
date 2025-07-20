from googlesearch import search

def google_search(query, num_results=5):
    print(f"🔍 Top {num_results} Google search results for: '{query}'\n")
    results = search(query, num_results=num_results, advanced=True)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Snippet: {result.description}\n")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    google_search(query, num_results=5)
