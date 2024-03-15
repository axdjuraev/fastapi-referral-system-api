from axsqlalchemy.schema import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    class Config:
        orm_mode = True
