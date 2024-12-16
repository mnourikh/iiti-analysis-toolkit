
# IITI Analysis Toolkit
# This script provides tools for Intra-Industry Trade (IITI) analysis and related indices.

import pandas as pd
import numpy as np

# Initial Processing
def initial_process(df, digits):
    # Aggregates data by year and HS code level (e.g., 2-digit, 4-digit).
    df_copy = df.copy()
    df_copy['code'] = df_copy['code'] // (10 ** (6 - digits))
    df_grouped = df_copy.groupby(['year', 'code'], as_index=False).agg({
        'dollar': 'sum',
        'rial': 'sum',
        'weight': 'sum'
    })
    return df_grouped

# IITI, WIITI, and MIITI Analysis
def iiti_analysis(export_df, import_df, name, top_n=10, output_dir="results"):
    # Merge export and import data
    trade = pd.merge(export_df, import_df, on=['year', 'code'], how='outer')
    trade = trade.rename(columns={'dollar_x': 'export', 'dollar_y': 'import'})
    trade['export'] = trade['export'].fillna(0)
    trade['import'] = trade['import'].fillna(0)
    
    # Calculate indices
    trade['diff'] = abs(trade['export'] - trade['import'])
    trade['IITI'] = 1 - (trade['diff'] / (trade['export'] + trade['import']))

    year_totals = trade.groupby('year')[['export', 'import']].sum()
    trade = trade.merge(year_totals, on='year', suffixes=('', '_total'))
    trade['weight'] = (trade['export'] + trade['import']) / (trade['export_total'] + trade['import_total'])
    trade['WIITI'] = trade['IITI'] * trade['weight']

    trade.sort_values(by=['code', 'year'], inplace=True)
    trade['dExport'] = trade.groupby('code')['export'].diff().fillna(0)
    trade['dImport'] = trade.groupby('code')['import'].diff().fillna(0)
    trade['MIITI'] = 1 - abs(trade['dExport'] - trade['dImport']) / (abs(trade['dExport']) + abs(trade['dImport']))
    trade['MIITI'] = np.where((trade['dExport'] == 0) & (trade['dImport'] == 0), 0, trade['MIITI'])

    # Aggregate results
    results = trade.groupby('year', as_index=False).agg({
        'IITI': 'mean',
        'WIITI': 'sum',
        'MIITI': 'mean'
    })

    # Top-ranked data per year based on WIITI
    top_trade_df = trade.groupby('year').apply(lambda x: x.nlargest(top_n, 'WIITI')).reset_index(drop=True)
    
    # Save outputs
    output_dir = f"./{output_dir}"
    os.makedirs(output_dir, exist_ok=True)
    results.to_excel(f"{output_dir}/IITI_Analysis_Results_{name}.xlsx", index=False)
    top_trade_df.to_excel(f"{output_dir}/Top_{top_n}_WIITI_{name}.xlsx", index=False)
    trade.to_excel(f"{output_dir}/Trade_Data_{name}.xlsx", index=False)

    print(f"IITI Analysis results saved in {output_dir}/")
    return results, top_trade_df

if __name__ == "__main__":
    # Example Usage
    # Load datasets (adjust paths as needed)
    export_data = pd.read_parquet("export_data.parquet")
    import_data = pd.read_parquet("import_data.parquet")

    # Process datasets
    export_hs2 = initial_process(export_data, 2)
    import_hs2 = initial_process(import_data, 2)

    export_hs4 = initial_process(export_data, 4)
    import_hs4 = initial_process(import_data, 4)

    # Run analysis for HS2 and HS4 levels
    iiti_results_hs2, top_trade_hs2 = iiti_analysis(export_hs2, import_hs2, "HS2")
    iiti_results_hs4, top_trade_hs4 = iiti_analysis(export_hs4, import_hs4, "HS4")
