from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role
from uuid import UUID

app = FastAPI()

db: List[User] = [
    User(
        # nosotros teniamos como uuid4() lo cual autogeneraba una id cada vez que se recargaba la pagina
        id=UUID("d905ad5d-66a5-4bf4-9937-dc5c09e0a118"),
        first_name="Angela",
        last_name="DiMaria",
        gender=Gender.female,
        roles=[Role.student]
    ),

    User(
        # de esta forma el id queda fijado
        id=UUID("d18effb9-de0b-4680-b449-6f3e135a2765"),
        first_name="Lionel",
        last_name="Messi",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
def root():
    return{"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

    # NOTA IMPORTANTE SOBRE THUNDER:
    # Si al crear un nuevo request ponemos get y el http del host, nos va a enviar la misma info
    # Ahora, si queremos probar el post, volvemos a pegar la pagina pero en el body tenemos que pegar
    # todos los datos de uno de los users desde el firstname a roles que nos aparecen en {}, SIN ID
    # podemos modificar los datos porque este nuevo User va a ser agregado al database
    # una vez enviado, volvemos a chequear el get y nos deberia aparecer el nuevo usuario


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        reaise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exists"
        )
