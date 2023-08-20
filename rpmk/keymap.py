from rpmk.new_core.keycodes import *
from rpmk.new_core.key import Key

KEYMAP = {
    "layers": ["l1"],
    "l1": ["r1", "r2", "r3"],
    "r1": [
        Key(KB_Q),
        Key(KB_W),
        Key(KB_E),
        Key(KB_R),
        Key(KB_T),
        Key(KB_Y),
        Key(KB_U),
        Key(KB_I),
        Key(KB_O),
        Key(KB_P),
    ],
    "r2": [
        Key(KB_A),
        Key(KB_S),
        Key(KB_D),
        Key(KB_F),
        Key(KB_G),
        Key(KB_H),
        Key(KB_J),
        Key(KB_K),
        Key(KB_L),
        Key(KB_SEMICOLON),
    ],
    "r3": [
        Key(),
        Key(KB_X),
        Key(KB_C),
        Key(KB_V),
        Key(KB_SPACE),
        Key(KB_BACK_SPACE),
        Key(KB_M),
        Key(KB_COMMA),
        Key(KB_DOT),
        Key(),
    ],
}
