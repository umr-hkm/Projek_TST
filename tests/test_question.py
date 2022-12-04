import json

def test_create_questions(client, normal_user_token_headers):
    payload = {
        "masalah": "Kurang berminat atau bergairah dalam melakukan apapun",
        "pilihan": "0 (Tidak Pernah), 1 (Beberapa Hari), 2 (Lebih Dari 1 Minggu), 3 (Hampir Setiap Hari)"
    }
    response = client.post("/questions/create", json=payload,  headers=normal_user_token_headers)
    assert response.status_code == 200 
    assert response.json() == {"Pesan": "Masalah berhasil ditambahkan."}

def test_get_questions(client, normal_user_token_headers):
    response = client.get("/questions/",  headers=normal_user_token_headers)
    assert response.json()[0]['masalah'] == 'Kurang berminat atau bergairah dalam melakukan apapun'
    assert response.status_code == 200

def test_get_a_question(client, normal_user_token_headers):
    response = client.get("/questions/1",  headers=normal_user_token_headers)
    assert response.json()['masalah'] == 'Kurang berminat atau bergairah dalam melakukan apapun'
    assert response.status_code == 200

def test_update_a_question(client, normal_user_token_headers):
    payload = {
        "masalah": "Kurang berminat atau bergairah dalam melakukan apapun.",
        "pilihan": "0 (Tidak Pernah), 1 (Beberapa Hari), 2 (Lebih Dari 1 Minggu), 3 (Hampir Setiap Hari)"
    }

    response = client.put("questions/update/1", json=payload, headers=normal_user_token_headers)
    assert response.json() == {"Pesan": "Masalah berhasil diperbarui."}
    assert response.status_code == 200

def test_delete_a_question(client, normal_user_token_headers):
    response = client.delete("questions/delete/1", headers=normal_user_token_headers)
    assert response.json() == {"Pesan": "Masalah berhasil dihapus."}

    assert response.status_code == 200