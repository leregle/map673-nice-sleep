import pandas as pd

# ── LOAD ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    '/Users/mba-dd/Documents/GitHub/map673-nice-sleep/data/facilities-daily-population-latest.csv',
    sep=';',
    parse_dates=['date']
)
print(df.columns.tolist())
print(df.head(2))

# ── SPLIT ON JAN 20 2025 (inauguration) ────────────────────────────────────
cutoff = pd.Timestamp('2025-01-20')
before = df[df['date'] < cutoff].copy()
after  = df[df['date'] >= cutoff].copy()

# ── RATE HELPER ─────────────────────────────────────────────────────────────
def compute_rates(period):
    active = period[period['n_detained'] > 0].copy()
    active['convicted_rate'] = active['n_detained_convicted_criminal'] / active['n_detained']
    active['female_rate']    = active['n_detained_female'] / active['n_detained']

    midnight = period[period['n_detained_at_midnight'] > 0]

    return pd.DataFrame({
        'avg_midnight':   midnight.groupby('detention_facility_code')['n_detained_at_midnight'].mean(),
        'convicted_rate': active.groupby('detention_facility_code')['convicted_rate'].mean(),
        'female_rate':    active.groupby('detention_facility_code')['female_rate'].mean(),
        'active_days':    active.groupby('detention_facility_code')['date'].count()
    })

before_stats = compute_rates(before).add_suffix('_before')
after_stats  = compute_rates(after).add_suffix('_after')

# ── JOIN AND EXPORT ──────────────────────────────────────────────────────────
out = before_stats.join(after_stats, how='outer').reset_index()
out.rename(columns={'detention_facility_code': 'facility_id'}, inplace=True)

rate_cols = [c for c in out.columns if 'rate' in c or 'midnight' in c]
out[rate_cols] = out[rate_cols].round(4)

out.to_csv(
    '/Users/mba-dd/Documents/GitHub/map673-nice-sleep/data/facilities_before_after.csv',
    index=False
)
print(f"Exported {len(out)} facilities")
print(out[['facility_id','avg_midnight_before','avg_midnight_after',
           'convicted_rate_before','convicted_rate_after']].head(10))