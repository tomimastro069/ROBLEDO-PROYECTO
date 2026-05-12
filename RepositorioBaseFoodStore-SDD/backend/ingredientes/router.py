from typing import List
from fastapi import APIRouter, Depends, status

from ingredientes.schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead
from ingredientes.service import IngredientesService
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from auth.dependencies import require_role
from auth.roles import Role
from auth.schemas import TokenData

router = APIRouter()

_WRITE_ROLES = (Role.ADMIN, Role.GESTOR_STOCK)


def get_service(uow: AppUnitOfWork = Depends(get_uow)) -> IngredientesService:
    return IngredientesService(uow)


# ── Catálogo global ───────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=List[IngredienteRead],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los ingredientes",
)
def list_ingredientes(service: IngredientesService = Depends(get_service)):
    return service.get_all()


@router.get(
    "/{ingrediente_id}",
    response_model=IngredienteRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener ingrediente por ID",
)
def get_ingrediente(ingrediente_id: int, service: IngredientesService = Depends(get_service)):
    return service.get_by_id(ingrediente_id)


@router.post(
    "",
    response_model=IngredienteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ingrediente",
)
def create_ingrediente(
    data: IngredienteCreate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: IngredientesService = Depends(get_service),
):
    return service.create(data)


@router.put(
    "/{ingrediente_id}",
    response_model=IngredienteRead,
    status_code=status.HTTP_200_OK,
    summary="Editar ingrediente",
)
def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: IngredientesService = Depends(get_service),
):
    return service.update(ingrediente_id, data)


@router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ingrediente (soft delete)",
)
def delete_ingrediente(
    ingrediente_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: IngredientesService = Depends(get_service),
):
    service.delete(ingrediente_id)


# ── Asociación con productos ──────────────────────────────────────────────────

@router.get(
    "/producto/{product_id}",
    response_model=List[IngredienteRead],
    status_code=status.HTTP_200_OK,
    summary="Listar ingredientes de un producto",
)
def get_ingredientes_de_producto(
    product_id: int,
    service: IngredientesService = Depends(get_service),
):
    return service.get_por_producto(product_id)


@router.post(
    "/{ingrediente_id}/producto/{product_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Asociar ingrediente a producto",
)
def asociar_ingrediente(
    ingrediente_id: int,
    product_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: IngredientesService = Depends(get_service),
):
    service.asociar_a_producto(product_id, ingrediente_id)
    return {"detail": "Ingrediente asociado correctamente."}


@router.delete(
    "/{ingrediente_id}/producto/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desasociar ingrediente de producto",
)
def desasociar_ingrediente(
    ingrediente_id: int,
    product_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: IngredientesService = Depends(get_service),
):
    service.desasociar_de_producto(product_id, ingrediente_id)
