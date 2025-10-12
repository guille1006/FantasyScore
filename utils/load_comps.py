import yaml
from rootutils import find_root

def load_comps() -> dict:
    """
    Esta función sirve para sacar un diccionario desde el archivo .yaml (muy similar a un JSON)
    """
    with open(find_root(indicator=[".git"]) / "utils" / "comps.yaml", "r") as f:
        comps = yaml.safe_load(f)
    return comps


def get_module_comps(module: str) -> dict:
    """
    Nos devuelve el diccionario anterior pero filtrando con el modulo especificado
    """
    if not isinstance(module, str):
        raise TypeError("'module' must be a string")
    comps = load_comps()
    module_comps = dict((k, v) for k, v in comps.items() if module in v)

    if not module_comps:
        raise ValueError("'module' doesnt exist")
    
    return module_comps