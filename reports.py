"""Member 4: Export analytics results safely to CSV and TXT files."""

from pathlib import Path


def export_table(dataframe, filename, output_dir="output"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    destination = output_path / filename
    dataframe.to_csv(destination, index=True)
    print(f"Saved: {destination.resolve()}")
    return destination


def export_text_report(sections, filename="cricket_report.txt",
                       output_dir="output"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    destination = output_path / filename

    with destination.open("w", encoding="utf-8") as file:  # Use UTF-8 for cross-platform compatibility.
        file.write("CRICKET SPORTS ANALYTICS REPORT\n")
        file.write("=" * 38 + "\n\n")

        for title, dataframe in sections:
            file.write(title.upper() + "\n")
            file.write("-" * len(title) + "\n")
            file.write(dataframe.to_string())
            file.write("\n\n")

    print(f"Saved: {destination.resolve()}")
    return destination
