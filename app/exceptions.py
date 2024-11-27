class InvalidEncryptionMode(Exception):
    def __init__(self, encryption_mode=None, mode_values=None):
        self.encryption_mode = encryption_mode
        self.mode_values = mode_values

    def __str__(self):
        return ('"{}" is not a valid value. A valid must follow format "AES + <MODE>", where <MODE> can be have any '
                'one of the following values: {}').format(self.encryption_mode, self.mode_values)

    def get_error(self):
        return {
            'status': 'Error',
            'message': self.__str__()
        }


class DecryptionException(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message

    def get_error(self):
        return {
            'status': 'Error',
            'message': self.__str__()
        }
