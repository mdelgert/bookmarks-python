# Bookmarks API Examples

This file demonstrates how to use the new REST API endpoints with JSON.

## Base URL
```
http://localhost:8000/api/bookmarks
```

## API Documentation
FastAPI automatically generates interactive API docs at:
- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc

## Examples

### 1. Get All Bookmarks
```bash
curl -X GET "http://localhost:8000/api/bookmarks" \
  -H "Content-Type: application/json"
```

### 2. Get Bookmarks with Pagination  
```bash
curl -X GET "http://localhost:8000/api/bookmarks?skip=0&limit=10" \
  -H "Content-Type: application/json"
```

### 3. Search Bookmarks
```bash  
curl -X GET "http://localhost:8000/api/bookmarks?q=github" \
  -H "Content-Type: application/json"
```

### 4. Get Single Bookmark
```bash
curl -X GET "http://localhost:8000/api/bookmarks/1" \
  -H "Content-Type: application/json"
```

### 5. Create New Bookmark
```bash
curl -X POST "http://localhost:8000/api/bookmarks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "GitHub",
    "url": "https://github.com",
    "description": "Code hosting platform", 
    "category": "development",
    "icon_type": "si",
    "icon_value": "github",
    "is_active": true
  }'
```

### 6. Update Bookmark
```bash
curl -X PUT "http://localhost:8000/api/bookmarks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "GitHub - Updated",
    "url": "https://github.com", 
    "description": "The world's leading code hosting platform",
    "category": "development", 
    "icon_type": "si",
    "icon_value": "github",
    "is_active": true
  }'
```

### 7. Delete Bookmark
```bash
curl -X DELETE "http://localhost:8000/api/bookmarks/1" \
  -H "Content-Type: application/json"
```

### 8. Health Check
```bash
curl -X GET "http://localhost:8000/api/bookmarks/health" \
  -H "Content-Type: application/json"
```

## Response Examples

### Get Bookmarks Response
```json
[
  {
    "id": 1,
    "title": "GitHub",
    "url": "https://github.com",
    "description": "Code hosting platform",
    "category": "development", 
    "icon_type": "si",
    "icon_value": "github",
    "is_active": true,
    "created_at": "2024-03-18T10:30:00Z",
    "updated_at": "2024-03-18T10:30:00Z"
  }
]
```

### Error Response
```json
{
  "detail": "Bookmark not found"
}
```

## Python Client Example

```python
import requests
import json

base_url = "http://localhost:8000/api/bookmarks"

# Create a new bookmark
bookmark_data = {
    "title": "FastAPI Docs", 
    "url": "https://fastapi.tiangolo.com",
    "description": "FastAPI documentation",
    "category": "documentation",
    "icon_type": "mdi",
    "icon_value": "file-document",
    "is_active": True
}

response = requests.post(base_url, json=bookmark_data)
if response.status_code == 201:
    created_bookmark = response.json()
    print(f"Created bookmark: {created_bookmark['title']} (ID: {created_bookmark['id']})")
    
    # Update the bookmark
    created_bookmark['description'] = "Official FastAPI documentation site"
    update_response = requests.put(f"{base_url}/{created_bookmark['id']}", json=created_bookmark)
    
    if update_response.status_code == 200:
        print("Bookmark updated successfully")
    
    # Get all bookmarks
    all_bookmarks = requests.get(base_url).json()
    print(f"Total bookmarks: {len(all_bookmarks)}")
    
    # Search bookmarks
    search_results = requests.get(f"{base_url}?q=fastapi").json()
    print(f"Search results for 'fastapi': {len(search_results)}")
else:
    print(f"Error: {response.status_code} - {response.json()}")
```

## JavaScript/Fetch Example

```javascript
const baseUrl = 'http://localhost:8000/api/bookmarks';

// Create bookmark
const createBookmark = async (bookmarkData) => {
  try {
    const response = await fetch(baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookmarkData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating bookmark:', error);
    throw error;
  }
};

// Usage
const newBookmark = await createBookmark({
  title: 'Vue.js',
  url: 'https://vuejs.org',
  description: 'The Progressive JavaScript Framework',
  category: 'frontend',
  icon_type: 'si',
  icon_value: 'vuedotjs',
  is_active: true
});
```