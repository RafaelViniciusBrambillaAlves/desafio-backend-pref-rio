from fastapi.security import HTTPBearer

bearer_schemas = HTTPBearer(
    scheme_name = "BearerAuth", 
    bearerFormat = "JWT"
) 