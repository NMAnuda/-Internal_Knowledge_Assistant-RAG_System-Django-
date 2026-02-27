from accounts.models import Role

ROLE_DEPARTMENT_ACCESS = {
    "employee": ["IT", "GENERAL","HR"],
    "hr": ["HR","IT"],
    "manager": ["HR", "FINANCE", "IT"],
    "admin": ["HR", "FINANCE", "IT", "GENERAL"]
}

def has_access(user_role, department):
    # Try to get from Role model first
    try:
        role_obj = Role.objects.get(name=user_role)
        allowed = role_obj.allowed_departments
    except Role.DoesNotExist:
        # Fallback to hardcoded mapping
        allowed = ROLE_DEPARTMENT_ACCESS.get(user_role.lower(), [])
    
    print("allowd", allowed)
    return department.upper() in allowed
