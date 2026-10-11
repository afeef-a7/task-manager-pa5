from utils.errors import ValidationError

PRODUCTS: dict[int, dict] = {}

def create_product(name: str, price: float) -> dict:
    """Create a new product.

    Args:
        name: The product's name.
        price: The product's price.

    Returns:
        The newly created product record.

    Raises:
        ValidationError: If name is empty or price is negative.
    """
    if not name or not name.strip():
        raise ValidationError("name", "cannot be empty")
    if price < 0:
        raise ValidationError("price", "cannot be negative")
    new_id = max(PRODUCTS.keys(), default=0) + 1
    PRODUCTS[new_id] = {"id": new_id, "name": name, "price": price}
    return PRODUCTS[new_id]
