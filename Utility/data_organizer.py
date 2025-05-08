import pandas as pd
import os

# Define configurations: (data_type, tissue_type, level, extension)
configs = [
    ("WGS", "blood", "sample", "clr"),
    ("WGS", "blood", "case", "clr"),
    ("WGS", "solid", "sample", "clr"),
    ("WGS", "solid", "case", "clr"),
    ("WXS", "blood", "sample", "clr"),
    ("WXS", "blood", "case", "clr"),
    ("WXS", "solid", "sample", "clr"),
    ("WXS", "solid", "case", "clr"),
]

base_path = "../Data/TCMA/Clean Data"

for seq, tissue, level, ext in configs:
    try:
        # Build full paths
        abundance_path = f"{base_path}/bacteria.{seq}.{tissue}.{level}.{ext}.txt"
        metadata_path = f"{base_path}/metadata.{seq}.{tissue}.{level}.txt"
        output_path = f"{base_path}/merged_{seq}_{tissue}_{level}_{ext}.csv"

        # Load data
        X = pd.read_csv(abundance_path, sep='\t', index_col=0).T
        meta = pd.read_csv(metadata_path, sep='\t')
        meta.rename(columns={meta.columns[0]: "SampleID"}, inplace=True)

        # Merge on SampleID
        df = X.merge(meta, left_index=True, right_on="SampleID")

        # Reorder columns: metadata first
        meta_cols = meta.columns.tolist()
        feature_cols = [col for col in df.columns if col not in meta_cols]
        df = df[meta_cols + feature_cols]

        # Save merged file
        df.to_csv(output_path, index=False)
        print(f"[✓] Merged and saved: {output_path}")
    except Exception as e:
        print(f"[✗] Error in {seq}-{tissue}-{level}-{ext}: {e}")
