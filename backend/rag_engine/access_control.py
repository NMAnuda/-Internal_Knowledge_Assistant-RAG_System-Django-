ROLE_DEPARTMENT_ACCESS = {
    "employee": ["IT", "GENERAL"],
    "hr": ["HR"],
    "manager": ["HR", "FINANCE", "IT"],
    "admin": ["HR", "FINANCE", "IT", "GENERAL"]
}

def has_access(role, department):
    allowed = ROLE_DEPARTMENT_ACCESS.get(role.lower(), [])
    print("allowd",allowed)
    return department.upper() in allowed
