import json
import os
from uuid import uuid4


def read_files():
    files = os.listdir("./data")
    return files


def add_article(data):
    data["id"] = str(uuid4())
    try:
        with open(f"./data/{data['id']}.json", "w") as file:
            json.dump(data, file, indent=4)
        return f"Article with id {data["id"]} created successfully"
    except Exception as e:
        return f"Error creating article: {str(e)}"


def get_all():
    data = []
    files = read_files()
    for file in files:
        with open(f"./data/{file}", "r") as file:
            data.append(json.load(file))
    return data


def get_by_id(article_id: str):
    if not article_id.endswith(".json"):
        article_id = article_id + ".json"

    if not os.path.exists(f"./data/{article_id}"):
        return None

    with open(f"./data/{article_id}", "r") as file:
        return json.load(file)


def update_article(article_id: str, updated_data):
    print("Hello World")
    if not article_id.endswith(".json"):
        article_id = article_id + ".json"

    if not os.path.exists(f"./data/{article_id}"):
        raise FileNotFoundError("Article not found")

    with open(f"./data/{article_id}", "w") as file:
        json.dump(updated_data, file, indent=4)


def delete_article(article_id):
    article = get_by_id(article_id)
    if article is None:
        raise FileNotFoundError(f"Article not found. (ID: {article_id})")

    try:
        os.remove(f"./data/{article_id}.json")
    except Exception as e:
        raise f"Error deleting article: {str(e)}"
