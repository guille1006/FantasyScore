def get_fields(data, fields):
    """
    Función destinada a poder filtrar en el JSON todos los campos deseados
    - Si usamos un str, nos devolverá todos los key-values para ese key
    - Si usamos un dict, podremos filtrar mediante una lista de str o dict 
      los elementos que deseemos usar
        - Si volvemos a usar un str nos devolverá todo
        - Si volvemos a usar un dict podremos volver a filtrar
    """
    sol = dict()

    for field in fields:
        if isinstance(field, str):
            sol.update(get_fields_str(data, field))
        
        elif isinstance(field, dict):
            sol.update(get_fields_dict(data, field))
    return sol

def get_fields_str(data, field):
    info = {field: data.get(field, {})}
    return info

def get_fields_dict(data, field):
    info = dict()
    for key, values in field.items():
        for value in values:
            if isinstance(value, str):
                info.update(get_fields_str(data[key], value))

            elif isinstance(value, dict):
                info.update(get_fields_dict(data[key], value))
        
    info_all = {key: info}
    return info_all
