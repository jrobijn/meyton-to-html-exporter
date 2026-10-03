import base64
import re
from datetime import date
from html import escape
from pathlib import Path
from string import Template

from models import Result

ROW_TEMPLATE = """<tr>
<td class="rank">{rank}</td>
<td class="name">{name}</td>
<td class="club">{club}</td>
<td class="series">{series1}</td>
<td class="series">{series2}</td>
<td class="series">{series3}</td>
<td class="tens">{inner_tens}</td>
<td class="total">{total}</td>
</tr>"""


def _safe_filename(name: str) -> str:
    """
    Converts a discipline name into a filesystem-safe filename component.

    Args:
        name (str): The discipline name to convert
    Returns:
        str: A lowercase, hyphen-separated filename-safe version of the name
    """
    slug = re.sub(r"[^\w]+", "-", name.strip().lower())
    return slug.strip("-") or "discipline"


def _blank_if_none(value: int | None) -> str:
    """
    Formats a series value, returning an empty string when the value is None.

    Args:
        value (int | None): The series value to format
    Returns:
        str: The value as a string, or an empty string when it is None
    """
    return "" if value is None else str(value)


def _logo_tag(logo_file: Path | None) -> str:
    """
    Builds an <img> tag with the logo embedded as a base64 data URI, or an empty
    string when no logo is available.

    Args:
        logo_file (Path | None): Path to the logo image file, if any
    Returns:
        str: An HTML <img> tag with the embedded logo, or an empty string
    """
    if logo_file is None or not logo_file.is_file():
        return ""

    encoded = base64.b64encode(logo_file.read_bytes()).decode("ascii")
    return f'<img src="data:image/png;base64,{encoded}" alt="logo">'


def render_discipline_page(
    template: Template,
    discipline: str,
    results: list[Result],
    day: date,
    logo_file: Path | None = None,
) -> str:
    """
    Renders a static HTML results page for a single discipline.

    Args:
        template (Template): The page template to fill in
        discipline (str): The name of the discipline
        results (list[Result]): The results to display for this discipline
        day (date): The competition date shown in the page header
        logo_file (Path | None): Optional path to a logo image to embed in the header
    Returns:
        str: The complete HTML document as a string
    """
    ranked = sorted(results, key=lambda r: (r.total, r.inner_tens), reverse=True)

    rows = "\n".join(
        ROW_TEMPLATE.format(
            rank=i + 1,
            name=escape(r.full_name),
            club=escape(r.club or ""),
            series1=_blank_if_none(r.series1),
            series2=_blank_if_none(r.series2),
            series3=_blank_if_none(r.series3),
            inner_tens=r.inner_tens,
            total=r.rounded_total,
        )
        for i, r in enumerate(ranked)
    )

    return template.substitute(
        discipline=escape(discipline),
        date=day.strftime("%d-%m-%Y"),
        logo=_logo_tag(logo_file),
        rows=rows,
    )


def write_discipline_pages(
    results_per_discipline: dict[str, list[Result]],
    day: date,
    output_folder: Path,
    template_file: Path,
    logo_file: Path | None = None,
) -> list[Path]:
    """
    Writes one static HTML results page per discipline into the output folder.

    Args:
        results_per_discipline (dict[str, list[Result]]): Mapping of discipline names to
            their results
        day (date): The competition date shown in each page header
        output_folder (Path): The folder in which to write the HTML files
        template_file (Path): Path to the HTML page template file
        logo_file (Path | None): Optional path to a logo image to embed in each page
    Returns:
        list[Path]: Paths of the HTML files that were written
    """
    output_folder.mkdir(parents=True, exist_ok=True)
    date_str = day.strftime("%Y-%m-%d")
    template = Template(template_file.read_text(encoding="utf-8"))

    written: list[Path] = []
    for discipline, results in results_per_discipline.items():
        page = render_discipline_page(template, discipline, results, day, logo_file)
        out_file = output_folder / f"{_safe_filename(discipline)}-{date_str}.html"
        out_file.write_text(page, encoding="utf-8")
        written.append(out_file)

    return written
