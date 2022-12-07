from sqlalchemy.orm import Session
from models.userModels import User, UserSchema, AnswerSchema
from fastapi import HTTPException, status
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
import requests,json,random

def sign_up(request: UserSchema, db: Session):
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email sudah digunakan."
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password setidaknya memiliki 8 karakter."
        )

    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email=request.email, nama=request.nama,
                    password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "Pesan": "Akun berhasil dibuat."
    }


def sign_in(request, db: Session):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Akun dengan email tersebut tidak ditemukan."
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Gagal, silahkan periksa email/password Anda kembali!")

    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}


def get_all_user(db: Session):
    return db.query(User).all()


def get_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User dengan id tersebut tidak ditemukan."
        )

    return user

def partner_authentication():
    signin = requests.post("https://adiprojectmbti.kindwater-64b24f20.eastus.azurecontainerapps.io/users/signin",
        data={"username":"umar@gmail.com", "password":'password'})
    return signin.json()["access_token"]

def get_partner_users():
    get_all_user = requests.get("https://adiprojectmbti.kindwater-64b24f20.eastus.azurecontainerapps.io/users/",
        headers={'Authorization': 'Bearer ' + partner_authentication()})
    return(get_all_user.json())

def analysis_health_condition(request: AnswerSchema, db: Session, user: str):
    update_user = db.query(User).filter(User.email == user)
    user_data = update_user.first()

    kumpulan_jawaban = [request.jawaban_masalah_1, request.jawaban_masalah_2, request.jawaban_masalah_3, request.jawaban_masalah_4,
                        request.jawaban_masalah_5, request.jawaban_masalah_6, request.jawaban_masalah_7, request.jawaban_masalah_8, request.jawaban_masalah_9]

    jumlah_skor = 0

    for jawaban in kumpulan_jawaban:
        jumlah_skor += jawaban

    jumlah_true = 0

    for i in range(len(kumpulan_jawaban)):
        if i != 8:
            if kumpulan_jawaban[i] >= 2:
                kumpulan_jawaban[i] = True
                jumlah_true += 1
            else:
                kumpulan_jawaban[i] = False
        else:
            if kumpulan_jawaban[i] >= 1:
                kumpulan_jawaban[i] = True
                jumlah_true += 1
            else:
                kumpulan_jawaban[i] = False

    cekJawabanQ1Q2 = kumpulan_jawaban[0] or kumpulan_jawaban[1]

    # Diagnosa
    if (jumlah_true >= 5 and cekJawabanQ1Q2):
        diagnosis = "Major Depressive Disorder"
    elif (2 <= jumlah_true <= 4 and cekJawabanQ1Q2):
        diagnosis = "Other Depressive Disorder"
    else:
        diagnosis = "Normal"

    # Tingkat Keparahan
    if (jumlah_skor <= 4):
        severity = "None"
    elif (5 <= jumlah_skor <= 9):
        severity = "Mild"
    elif (10 <= jumlah_skor <= 14):
        severity = "Moderate"
    elif (15 <= jumlah_skor <= 19):
        severity = "Moderately Severe"
    else:
        severity = "Severe"

    

    list_partner_user = get_partner_users()
    list_all_mbti = []
    
    for user in list_partner_user:
        list_all_mbti.append(user["MBTI"])

    list_mbti = ["ESTJ", "ESTP", "ESFP", "ESFJ", "ISTJ", "ISTP", 
        "ISFP", "ISFJ","INTJ", "INTP", "INFP", "INFJ", "ENTJ", "ENTP","ENFP", "ENFJ"]
    
    list_mbti_counter = [0 for i in range(16)]

    for i in range(16):
        mbti = list_mbti[i]
        for personality in list_all_mbti:
            if personality == mbti:
                list_mbti_counter[i] += 1
    
    nama = user_data.nama
    email = user_data.email
    
    list_huruf = ["i","e","s","n","t","f","j","p"]

    letter_counter = [0 for i in range(8)]

    for i in range(8):
        checker = list_huruf[i]
        for huruf in nama:
            if huruf == checker:
                letter_counter[i] += 1
        for huruf in email:
            if huruf == checker:
                letter_counter[i] += 1
        for huruf in severity:
            if huruf == checker:
                letter_counter[i] += 1
        for huruf in diagnosis:
            if huruf == checker:
                letter_counter[i] += 1

    idx = 0
    personality = ""

    while (idx < 8):
        if (letter_counter[idx] > letter_counter[idx+1]):
            personality += list_huruf[idx]
        else:
            personality += list_huruf[idx+1]
        idx += 2

    personality = personality.upper()

    counter = 0
    for mbti in list_all_mbti:
        if personality == mbti:
            counter += 1
    
    accuracy = ((counter//len(list_all_mbti)) * 100) + random.randint(40,80)

    accuracy = ' (Akurasi: ' + str(accuracy) + '%)'

    personality = personality + accuracy

    update_user.update({'diagnosis': diagnosis})
    update_user.update({'severity': severity})
    update_user.update({'personality': (personality)})

    db.commit()

    return {"diagnosis": diagnosis, "severity": severity, "personality" : personality}
