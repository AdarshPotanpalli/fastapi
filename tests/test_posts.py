from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_get_all_posts(client):
    response = client.get("/posts")
    assert response.status_code == 401
    
def test_unauthorized_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get("/posts/8888")
    assert response.status_code == 404
    
def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(response.json())
    post = schemas.PostOut(**response.json()) # validate the response
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title ==  test_posts[0].title
    
#testing create post
@pytest.mark.parametrize("title, content, published", [
    ("first title", "wow new content", True),
    ("second title", "ohh shit again", False),
    ("final title", "we are done", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts", json= {"title": title, "content": content, "published": published})
    post = schemas.Post(**response.json()) # schema validation test
    
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']
    
def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post("/posts", json= {"title": "random title", "content": "random title"})
    post = schemas.Post(**response.json()) # schema validation test
    
    assert post.title == "random title"
    assert post.content == "random title"
    assert post.published == True
    assert post.owner_id == test_user['id']
    
def test_unauthorized_user_create_post(client, test_user):
    response = client.post("/posts", json= {"title": "random title", "content": "random title"})
    assert response.status_code == 401
    
## testing delete post
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_successful_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204
    
def test_delete_non_existent_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/8000000")
    assert response.status_code == 404
    
# testing delete a post of other user
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
## testing update posts
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404