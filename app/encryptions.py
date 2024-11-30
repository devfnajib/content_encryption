import json
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from app.exceptions import InvalidEncryptionMode, DecryptionException


ENCRYPTION_MODE_CODES = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'OFB': AES.MODE_OFB,
    'CTR': AES.MODE_CTR,
    'OPENPGP': AES.MODE_OPENPGP,
    'CCM': AES.MODE_CCM,
    'EAX': AES.MODE_EAX,
    'SIV': AES.MODE_SIV,
    'GCM': AES.MODE_GCM,
    'OCB': AES.MODE_OCB
}


def validate_input(encryption_mode):
    if '+' not in encryption_mode:
        raise InvalidEncryptionMode(encryption_mode=encryption_mode, mode_values=list(ENCRYPTION_MODE_CODES.keys()))

    encryption_mode_parts = encryption_mode.split('+')
    if not encryption_mode_parts[0].strip().lower() == 'aes':
        raise InvalidEncryptionMode(encryption_mode=encryption_mode, mode_values=list(ENCRYPTION_MODE_CODES.keys()))
    if not ENCRYPTION_MODE_CODES.keys().__contains__(encryption_mode_parts[1].strip().upper()):
        raise InvalidEncryptionMode(encryption_mode=encryption_mode, mode_values=list(ENCRYPTION_MODE_CODES.keys()))

    return ENCRYPTION_MODE_CODES[encryption_mode_parts[1].strip().upper()]


def modern_encryption(content, encryption_mode, encryption_key):
    header = b'Hard coded header for now.'
    data = content.encode('utf-8')
    cipher = AES.new(encryption_key, encryption_mode)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))

    return result


def siv_encryption(content, encryption_mode, encryption_key):
    header = b'Hard coded header for now.'
    data = content.encode('utf-8')
    nonce = get_random_bytes(16)
    cipher = AES.new(encryption_key, encryption_mode, nonce=nonce)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))

    return result


def classic_encryption(content, encryption_mode, encryption_key):
    data = content.encode('utf-8')
    cipher = AES.new(encryption_key, encryption_mode)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv': iv, 'ciphertext': ct})

    return result


def openpgp_encryption(content, encryption_mode, encryption_key):
    data = content.encode('utf-8')
    cipher = AES.new(encryption_key, encryption_mode)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(ct_bytes[:AES.block_size + 2]).decode('utf-8')
    ct = b64encode(ct_bytes[AES.block_size + 2:]).decode('utf-8')
    result = json.dumps({'iv': iv, 'ciphertext': ct})

    return result


def ctr_encryption(content, encryption_mode, encryption_key):
    data = content.encode('utf-8')
    cipher = AES.new(encryption_key, encryption_mode)
    ct_bytes = cipher.encrypt(data)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'nonce': nonce, 'ciphertext': ct})

    return result


def ecb_encryption(content, encryption_mode, encryption_key):
    data = content.encode('utf-8')
    cipher = AES.new(encryption_key, encryption_mode)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'ciphertext': ct})

    return result


def encrypt(content, encryption_mode, encryption_key):
    if encryption_mode in [AES.MODE_CCM, AES.MODE_EAX, AES.MODE_GCM, AES.MODE_OCB]:
        return modern_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)
    elif encryption_mode == AES.MODE_SIV:
        return siv_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)
    elif encryption_mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB]:
        return classic_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)
    elif encryption_mode == AES.MODE_OPENPGP:
        return openpgp_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)
    elif encryption_mode == AES.MODE_CTR:
        return ctr_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)
    elif encryption_mode == AES.MODE_ECB:
        return ecb_encryption(content=content, encryption_mode=encryption_mode, encryption_key=encryption_key)


def modern_decryption(encryption_key, encryption_mode, encryption_payload):
    try:
        b64 = json.loads(encryption_payload)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}

        cipher = AES.new(encryption_key, encryption_mode, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        return plaintext.decode('utf-8')
    except (ValueError, KeyError):
        raise Exception('Unable to decrypt.')


def siv_decryption(encryption_key, encryption_mode, encryption_payload):
    try:
        b64 = json.loads(encryption_payload)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, encryption_mode, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])

        return plaintext.decode('utf-8')
    except (ValueError, KeyError):
        raise Exception('Unable to decrypt.')


def classic_decryption(encryption_key, encryption_mode, encryption_payload):
    try:
        b64 = json.loads(encryption_payload)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(encryption_key, encryption_mode, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except (ValueError, KeyError):
        raise Exception('Unable to decrypt.')


def ctr_decryption(encryption_key, encryption_mode, encryption_payload):
    try:
        b64 = json.loads(encryption_payload)
        nonce = b64decode(b64['nonce'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(encryption_key, encryption_mode, nonce=nonce)
        pt = cipher.decrypt(ct)
        return pt.decode('utf-8')
    except (ValueError, KeyError):
        raise Exception('Unable to decrypt.')


def ecb_decryption(encryption_key, encryption_mode, encryption_payload):
    try:
        b64 = json.loads(encryption_payload)
        ciphertext = b64decode(b64['ciphertext'])
        decipher = AES.new(encryption_key, encryption_mode)
        msg_dec = decipher.decrypt(ciphertext)
        return unpad(msg_dec, AES.block_size).decode('utf-8')
    except (ValueError, KeyError):
        raise Exception('Unable to decrypt.')


def decrypt(encryption_key, encryption_mode, encryption_payload):
    if encryption_mode in [AES.MODE_CCM, AES.MODE_EAX, AES.MODE_GCM, AES.MODE_OCB]:
        return modern_decryption(encryption_key=encryption_key, encryption_mode=encryption_mode,
                                 encryption_payload=encryption_payload)
    elif encryption_mode == AES.MODE_SIV:
        return siv_decryption(encryption_key=encryption_key, encryption_mode=encryption_mode,
                              encryption_payload=encryption_payload)
    elif encryption_mode in [AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB, AES.MODE_OPENPGP]:
        return classic_decryption(encryption_key=encryption_key, encryption_mode=encryption_mode,
                                  encryption_payload=encryption_payload)
    elif encryption_mode == AES.MODE_CTR:
        return ctr_decryption(encryption_key=encryption_key, encryption_mode=encryption_mode,
                              encryption_payload=encryption_payload)
    elif encryption_mode == AES.MODE_ECB:
        return ecb_decryption(encryption_key=encryption_key, encryption_mode=encryption_mode,
                              encryption_payload=encryption_payload)


def generate_encryption_key(size=32):
    return get_random_bytes(size)
