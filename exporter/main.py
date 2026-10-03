import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from db import get_results_per_discipline
from models import DatabaseSettings
from render import write_discipline_pages

load_dotenv()


def main(
    db_settings: DatabaseSettings,
    day: date,
    output_folder: Path,
    template_file: Path,
    logo_file: Path | None,
):
    """
    Main function of the Meyton results exporter. Fetches the competition results for the
    given day from the Meyton database and exports them to one static HTML file per discipline.

    Args:
        db_settings (DatabaseSettings): Object containing the database connection configuration
        day (date): The tournament date for which to fetch results
        output_folder (Path): Path to the folder where the HTML files should be saved
        template_file (Path): Path to the HTML page template file
        logo_file (Path | None): Optional path to a logo image to embed in each HTML page
    """

    results_per_discipline = get_results_per_discipline(db_settings, day)

    written = write_discipline_pages(
        results_per_discipline,
        day=day,
        output_folder=output_folder,
        template_file=template_file,
        logo_file=logo_file,
    )

    for path in written:
        print(f"Wrote {path}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--date",
        type=lambda s: date.strptime(s, "%Y-%m-%d"),
        default=date.today(),
        help="The tournament date for which to fetch results."
    )
    argparser.add_argument(
        "--output-folder",
        type=Path,
        default=Path("output")
    )
    argparser.add_argument(
        "--template-file",
        type=Path,
        default=Path("input") / "template.html",
        help="Path to the HTML page template file."
    )
    argparser.add_argument(
        "--logo-file",
        type=Path,
        default=Path("assets") / "logo-white.png",
        help="Path to a logo image to embed in each HTML page."
    )
    args = argparser.parse_args()

    db_settings = DatabaseSettings(
        user=os.getenv("MARIADB_USER"),
        password=os.getenv("MARIADB_PASSWORD"),
        host=os.getenv("MARIADB_HOST"),
        port=int(os.getenv("MARIADB_PORT", "3306")),
        database=os.getenv("MARIADB_DATABASE")
    )

    main(
        db_settings=db_settings,
        day=args.date,
        output_folder=args.output_folder,
        template_file=args.template_file,
        logo_file=args.logo_file,
    )
