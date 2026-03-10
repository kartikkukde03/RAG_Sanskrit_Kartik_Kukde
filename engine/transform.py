from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def to_devanagari(text: str) -> str:
    return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)


def to_transliteration(text: str) -> str:
    return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
