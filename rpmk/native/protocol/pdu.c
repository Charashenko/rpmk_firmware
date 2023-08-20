#include "py/dynruntime.h"

STATIC void add(mp_obj_t size_obj, mp_obj_t unit_idx_obj, ) {
  mp_bool_t bit = mp_obj_get_bool(bit_obj);
  if (pdu->bit_idx >= pdu->size) {
    pdu->unit_idx++;
    pdu->bit_idx = 0;
  }
  pdu->units[pdu->unit_idx] <<= 1;
  if (bit) {
    pdu->units[pdu->unit_idx]++;
  } else {
    if (!pdu->units[pdu->unit_idx]) {
      pdu->unit_begin_zeroes[pdu->unit_idx]++;
    }
  }
  pdu->bit_idx++;
}

STATIC MP_DEFINE_CONST_FUN_OBJ_1(add_obj, add);

// This is the entry point and is called when the module is imported
mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw,
                  mp_obj_t *args) {
  // This must be first, it sets up the globals dict and other things
  MP_DYNRUNTIME_INIT_ENTRY

  // Make the function available in the module's namespace
  mp_store_global(MP_QSTR_add, MP_OBJ_FROM_PTR(&add_obj));

  // This must be last, it restores the globals dict
  MP_DYNRUNTIME_INIT_EXIT
}