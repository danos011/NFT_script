from pydantic import BaseModel
from typing import List


class Attribute(BaseModel):
    trait_type: str
    value: str


class NFT(BaseModel):
    name: str
    image: str
    attributes: List[Attribute]
    tier: int


class OutputInfo(BaseModel):
    item: NFT
    rarity_score: int


class Property(BaseModel):
    name: str
    weight: int
    quantity: int


class AttributeInfo(BaseModel):
    trait_type: str
    all_quantity: int
    properties: List[Property]
