from Crypto.Cipher import AES

from app.exceptions import InvalidEncryptionMode


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
