from http.client import HTTPException
from typing import List, Optional
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(
    title="VetNordic Mock API",
    version="0.0.2",
    contact={"Name": "Emil Hørlyck", "email": "eh@signifly.com"},
)

productsTable = {}


class Product(BaseModel):
    id: int
    title: str
    sku: int
    price: Optional[float] = None
    itemCode: int
    productDescription: Optional[str] = None
    productDescription2: Optional[str] = None
    SAP: Optional[float] = None
    micron: Optional[float] = None
    material: Optional[str] = None
    size: Optional[str] = None
    coating: Optional[str] = None
    category: Optional[str] = None
    subCategory: Optional[str] = None
    brand: Optional[str] = None
    individualItemDescription: Optional[str] = None
    barcodesPerIndividualItem: Optional[List[int]] = None
    skuDescription: Optional[str] = None
    skuUnitDescription: Optional[str] = None
    qtyPerSku: Optional[int] = None
    tarifCode: Optional[int] = None
    UNSPSC: Optional[int] = None


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK, tags=["products"])
def get_product(product_id: int):
    # if product_id not in products:
    #     raise HTTPException(status_code=404, details="Product ID not found")

    return productsTable[product_id]


@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["products"])
def create_product(product_id: int, product: Product):
    if product_id in productsTable:
        raise HTTPException(status_code=400, details="Product ID already exists")
    productsTable[product_id] = product
    return {"succesfully created product": {"id": product_id, "data": product}}


@app.post("/products", status_code=status.HTTP_201_CREATED, tags=["products"])
def create_product(products: List[Product]):

    operationStatus = status.HTTP_400_BAD_REQUEST

    failingProductIds = []

    for product in products:
        if product.id in productsTable:
            failingProductIds.append(product.id)
        else:
            productsTable[product.id] = product

    if len(products) == len(failingProductIds):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="All product ID already exists",
        )
    elif len(failingProductIds) > 0:
        raise HTTPException(
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            details="The following product IDs already exists: ",
        )

    raise HTTPException(status=operationStatus)
    return {"succesfully created product": {"id": product_id, "data": product}}


# @app.put("/product")
# def update_product(product: Product):
#     return {"title": product.title}
