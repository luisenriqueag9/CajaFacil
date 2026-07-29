import sqlite3

def seed():
    conn = sqlite3.connect("backend/caja_facil.db")
    c = conn.cursor()

    company_id = 'dc555b36ede8432ca8b9a31294c8308a'
    category_id = 'c1000000000000000000000000000001'
    brand_id = 'b1000000000000000000000000000001'
    unit_id = 'u10000000000000000000000000000001'

    # Clean existing seed records if any
    c.execute("DELETE FROM product WHERE company_id = ?", (company_id,))
    c.execute("DELETE FROM category WHERE company_id = ?", (company_id,))
    c.execute("DELETE FROM brand WHERE company_id = ?", (company_id,))
    c.execute("DELETE FROM unit WHERE company_id = ?", (company_id,))

    # Insert Category
    c.execute("""
        INSERT INTO category (id, company_id, name, status, protected)
        VALUES (?, ?, ?, ?, ?)
    """, (category_id, company_id, 'General', 'ACTIVE', 0))

    # Insert Brand
    c.execute("""
        INSERT INTO brand (id, company_id, name, status)
        VALUES (?, ?, ?, ?)
    """, (brand_id, company_id, 'General', 'ACTIVE'))

    # Insert Unit
    c.execute("""
        INSERT INTO unit (id, company_id, code, name, abbreviation, allows_decimal, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (unit_id, company_id, 'UND', 'Unidad', 'und', 0, 'ACTIVE'))

    # Insert Products
    products = [
        ('p10000000000000000000000000000001', '001', '001', 'Coca Cola 355ml', 15.00, 25.00, 15.00),
        ('p10000000000000000000000000000002', '002', '002', 'Pan Blanco', 10.00, 18.00, 15.00),
        ('p10000000000000000000000000000003', '003', '003', 'Hielo Bolsa', 12.00, 20.00, 15.00),
        ('p10000000000000000000000000000004', '004', '004', 'Agua 600ml', 8.00, 15.00, 15.00),
        ('p10000000000000000000000000000005', '005', '005', 'Leche Entera 1L', 25.00, 38.00, 15.00),
    ]

    for pid, code, barcode, name, cost, price, tax in products:
        c.execute("""
            INSERT INTO product (
                id, company_id, internal_code, barcode, name, cost, price, tax_rate,
                controls_stock, allows_decimal, is_perishable, minimum_stock, status,
                category_id, brand_id, unit_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0, 0.0, 'ACTIVE', ?, ?, ?)
        """, (pid, company_id, code, barcode, name, cost, price, tax, category_id, brand_id, unit_id))

    conn.commit()
    conn.close()
    print("Database seeded successfully with product catalog!")

if __name__ == "__main__":
    seed()
