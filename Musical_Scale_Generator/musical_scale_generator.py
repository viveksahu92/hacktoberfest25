
NOTES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTES_FLAT  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# Defining the semitone patterns for different scale types
SCALE_PATTERNS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "natural_minor": [2, 1, 2, 2, 1, 2, 2],
    "harmonic_minor": [2, 1, 2, 2, 1, 3, 1],
    "melodic_minor": [2, 1, 2, 2, 2, 2, 1],
    "pentatonic_major": [2, 2, 3, 2, 3],
    "pentatonic_minor": [3, 2, 2, 3, 2],
    "blues": [3, 2, 1, 1, 3, 2],
}

def generate_scale(root: str, scale_type: str, use_flats: bool = False):
    """
    Generate a musical scale from a root note and a scale type.
    
    Args:
        root (str): Root note, e.g. "C", "A#", "Db"
        scale_type (str): Type of scale, e.g. "major", "natural_minor"
        use_flats (bool): Use flat note naming
    
    Returns:
        list: Notes in the generated scale
    """
    root = root.capitalize()
    notes = NOTES_FLAT if use_flats else NOTES_SHARP

    if scale_type not in SCALE_PATTERNS:
        raise ValueError(f"Unknown scale type '{scale_type}'. Try one of: {list(SCALE_PATTERNS.keys())}")
    
    if root not in notes:
        equivalents = {"Db":"C#", "Eb":"D#", "Gb":"F#", "Ab":"G#", "Bb":"A#"}
        root = equivalents.get(root, root)
    
    if root not in notes:
        raise ValueError(f"Invalid root note '{root}'. Must be one of: {notes}")

    pattern = SCALE_PATTERNS[scale_type]
    index = notes.index(root)
    
    scale = [root]
    for step in pattern:
        index = (index + step) % len(notes)
        scale.append(notes[index])
    return scale

examples = [
    ("C", "major"),
    ("A", "natural_minor"),
    ("C", "blues")
]

for root, scale_type in examples:
    print(f"\n {root} {scale_type.replace('_', ' ').title()} Scale:")
    print("-> ".join(generate_scale(root, scale_type)))
