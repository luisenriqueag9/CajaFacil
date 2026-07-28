import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Union

from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.domain.exceptions import CompraYaExisteException
from app.modules.compra.application.ports.unit_of_work import UnitOfWork
from app.modules.compra.application.commands.registrar_compra_command import RegistrarCompraCommand
from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.compra_dto_mapper import CompraDTOMapper
from app.common.event_dispatcher import EventDispatcher

class RegistrarCompraUseCase:
    """
    Caso de uso para registrar y confirmar una compra.
    Orquesta el flujo, interactua con el repositorio y el Unit of Work, 
    y despacha los eventos resultantes del agregado.
    """
    def __init__(
        self, 
        repository: CompraRepository, 
        uow: UnitOfWork,
        supplier_lookup: any = None,
        product_lookup: any = None,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        
        # Adapt session-like object to UnitOfWork if passed
        if not isinstance(uow, UnitOfWork):
            class SessionUnitOfWork(UnitOfWork):
                def __init__(self, session):
                    self.session = session
                def __enter__(self) -> "SessionUnitOfWork":
                    self.session.begin_nested()
                    return self
                def __exit__(self, exc_type, exc_val, exc_tb) -> None:
                    if exc_type is not None:
                        self.session.rollback()
                    else:
                        self.session.commit()
                def begin(self) -> None:
                    self.session.begin_nested()
                def commit(self) -> None:
                    self.session.commit()
                def rollback(self) -> None:
                    self.session.rollback()
            self.uow = SessionUnitOfWork(uow)
        else:
            self.uow = uow
        
        self.event_dispatcher = event_dispatcher

    def execute(self, command: RegistrarCompraCommand) -> CompraDTO:
        # 1. Validar numero de factura duplicado
        existing = self.repository.get_by_invoice_number(
            command.company_id, 
            command.supplier_id, 
            command.invoice_number
        )
        if existing is not None:
            raise CompraYaExisteException(command.invoice_number, command.supplier_id)

        # 2. Construir el agregado Compra en estado REGISTRADA
        purchase_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        
        items_payload = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost
            }
            for item in command.items
        ]

        compra = Compra.register(
            id=purchase_id,
            company_id=command.company_id,
            supplier_id=command.supplier_id,
            invoice_number=command.invoice_number,
            payment_condition=command.payment_condition,
            issue_date=command.issue_date,
            created_at=now,
            updated_at=now,
            items_payload=items_payload
        )

        # 3. Transaccion y persitencia (Unit of Work)
        try:
            with self.uow:
                created_purchase = self.repository.create(compra)

                # Despachar eventos acumulados en el agregado
                for event in compra.eventos:
                    if self.event_dispatcher:
                        self.event_dispatcher.dispatch(event)
                compra.limpiar_eventos()
            
            return CompraDTOMapper.to_dto(created_purchase)
        except Exception as e:
            raise e
