# Skine model s HuggingFacea u lokalnu mapu.
#
# Koristi se kod builda Docker imagea i snapa, da aplikacija poslije radi i
# bez interneta. Pokrece se ovako:
#   python scripts/download_model.py <mapa>

from __future__ import annotations

import sys

from huggingface_hub import snapshot_download

# Mora biti isti model kao u config.py.
MODEL_ID = "mrm8488/bert-mini-finetuned-age_news-classification"


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "model"
    # Treba nam samo safetensors, config i tokenizer. Stari .bin preskacem
    # jer bi image bez veze bio duplo veci.
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=target,
        allow_patterns=["*.json", "*.txt", "*.safetensors"],
    )
    print(f"Model spremljen u {target}")


if __name__ == "__main__":
    main()
