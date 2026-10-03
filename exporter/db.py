import logging
import sys
from datetime import date

import mariadb

from models import DatabaseSettings, Result

logger = logging.getLogger(__name__)


def get_db_connection(settings: DatabaseSettings) -> mariadb.Connection:
    """
    Establishes a connection to the MariaDB database using the provided credentials.

    Args:
        settings (DatabaseSettings): Object containing the database connection configuration
    Returns:
        mariadb.Connection: Object representing the established database connection
    """
    try:
        return mariadb.connect(
            user=settings.user,
            password=settings.password,
            host=settings.host,
            port=settings.port,
            database=settings.database
        )

    except mariadb.Error as e:
        logger.error(f"Error connecting to MariaDB: {e}")
        sys.exit(1)


def get_competition_results(db_settings: DatabaseSettings, day: date) -> list[Result]:
    """
    Queries the database and returns the competition results for the given day

    Args:
        db_settings (DatabaseSettings): Object containing the database connection configuration
        day (date): The tournament date for which to fetch results
    Returns:
        list[Result]: List of Result objects representing the fetched competition results
    """
    conn = get_db_connection(db_settings)

    cur = conn.cursor()
    with open("queries/results.sql", "r") as f:
        date_str = day.strftime("%Y-%m-%d")
        cur.execute(f.read(), (date_str + "%",))

    return [Result(*row) for row in cur.fetchall()]


def get_results_per_discipline(db_settings: DatabaseSettings, day: date) -> dict[str, list[Result]]:
    """
    Queries the database and returns the results per discipline for the given day

    Args:
        db_settings (DatabaseSettings): Object containing the database connection configuration
        day (date): The tournament date for which to fetch results
    Returns:
        dict[str, list[Result]]: Dictionary mapping discipline names to lists of Result objects
            representing the fetched competition results for that discipline
    """
    results = get_competition_results(db_settings, day)

    results_per_discipline: dict[str, list[Result]] = {}
    for r in results:
        if r.discipline not in results_per_discipline:
            results_per_discipline[r.discipline] = []
        results_per_discipline[r.discipline].append(r)

    return results_per_discipline
