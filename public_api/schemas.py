from pydantic import BaseModel


class MemeBase(BaseModel):
    title: str
    description: str
    image_url: str


class MemeCreate(BaseModel):
    pass


class Meme(BaseModel):
    id: int

    class Config:
        from_attributes = True
