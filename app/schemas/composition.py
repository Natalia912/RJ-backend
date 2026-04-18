from enum import Enum
from typing import Optional

from pydantic import BaseModel

class Numerator(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11
    twelve = 12
    thirteen = 13
    fourteen = 14
    fifteen = 15
    sixteen = 16

class Denominator(int, Enum):
    two = 2
    four = 4
    eight = 8

class Keys(str, Enum):
    C = 'C'
    G = 'G'
    D = 'D'
    A = 'A'
    E = 'E'
    B = 'B'
    F_sharp = 'F#'
    C_sharp = 'C#'
    Ab = 'Ab'
    Eb = 'Eb'
    Bb = 'Bb'
    F = 'F'
    Am = 'Am'
    Em = 'Em'
    Bm = 'Bm'
    F_sharp_m = 'F#m'
    C_sharp_m = 'C#m'
    G_sharp_m = 'G#m'
    D_sharp_m = 'D#m'
    Bbm = 'Bbm'
    Fm = 'Fm'
    Cm = 'Cm'
    Gm = 'Gm'
    Dm = 'Dm'

class ChordBase(BaseModel):
    chord: Keys
    duration_numerator: Numerator
    duration_denominator: Denominator

class ChordCreate(ChordBase):
    pass

class ChordUpdate(ChordBase):
    id: Optional[int] = None

class SectionBase(BaseModel):
    name: str
    section_key: Keys
    signature_numerator: Numerator
    signature_denominator: Denominator
    repeat: int
    chords: list[ChordBase]

class SectionCreate(SectionBase):
    pass

class SectionUpdate(SectionBase):
    id: Optional[int] = None
    chords: list[ChordUpdate]

class CompositionBase(BaseModel):
    name: str
    sections: list[SectionBase]

class CompositionCreate(CompositionBase):
    pass

class Chord(ChordBase):
    id: int

class Section(SectionBase):
    id: int
    chords: list[Chord]

class Composition(CompositionBase):
    id: int
    created: str
    edited: str
    sections: list[Section]

class CompositionNew(CompositionCreate):
    pass

class CompositionUpdate(CompositionBase):
    sections: list[SectionUpdate]
    


