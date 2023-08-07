from rpmk.new_core.keycodes import *
from rpmk.new_core.key import Key

KEYMAP = {
    "layers": ["l1"],
    "l1": ["r1", "r2", "r1"],
    "r1": [
        Key(KB_0),
        Key(KB_1),
        Key(KB_2),
        Key(KB_3),
        Key(KB_4),
        Key(KB_5),
        Key(KB_6),
        Key(KB_7),
        Key(KB_8),
        Key(KB_9),
    ],
    "r2": [
        Key(KB_A),
        Key(KB_B),
        Key(KB_C),
        Key(KB_D),
        Key(KB_E),
        Key(KB_F),
        Key(KB_G),
        Key(KB_H),
        Key(KB_I),
        Key(KB_J),
    ],
}
