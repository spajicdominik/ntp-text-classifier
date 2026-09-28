#!/bin/sh
# Brzi test instaliranog snapa, bez GUI-a: ucita model iz snapa i
# klasificira jednu recenicu. Pokrece se unutar snap okruzenja:
#   snap run --shell text-classifier -c "sh scripts/snap_smoke_test.sh"
set -e

# isti env kao u snap/local/launcher.sh
export PYTHONPATH="$SNAP/app:$SNAP/usr/lib/python3.12:$SNAP/usr/lib/python3.12/lib-dynload"
export TEXT_CLASSIFIER_MODEL="$SNAP/model"
export HF_HUB_OFFLINE=1

exec "$SNAP/bin/python3" - <<'EOF'
import tkinter
from text_classifier.model.transformer_classifier import TransformerClassifier

r = TransformerClassifier().classify(
    "The central bank raised interest rates to curb inflation")
print(f"tk {tkinter.TkVersion} | {r.label} {r.confidence:.0%}")
assert r.label == "Business", r.label
EOF
