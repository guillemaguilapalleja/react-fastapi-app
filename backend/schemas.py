from pydantic import BaseModel


class SortMapSchema(BaseModel):
    value: str


class SortMap(SortMapSchema):
    id: int

    class Config:
        orm_mode = True


class ResponseSchema(BaseModel):
    sortmap_id: int
    response: str
    time: float


class RequestSchema(BaseModel):
    request: str
