from enum import Enum

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


class Composition (BaseModel):
    id: int
    name: str
    created: str
    edited: str

class Section (BaseModel):
    id: int
    name: str
    section_key: Keys
    signature_numerator: Numerator
    signature_denominator: Denominator
    repeat: int
    composition_id: int

class Chord (BaseModel):
    id: int
    chord: str
    duration_numerator: Numerator
    duration_denominator: Denominator
    section_id: int