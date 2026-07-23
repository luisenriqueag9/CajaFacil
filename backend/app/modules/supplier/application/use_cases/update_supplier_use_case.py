from uuid import UUID
from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.domain.exceptions.supplier_not_found_exception import SupplierNotFoundException
from app.modules.supplier.domain.exceptions.supplier_already_exists_exception import SupplierAlreadyExistsException
from app.common.exceptions import ValidationException
from app.modules.supplier.application.utils import clean_supplier_name, clean_tax_id

class UpdateSupplierUseCase:
    """
    Application use case responsible for updating an existing Supplier's profile.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: UUID, updates: dict[str, object]) -> Supplier:
        if not updates:
            raise ValidationException("No se enviaron campos para actualizar.")

        supplier = self.repository.get_by_id(supplier_id)
        if supplier is None:
            raise SupplierNotFoundException(supplier_id)

        # Extract values or fallback to current values
        name = str(updates.get("name", supplier.name))
        tax_id = updates.get("tax_id")
        
        # Determine target tax_id
        if "tax_id" in updates:
            target_tax_id = clean_tax_id(tax_id)
        else:
            target_tax_id = supplier.tax_id

        # Normalize name
        target_name = clean_supplier_name(name)

        # Check for tax ID uniqueness in the company scope if changed and not None
        if target_tax_id is not None and target_tax_id != supplier.tax_id:
            existing = self.repository.get_by_tax_id(supplier.company_id, target_tax_id)
            if existing is not None and existing.id != supplier.id:
                raise SupplierAlreadyExistsException(target_tax_id, supplier.company_id)

        # Extract contact information
        target_contact_name = updates.get("contact_name") if "contact_name" in updates else supplier.contact_name
        target_phone = updates.get("phone") if "phone" in updates else supplier.phone
        target_email = updates.get("email") if "email" in updates else supplier.email

        # If any value is None/Empty String, set it appropriately or preserve
        if target_contact_name is not None:
            target_contact_name = str(target_contact_name)
        if target_phone is not None:
            target_phone = str(target_phone)
        if target_email is not None:
            target_email = str(target_email)

        # Delegate update logic to the domain entity
        supplier.update_profile(
            name=target_name,
            tax_id=target_tax_id,
            contact_name=target_contact_name,
            phone=target_phone,
            email=target_email
        )

        return self.repository.update(supplier)
