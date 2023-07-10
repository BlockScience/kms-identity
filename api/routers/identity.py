from fastapi import APIRouter

router = APIRouter(
    prefix="/identity"
)

@router.post("")
def create_identity():
    ...

"""
API paths

POST    /identity
GET     /identity/{id}
PUT     /identity/{id}
DELETE  /identity/{id}

        /identity/members
        /identity/{id}/group

"""