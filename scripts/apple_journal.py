"""
Convert apple journal pdf output to structured json data
"""

import click
import pypdf
from datetime import datetime
import json

@click.command()
@click.option("--path", prompt="Path to Journal.pdf")
@click.option("--out", default="journal.json")
def export(path, out):
    output = {}
    reader = pypdf.PdfReader(path)
    page_content = ""
    for page in reader.pages:
        text = page.extract_text()
        heading = text.split("\n")[0].strip()
        try:
            date = datetime.strptime(heading, "%A %d %B %Y")
        except ValueError as e:
            page_content += " " + text
        else:
            page_content = text
        output[date.isoformat()] = page_content
    with open(out, 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    export()
