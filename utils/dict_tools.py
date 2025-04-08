from collections.abc import Mapping

def deep_update(results: dict, new_data: dict):
    for key, value in new_data.items():
        if isinstance(value, list):
            if key not in results or not isinstance(results[key], list):
                results[key] = []
            results[key].extend(v for v in value if v not in results[key])
        elif isinstance(value, Mapping):
            if key not in results or not isinstance(results[key], dict):
                results[key] = {}
            deep_update(results[key], value)
        else:
            results[key] = value
    
def filter_unknown_fields(data: dict) -> dict:
    invalid_values = {"unknown", "none", "n/a", "na", "", "null"}

    def is_valid(value):
        if value is None:
            return False
        if isinstance(value, str) and value.strip().lower() in invalid_values:
            return False
        if isinstance(value, list):
            if not value:
                return False
            return any(is_valid(item) for item in value)
        return True

    return {k: v for k, v in data.items() if is_valid(v)}
