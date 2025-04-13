from pydantic import BaseModel

class OffshoreLeaks(BaseModel):
    entity:str
    jurisdiction: str
    linkedTo: str
    dataFrom: str

class WorldBank(BaseModel):
    firmName:str
    address: str
    country: str
    fromDate: str
    toDate: str
    ground: str

class OFACformat(BaseModel):
    name: str
    address: str
    type: str
    programs: str
    list: str
    score: str

class EntityRiskData(BaseModel):
    #offshoreLeaksResults: list[OffshoreLeaks] | None = None
    #offshoreLeaksHits: int | None = None
    #worldBankResultsResults: list[WorldBank] | None = None
    #worldBankResultsHits: int | None = None
    ofacResults: list[OFACformat] | None = None
    ofacHits: int | None = None