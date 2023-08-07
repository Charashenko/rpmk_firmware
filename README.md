# rpmk_firmware
## Helper script example usage
```
sudo python tools/helper.py \
--mpy_cross_tool=../../downloads/micropython/tools/mpy_cross_all.py \
-b build/ \
-s rpmk/ \
-n utility/fw/flash_nuke.uf2 \
-m output/ \
-f utility/fw/firmware-blank.uf2 \
-l build/ \
--rshell_commands_dir tools/rshell_cmds/ \
run
```
