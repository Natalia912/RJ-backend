from sqlmodel import Field, SQLModel

class Composition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    created: str
    edited: str

class Section(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    section_key: str
    signature_numerator: int
    signature_denominator: int
    repeat: int
    composition_id: int = Field(foreign_key="composition.id")

class Chord(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chord: str
    duration_numerator: int
    duration_denominator: int
    section_id: int = Field(foreign_key="section.id")



# -- Indexes for performance (add these after creating tables)
# CREATE INDEX idx_sections_composition_id ON sections(composition_id);
# CREATE INDEX idx_chords_section_id ON chords(section_id);