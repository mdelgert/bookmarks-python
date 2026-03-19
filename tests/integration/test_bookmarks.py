def test_create_and_list_bookmarks(client):
    response = client.post(
        "/bookmarks",
        json={"title": "GitHub", "url": "https://github.com", "notes": "code"},
    )
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == "GitHub"

    list_response = client.get("/bookmarks")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["url"] == "https://github.com"
