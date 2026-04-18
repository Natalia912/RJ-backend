from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Enum
from ..schemas.composition import Keys

class Composition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    created: str
    edited: str
    user_id: int = Field(foreign_key="user.id")
    sections: list["Section"] = Relationship(back_populates="composition")

class Section(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    section_key: Keys = Field(sa_type=Enum(Keys))
    signature_numerator: int
    signature_denominator: int
    repeat: int
    composition_id: int = Field(foreign_key="composition.id")
    chords: list["Chord"] = Relationship(back_populates="section")
    composition: "Composition" = Relationship(back_populates="sections")

class Chord(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chord: Keys = Field(sa_type=Enum(Keys))
    duration_numerator: int
    duration_denominator: int
    section_id: int = Field(foreign_key="section.id")
    section: "Section" = Relationship(back_populates="chords")



# -- Indexes for performance (add these after creating tables)
# CREATE INDEX idx_sections_composition_id ON sections(composition_id);
# CREATE INDEX idx_chords_section_id ON chords(section_id);