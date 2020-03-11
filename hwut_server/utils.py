from hwut_server.decorators import check_authentication, authenticate

FILE_STORAGE = './file_storage'

def dict_list_extended_if_authentication(r, l):
    if r.args.get('extended') == '1':
        if not r.authorization or \
                not check_authentication(r.authorization.username, r.authorization.password):
            return authenticate()
        return [b.to_dict_long() for b in l]
    else:
        return [b.to_dict_short() for b in l]
