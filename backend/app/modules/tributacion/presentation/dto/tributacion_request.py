from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class TasaInputSchema(BaseModel):
    name: str = Field(..., description="Nombre de la tasa impositiva (ej: IVA General)")
    code: str = Field(..., description="Código único de la tasa (ej: IVA_GENERAL)")
    rate_percentage: Decimal = Field(..., description="Porcentaje impositivo (ej: 15.00)")


class CrearConfiguracionRequest(BaseModel):
    name: str = Field(..., description="Nombre descriptivo de la versión fiscal")
    calculation_type: str = Field("ADICIONADO", description="INCLUIDO, ADICIONADO")
    rates: list[TasaInputSchema] = Field(default_factory=list, description="Lista de tasas impositivas")


class ItemCotizacionSchema(BaseModel):
    price: Decimal = Field(..., description="Precio del artículo")
    quantity: Decimal = Field(..., description="Cantidad de unidades")
    tax_category: str = Field(..., description="Clasificación fiscal (EXENTO, TASA_GENERAL, TASA_ESPECIAL)")


class CotizarItemsRequest(BaseModel):
    items: list[ItemCotizacionSchema] = Field(..., description="Lista de artículos a calcular")
