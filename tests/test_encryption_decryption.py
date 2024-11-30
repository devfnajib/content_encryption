from Crypto.Cipher import AES

from app.encryptions import generate_encryption_key, encrypt, decrypt


def test_ecb():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_ECB, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_ECB,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_cbc():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_CBC, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_CBC,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_cfb():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_CFB, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_CFB,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_ofb():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_OFB, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_OFB,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_ctr():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_CTR, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_CTR,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_openpgp():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_OPENPGP, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_OPENPGP,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_ccm():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_CCM, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_CCM,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_eax():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_EAX, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_EAX,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_siv():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_SIV, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_SIV,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_gcm():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_GCM, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_GCM,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content


def test_ocb():
    content = 'This is sample content for testing.'
    encryption_key = generate_encryption_key(32)
    encrypted_payload = encrypt(content=content, encryption_mode=AES.MODE_OCB, encryption_key=encryption_key)
    assert isinstance(encrypted_payload, str)

    decrypted_content = decrypt(encryption_key=encryption_key, encryption_mode=AES.MODE_OCB,
                                encryption_payload=encrypted_payload)
    assert decrypted_content == content
