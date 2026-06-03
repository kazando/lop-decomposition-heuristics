import re
from pathlib import Path
import pandas as pd

input_dir = Path(".")
output_file = "maxsize_raw_results.csv"

# 対応するファイル名の例:
# xLOLIB_150-rborda_2.csv
# xLOLIB_150_rborda_2.csv
pattern = re.compile(
    r"^xLOLIB_150[-_](level|mincut|rborda)[-_](\d+)\.csv$"
)

rows = []

for path in sorted(input_dir.glob("*.csv")):
    if path.name == output_file:
        continue

    m = pattern.match(path.name)
    if not m:
        continue

    method = m.group(1)
    maxsize = int(m.group(2))

    df = pd.read_csv(
        path,
        header=None,
        names=["instance", "time", "objective"]
    )

    df.insert(0, "maxsize", maxsize)
    df.insert(0, "method", method)

    rows.append(df)

    print(f"Read {path.name}: method={method}, maxsize={maxsize}, rows={len(df)}")

if not rows:
    print("No input files were found.")
    print("Expected file names such as:")
    print("  xLOLIB_150-rborda_2.csv")
    print("  xLOLIB_150-mincut_2.csv")
    print("  xLOLIB_150-level_2.csv")
    raise SystemExit(1)

combined = pd.concat(rows, ignore_index=True)

combined = combined[
    ["method", "maxsize", "instance", "time", "objective"]
]

combined.to_csv(output_file, index=False)

print()
print(f"Created {output_file}")
print(f"Number of rows: {len(combined)}")
print(combined.head())