import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def filter_titles_by_word_count(data, max_words=6):
    return [item for item in data if len(item['title'].split()) <= max_words]

def filter_body_by_line_count(data, max_lines=3):
    return [item for item in data if len(item['body'].split('\n')) <= max_lines]

def main():
    response = requests.get(f"{BASE_URL}/posts")
    if response.status_code == 200:
        posts = response.json()
        print("Original number of posts:", len(posts))
        filtered_by_title = filter_titles_by_word_count(posts)
        print("Posts with titles <= 6 words:", len(filtered_by_title))
        filtered_by_body = filter_body_by_line_count(posts)
        print("Posts with body <= 3 lines:", len(filtered_by_body))
    else:
        print("GET request failed:", response.status_code)

    new_post = {
        "title": "New post for testing",
        "body": "This is a test post body.",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    if response.status_code == 201:
        print("POST request successful. Created post:", response.json())
    else:
        print("POST request failed:", response.status_code)

    updated_post = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body content.",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/1", json=updated_post)
    if response.status_code == 200:
        print("PUT request successful. Updated post:", response.json())
    else:
        print("PUT request failed:", response.status_code)

    response = requests.delete(f"{BASE_URL}/posts/1")
    if response.status_code == 200:
        print("DELETE request successful.")
    else:
        print("DELETE request failed:", response.status_code)

if __name__ == "__main__":
    main()
