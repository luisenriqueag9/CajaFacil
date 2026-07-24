from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional, Dict, Any
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria, DesgloseImpuesto

class MotorTributario:
    """
    Domain Service (Servicio de Dominio) responsible for executing stateless tax calculations
    on transaction items based on the active Tax Configuration of the tenant.
    """
    def calcular(
        self, 
        items: List[Dict[str, Any]], 
        configuracion: Optional[ConfiguracionTributaria]
    ) -> List[DesgloseImpuesto]:
        """
        Calculates tax breakdowns grouped by tax rate code.
        Each item in items must have:
            - 'price': Decimal (unit price)
            - 'quantity': Decimal
            - 'tax_category': str (e.g. 'TASA_GENERAL', 'EXENTO', 'TASA_ESPECIAL')
        """
        if not configuracion or not configuracion.is_active:
            # Fallback when no active tax config exists (Monotributo / No taxes mode)
            # Group by category, but tax amount is strictly 0
            accumulated: Dict[str, Dict[str, Decimal]] = {}
            for item in items:
                cat = item.get("tax_category", "EXENTO")
                price = Decimal(str(item["price"]))
                qty = Decimal(str(item["quantity"]))
                total = price * qty
                
                if cat not in accumulated:
                    accumulated[cat] = {"net": Decimal("0.0000"), "tax": Decimal("0.0000"), "percentage": Decimal("0.0000")}
                accumulated[cat]["net"] += total

            return [
                DesgloseImpuesto(
                    rate_code=code,
                    rate_percentage=vals["percentage"],
                    net_amount=vals["net"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    tax_amount=vals["tax"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                ) for code, vals in accumulated.items()
            ]

        # Standard calculation using the provided active Configuration
        accumulated = {}
        # Pre-populate map of rates for quick lookup
        rates_map = {r.code: r.rate_percentage for r in configuracion.rates}

        for item in items:
            cat = item.get("tax_category", "EXENTO")
            # Map default categories to codes
            # e.g., 'TASA_GENERAL' -> 'IVA_GENERAL', 'EXENTO' -> 'IVA_EXENTO', 'TASA_ESPECIAL' -> 'IVA_ESPECIAL'
            # If rate code matches cat directly or matches mapped values
            rate_code = cat
            if cat == "TASA_GENERAL" and "IVA_GENERAL" in rates_map:
                rate_code = "IVA_GENERAL"
            elif cat == "EXENTO" and "IVA_EXENTO" in rates_map:
                rate_code = "IVA_EXENTO"
            elif cat == "TASA_ESPECIAL" and "IVA_ESPECIAL" in rates_map:
                rate_code = "IVA_ESPECIAL"

            rate_pct = rates_map.get(rate_code, Decimal("0.0000"))
            price = Decimal(str(item["price"]))
            qty = Decimal(str(item["quantity"]))

            if configuracion.calculation_type == "ADICIONADO":
                # Price is Net. Tax is added on top.
                net_amount = price * qty
                tax_amount = net_amount * (rate_pct / Decimal("100.0"))
            else:
                # Price is final (includes tax). Deduct tax to find net.
                total_final = price * qty
                net_amount = total_final / (Decimal("1.0") + (rate_pct / Decimal("100.0")))
                tax_amount = total_final - net_amount

            if rate_code not in accumulated:
                accumulated[rate_code] = {"net": Decimal("0.0000"), "tax": Decimal("0.0000"), "percentage": rate_pct}
            accumulated[rate_code]["net"] += net_amount
            accumulated[rate_code]["tax"] += tax_amount

        # Round results to 2 decimals for presentation/accounting
        return [
            DesgloseImpuesto(
                rate_code=code,
                rate_percentage=vals["percentage"],
                net_amount=vals["net"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                tax_amount=vals["tax"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            ) for code, vals in accumulated.items()
        ]
