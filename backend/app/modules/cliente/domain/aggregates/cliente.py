import uuid
from datetime import datetime, timezone
from typing import Union, List, Any

from app.modules.cliente.domain.value_objects.nombre_cliente import NombreCliente
from app.modules.cliente.domain.value_objects.estado_cliente import EstadoCliente
from app.modules.cliente.domain.value_objects.email_cliente import EmailCliente
from app.modules.cliente.domain.exceptions.cliente_invalido_exception import ClienteInvalidoException

class Cliente:
    """
    Aggregate Root que representa a un Cliente dentro de la empresa.
    """
    def __init__(
        self,
        id: uuid.UUID,
        company_id: uuid.UUID,
        name: Union[NombreCliente, str],
        tax_id: str | None,
        phone: str | None,
        email: Union[EmailCliente, str, None],
        status: Union[EstadoCliente, str],
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.company_id = company_id
        
        # Hybrid coercion for constructors
        self.name = name if isinstance(name, NombreCliente) else NombreCliente(name)
        self.tax_id = tax_id.strip() if tax_id else None
        self.phone = phone.strip() if phone else None
        self.email = email if isinstance(email, EmailCliente) else EmailCliente(email)
        self.status = status if isinstance(status, EstadoCliente) else EstadoCliente(status)
        
        self.created_at = created_at
        self.updated_at = updated_at
        
        self._events: List[Any] = []
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.id, uuid.UUID):
            raise ClienteInvalidoException("El ID del cliente debe ser un UUID valido.")
        if not isinstance(self.company_id, uuid.UUID):
            raise ClienteInvalidoException("El ID de la empresa debe ser un UUID valido.")
        if not isinstance(self.created_at, datetime):
            raise ClienteInvalidoException("La fecha de creacion debe ser un objeto datetime valido.")

    @property
    def eventos(self) -> List[Any]:
        return self._events

    def registrar_evento(self, evento: Any) -> None:
        self._events.append(evento)

    def limpiar_eventos(self) -> None:
        self._events.clear()

    @classmethod
    def register(
        cls,
        id: uuid.UUID,
        company_id: uuid.UUID,
        name: str,
        tax_id: str | None,
        phone: str | None,
        email: str | None,
        created_at: datetime,
        updated_at: datetime
    ) -> "Cliente":
        """
        Factory method para registrar un nuevo cliente en estado ACTIVO.
        """
        cliente = cls(
            id=id,
            company_id=company_id,
            name=name,
            tax_id=tax_id,
            phone=phone,
            email=email,
            status=EstadoCliente.activo(),
            created_at=created_at,
            updated_at=updated_at
        )
        
        # Dispatch ClienteRegistrado event
        from app.modules.cliente.domain.events.cliente_events import ClienteRegistrado
        cliente.registrar_evento(
            ClienteRegistrado(
                client_id=cliente.id,
                company_id=cliente.company_id,
                name=cliente.name.valor,
                tax_id=cliente.tax_id,
                occurred_at=created_at
            )
        )
        return cliente

    def update_profile(
        self,
        name: str,
        tax_id: str | None,
        phone: str | None,
        email: str | None,
        timestamp: datetime
    ) -> None:
        """
        Actualiza el perfil del cliente.
        """
        self.name = NombreCliente(name)
        self.tax_id = tax_id.strip() if tax_id else None
        self.phone = phone.strip() if phone else None
        self.email = EmailCliente(email)
        self.updated_at = timestamp
        self.validate()

        # Dispatch ClienteActualizado event
        from app.modules.cliente.domain.events.cliente_events import ClienteActualizado
        self.registrar_evento(
            ClienteActualizado(
                client_id=self.id,
                company_id=self.company_id,
                name=self.name.valor,
                tax_id=self.tax_id,
                occurred_at=timestamp
            )
        )

    def deactivate(self, timestamp: datetime) -> None:
        """
        Inactiva comercialmente al cliente.
        """
        if self.status.is_inactivo:
            raise ClienteInvalidoException("El cliente ya se encuentra inactivo.")
            
        self.status = EstadoCliente.inactivo()
        self.updated_at = timestamp
        self.validate()

        # Dispatch ClienteInactivado event
        from app.modules.cliente.domain.events.cliente_events import ClienteInactivado
        self.registrar_evento(
            ClienteInactivado(
                client_id=self.id,
                company_id=self.company_id,
                occurred_at=timestamp
            )
        )
