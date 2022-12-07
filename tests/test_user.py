import json

def test_create_user(client):
    payload = {
        "nama":"Tes User",
        "email": "umar@gmail.com",
        "password": "password",
    }
    response = client.post("/users/signup",json.dumps(payload))
    assert response.status_code == 200 
    assert response.json() == {"Pesan": "Akun berhasil dibuat."}

def test_get_users(client, normal_user_token_headers):
    response = client.get("/users/",  headers=normal_user_token_headers)
    assert response.json()[0]['nama'] == 'Tes User'
    assert response.status_code == 200

def test_get_a_user(client, normal_user_token_headers):
    response = client.get("/users/1",  headers=normal_user_token_headers)
    assert response.json()['nama'] == 'Tes User'
    assert response.status_code == 200

def test_get_user_health_condition(client, normal_user_token_headers):
    payload = {
        "jawaban_masalah_1": 0,
        "jawaban_masalah_2": 1,
        "jawaban_masalah_3": 0,
        "jawaban_masalah_4": 2,
        "jawaban_masalah_5": 0,
        "jawaban_masalah_6": 3,
        "jawaban_masalah_7": 0,
        "jawaban_masalah_8": 1,
        "jawaban_masalah_9": 2
    }

    response = client.put("/users/mental-health-condition-and-personality-prediction", json=payload,headers=normal_user_token_headers)
    assert response.json()['diagnosis'] == 'Normal'
    assert response.json()['severity'] == 'Mild'
    assert response.status_code == 200
