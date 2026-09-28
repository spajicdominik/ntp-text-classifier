#!/bin/sh
# Pokrece klasifikator unutar snapa.

# Tkinter iz python3-tk paketa stoji u usr/lib/python3.12, pa ga dodajemo
# u put, zajedno s nasim kodom u $SNAP/app.
export PYTHONPATH="$SNAP/app:$SNAP/usr/lib/python3.12:$SNAP/usr/lib/python3.12/lib-dynload"

# Tcl/Tk biblioteke su za svaku arhitekturu u drugoj mapi.
case "$SNAP_ARCH" in
    amd64) TRIPLET=x86_64-linux-gnu ;;
    arm64) TRIPLET=aarch64-linux-gnu ;;
esac
export LD_LIBRARY_PATH="$SNAP/usr/lib/$TRIPLET:$LD_LIBRARY_PATH"
export TCL_LIBRARY="$SNAP/usr/share/tcltk/tcl8.6"
export TK_LIBRARY="$SNAP/usr/share/tcltk/tk8.6"

# Model je vec u snapu, na internet ne treba ici.
export TEXT_CLASSIFIER_MODEL="$SNAP/model"
export HF_HUB_OFFLINE=1

exec "$SNAP/bin/python3" -m text_classifier
