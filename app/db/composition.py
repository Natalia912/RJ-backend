from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.models.composition import Composition, Section, Chord
from app.schemas.composition import CompositionNew, CompositionUpdate


def get_compositions(session: Session, user_id: int) -> list[Composition]:
    return session.exec(
        select(Composition)
        .options(joinedload(Composition.sections).joinedload(Section.chords))
        .where(Composition.user_id == user_id)
    ).unique().all()


def create_composition(session: Session, user_id: int, data: CompositionNew) -> Composition:
    composition = Composition(
        name=data.name,
        created=datetime.now().isoformat(),
        edited=datetime.now().isoformat(),
        user_id=user_id,
    )

    session.add(composition)
    session.commit()
    session.refresh(composition)

    for section_data in data.sections:
        db_section = Section(
            name=section_data.name,
            section_key=section_data.section_key,
            signature_numerator=section_data.signature_numerator,
            signature_denominator=section_data.signature_denominator,
            repeat=section_data.repeat,
            composition_id=composition.id,
        )
        session.add(db_section)
        session.commit()
        session.refresh(db_section)

        for chord_data in section_data.chords:
            db_chord = Chord(
                chord=chord_data.chord,
                duration_numerator=chord_data.duration_numerator,
                duration_denominator=chord_data.duration_denominator,
                section_id=db_section.id,
            )
            session.add(db_chord)
        session.commit()

    return composition


def update_composition(session: Session, composition_id: int, user_id: int, data: CompositionUpdate) -> None:
    existing = session.exec(
        select(Composition)
        .options(joinedload(Composition.sections).joinedload(Section.chords))
        .where(Composition.id == composition_id)
    ).first()

    if not existing or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail='Composition not found')

    existing.name = data.name
    existing.edited = datetime.now().isoformat()

    existing_sections = {section.id: section for section in existing.sections}
    updated_section_ids = set()

    for section_data in data.sections:
        if section_data.id and section_data.id in existing_sections:
            section = existing_sections[section_data.id]
            section.name = section_data.name
            section.section_key = section_data.section_key
            section.signature_numerator = section_data.signature_numerator
            section.signature_denominator = section_data.signature_denominator
            section.repeat = section_data.repeat

            existing_chords = {chord.id: chord for chord in section.chords}
            updated_chord_ids = set()

            for chord_data in section_data.chords:
                if chord_data.id and chord_data.id in existing_chords:
                    chord = existing_chords[chord_data.id]
                    chord.chord = chord_data.chord
                    chord.duration_numerator = chord_data.duration_numerator
                    chord.duration_denominator = chord_data.duration_denominator
                    updated_chord_ids.add(chord.id)
                else:
                    db_chord = Chord(
                        chord=chord_data.chord,
                        duration_numerator=chord_data.duration_numerator,
                        duration_denominator=chord_data.duration_denominator,
                        section_id=section.id,
                    )
                    session.add(db_chord)

            for chord_id, chord in existing_chords.items():
                if chord_id not in updated_chord_ids:
                    session.delete(chord)

            updated_section_ids.add(section.id)
        else:
            db_section = Section(
                name=section_data.name,
                section_key=section_data.section_key,
                signature_numerator=section_data.signature_numerator,
                signature_denominator=section_data.signature_denominator,
                repeat=section_data.repeat,
                composition_id=existing.id,
            )
            session.add(db_section)
            session.commit()
            session.refresh(db_section)

            for chord_data in section_data.chords:
                db_chord = Chord(
                    chord=chord_data.chord,
                    duration_numerator=chord_data.duration_numerator,
                    duration_denominator=chord_data.duration_denominator,
                    section_id=db_section.id,
                )
                session.add(db_chord)
            session.commit()

            updated_section_ids.add(db_section.id)

    for section_id, section in existing_sections.items():
        if section_id not in updated_section_ids:
            for chord in section.chords:
                session.delete(chord)
            session.delete(section)

    session.commit()


def delete_composition(session: Session, composition_id: int, user_id: int) -> None:
    existing = session.exec(
        select(Composition)
        .options(joinedload(Composition.sections).joinedload(Section.chords))
        .where(Composition.id == composition_id)
    ).first()

    if not existing or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail='Composition not found')

    for section in existing.sections:
        for chord in section.chords:
            session.delete(chord)
        session.delete(section)

    session.delete(existing)
    session.commit()
