import logging
import shutil
from pathlib import Path

import braunchem.utils.config as config
from braunchem.presentation import PresentationSet


def main():
    logging.basicConfig(level=logging.INFO, filename="bin/pres.log", filemode="w")

    config.load_config("bin/config.cfg")

    pres_db = PresentationSet.parse_database(config.PRESENTATIONS_DIR)

    pres_db["S2A"].write_pdf(
        tmp_dir=config.TMP_PRESENTATIONS_DIR,
        out_dir=config.OUT_DIR.joinpath("presentations"),
    )


if __name__ == "__main__":
    main()
