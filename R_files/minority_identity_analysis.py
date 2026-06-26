import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from scipy import stats
import re
import warnings
warnings.filterwarnings('ignore')

import os
os.makedirs('outputs', exist_ok=True)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
MINORITY_LABELS = {
    'Black':    [r'\bblack\b', r'\bblack people\b', r'\bafrican[- ]american\b'],
    'Latino':   [r'\blatino\b', r'\blatina\b', r'\bhispanic\b', r'\blatinx\b'],
    'Asian':    [r'\basian\b', r'\bchinese[-\s]american\b', r'\bkorean[-\s]american\b'],
    'Refugee':  [r'\brefugee\b', r'\brefugees\b', r'\bundocumented\b', r'\bimmigrant\b'],
    'Muslim':   [r'\bmuslim\b', r'\bislamist\b'],
    'Jewish':   [r'\bjewish\b', r'\bjew\b'],
    'Indigenous': [r'\bindigenous\b', r'\bnative american\b', r'\btribal\b'],
}
NON_MINORITY_LABELS = {
    'White':         [r'\bwhite\b', r'\bcaucasian\b'],
    'Christian':     [r'\bchristian\b', r'\bevangelist\b'],
    'American-born': [r'\bamerican[- ]born\b'],
}
CRIME_KEYWORDS = [
    r'\bcrime\b', r'\bcriminal\b', r'\bmurder\b', r'\bshooting\b', r'\bassault\b',
    r'\brobbery\b', r'\btheft\b', r'\bviolence\b', r'\bterror\b', r'\barrest\b',
    r'\bkilling\b', r'\bhomicide\b', r'\bvictim\b', r'\battack\b', r'\bsuspect\b',
    r'\bgangster\b', r'\bdrug\b', r'\bguns\b', r'\bgunman\b', r'\bpolice\b',
]
SEVERITY_HIGH = [r'\bmurder\b', r'\bhomicide\b', r'\bterror\b', r'\bkilling\b', r'\bshooting\b']
SEVERITY_MED  = [r'\bassault\b', r'\brobbery\b', r'\bviolence\b', r'\battack\b', r'\bgunman\b']

CATALYSTS = {
    'Floyd Murder\n(May 2020)': (2020, 5),
    'Jan 6\nCapitol (2021)': (2021, 1),
    'Atlanta Spa\nShooting (2021)': (2021, 3),
    'Uvalde\n(May 2022)': (2022, 5),
}

PALETTE = {'Minority': '#E05C3A', 'Non-Minority': '#3A7EC0', 'Neutral': '#AAAAAA'}
FIG_STYLE = {'figure.facecolor': '#FAFAFA', 'axes.facecolor': '#F4F4F4',
             'axes.grid': True, 'grid.color': 'white', 'grid.linewidth': 1.2}

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
df = pd.read_excel('combined_news.xlsx')
df = df[df['pubtitle'].str.contains('New York Times', na=False)].copy()
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df[(df['year'] >= 2020) & (df['year'] <= 2026)].copy()
df['pubdate'] = pd.to_datetime(df['pubdate'], errors='coerce')
df['text'] = (df['Title'].fillna('') + ' ' +
              df['identifierKeywords'].fillna('') + ' ' +
              df['subjectTerms'].fillna('')).str.lower()

print(f"Total NYT articles (2020–2026): {len(df)}")

# ─── SEMANTIC FRAME EXTRACTION ────────────────────────────────────────────────
def match_any(text, patterns):
    return int(any(re.search(p, text) for p in patterns))

# Crime detection
df['is_crime'] = df['text'].apply(lambda t: match_any(t, CRIME_KEYWORDS))
# Severity
def get_severity(text):
    if match_any(text, SEVERITY_HIGH): return 2
    if match_any(text, SEVERITY_MED):  return 1
    return 0
df['crime_severity'] = df['text'].apply(get_severity)

# Identity markers
for label, pats in MINORITY_LABELS.items():
    df[f'min_{label}'] = df['text'].apply(lambda t: match_any(t, pats))
for label, pats in NON_MINORITY_LABELS.items():
    df[f'nonmin_{label}'] = df['text'].apply(lambda t: match_any(t, pats))

min_cols    = [f'min_{l}' for l in MINORITY_LABELS]
nonmin_cols = [f'nonmin_{l}' for l in NON_MINORITY_LABELS]

df['has_minority']     = (df[min_cols].sum(axis=1) > 0).astype(int)
df['has_non_minority'] = (df[nonmin_cols].sum(axis=1) > 0).astype(int)
df['identity_group']   = 'Neither'
df.loc[df['has_minority'] == 1, 'identity_group'] = 'Minority'
df.loc[(df['has_non_minority'] == 1) & (df['has_minority'] == 0), 'identity_group'] = 'Non-Minority'

crime_df = df[df['is_crime'] == 1].copy()
print(f"Crime-related articles: {len(crime_df)}")
print(f"  Minority-marked:     {crime_df['has_minority'].sum()}")
print(f"  Non-minority-marked: {crime_df['has_non_minority'].sum()}")

# ─── FIGURE 1 — Semantic Frame Extraction ────────────────────────────────────
with plt.rc_context(FIG_STYLE):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Figure 1 – Semantic Frame Extraction:\nIdentity Label Detection in Crime-Related NYT Articles (2020–2026)',
                 fontsize=14, fontweight='bold', y=1.02)

    # 1a — counts by label
    ax = axes[0]
    min_counts    = {l: crime_df[f'min_{l}'].sum() for l in MINORITY_LABELS}
    nonmin_counts = {l: crime_df[f'nonmin_{l}'].sum() for l in NON_MINORITY_LABELS}
    all_labels = list(min_counts.keys()) + list(nonmin_counts.keys())
    all_counts = list(min_counts.values()) + list(nonmin_counts.values())
    colors = [PALETTE['Minority']] * len(min_counts) + [PALETTE['Non-Minority']] * len(nonmin_counts)
    bars = ax.barh(all_labels, all_counts, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_xlabel('Article Count')
    ax.set_title('(a) Identity Label Frequency\nin Crime Context', fontweight='bold')
    for bar, val in zip(bars, all_counts):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, str(val),
                va='center', fontsize=8)
    p1 = mpatches.Patch(color=PALETTE['Minority'], label='Minority')
    p2 = mpatches.Patch(color=PALETTE['Non-Minority'], label='Non-Minority')
    ax.legend(handles=[p1, p2], fontsize=8)

    # 1b — proportion in crime vs non-crime
    ax = axes[1]
    groups = ['Minority\n(crime)', 'Minority\n(non-crime)', 'Non-Min.\n(crime)', 'Non-Min.\n(non-crime)']
    vals = [
        crime_df['has_minority'].mean() * 100,
        df[df['is_crime']==0]['has_minority'].mean() * 100,
        crime_df['has_non_minority'].mean() * 100,
        df[df['is_crime']==0]['has_non_minority'].mean() * 100,
    ]
    bar_colors = [PALETTE['Minority'], '#F0B0A0', PALETTE['Non-Minority'], '#A0C0E0']
    bars2 = ax.bar(groups, vals, color=bar_colors, edgecolor='white')
    ax.set_ylabel('% of Articles in Category')
    ax.set_title('(b) Identity Marking Rate:\nCrime vs Non-Crime Context', fontweight='bold')
    for bar, v in zip(bars2, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{v:.1f}%',
                ha='center', fontsize=9, fontweight='bold')

    # 1c — severity breakdown
    ax = axes[2]
    sev_labels = ['Low\n(0)', 'Medium\n(1)', 'High\n(2)']
    min_by_sev    = [crime_df[crime_df['crime_severity']==s]['has_minority'].mean()*100 for s in [0,1,2]]
    nonmin_by_sev = [crime_df[crime_df['crime_severity']==s]['has_non_minority'].mean()*100 for s in [0,1,2]]
    x = np.arange(3); w = 0.35
    ax.bar(x - w/2, min_by_sev, w, label='Minority', color=PALETTE['Minority'], edgecolor='white')
    ax.bar(x + w/2, nonmin_by_sev, w, label='Non-Minority', color=PALETTE['Non-Minority'], edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(sev_labels)
    ax.set_ylabel('% Articles with Identity Label')
    ax.set_title('(c) Identity Marking by\nCrime Severity Level', fontweight='bold')
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('outputs/fig1_semantic_frame.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 1 saved.")

# ─── FIGURE 2 — Temporal Shifts ──────────────────────────────────────────────
# yearly rates
yearly = crime_df.groupby('year').agg(
    total=('Title','count'),
    minority_n=('has_minority','sum'),
    nonmin_n=('has_non_minority','sum'),
).reset_index()
yearly['minority_rate']  = yearly['minority_n'] / yearly['total'] * 100
yearly['nonmin_rate']    = yearly['nonmin_n']   / yearly['total'] * 100

# monthly for smoothed trend
crime_df['ym'] = crime_df['pubdate'].dt.to_period('M')
monthly = crime_df.groupby('ym').agg(
    total=('Title','count'),
    minority_n=('has_minority','sum'),
    nonmin_n=('has_non_minority','sum'),
).reset_index()
monthly = monthly[monthly['total'] >= 5]
monthly['minority_rate'] = monthly['minority_n'] / monthly['total'] * 100
monthly['nonmin_rate']   = monthly['nonmin_n']   / monthly['total'] * 100
monthly['dt'] = monthly['ym'].dt.to_timestamp()

# per-label yearly breakdown
label_yearly = {}
for l in MINORITY_LABELS:
    label_yearly[l] = crime_df.groupby('year')[f'min_{l}'].mean() * 100

with plt.rc_context(FIG_STYLE):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Figure 2 – Temporal Shifts:\nIdentity Labeling in Crime Headlines (NYT, 2020–2026)',
                 fontsize=14, fontweight='bold')

    # 2a — yearly bar comparison
    ax = axes[0, 0]
    x = np.arange(len(yearly)); w = 0.35
    ax.bar(x - w/2, yearly['minority_rate'], w, label='Minority', color=PALETTE['Minority'], edgecolor='white')
    ax.bar(x + w/2, yearly['nonmin_rate'],   w, label='Non-Minority', color=PALETTE['Non-Minority'], edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(yearly['year'].astype(int))
    ax.set_ylabel('% Crime Articles with Identity Label')
    ax.set_title('(a) Yearly Labeling Rate: Minority vs Non-Minority', fontweight='bold')
    ax.legend()
    for i, row in yearly.iterrows():
        xi = list(yearly['year']).index(row['year'])
        ax.text(xi - w/2, row['minority_rate'] + 0.2, f"{row['minority_rate']:.1f}%", ha='center', fontsize=7, color=PALETTE['Minority'])
        ax.text(xi + w/2, row['nonmin_rate']   + 0.2, f"{row['nonmin_rate']:.1f}%",   ha='center', fontsize=7, color=PALETTE['Non-Minority'])

    # 2b — smoothed monthly trend with catalysts
    ax = axes[0, 1]
    ax.plot(monthly['dt'], monthly['minority_rate'].rolling(3, center=True).mean(),
            color=PALETTE['Minority'], lw=2.5, label='Minority (3-mo avg)')
    ax.plot(monthly['dt'], monthly['nonmin_rate'].rolling(3, center=True).mean(),
            color=PALETTE['Non-Minority'], lw=2.5, label='Non-Minority (3-mo avg)')
    ax.fill_between(monthly['dt'], monthly['minority_rate'].rolling(3,center=True).mean(),
                    alpha=0.15, color=PALETTE['Minority'])
    for name, (yr, mo) in CATALYSTS.items():
        dt = pd.Timestamp(yr, mo, 1)
        ax.axvline(dt, color='gray', ls='--', lw=1, alpha=0.8)
        ax.text(dt, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 25, name,
                fontsize=6.5, rotation=90, va='top', color='#555555')
    ax.set_ylabel('% Articles with Identity Label')
    ax.set_title('(b) Monthly Trend with Sociopolitical Catalysts', fontweight='bold')
    ax.legend(fontsize=9)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))

    # 2c — stacked minority label breakdown by year
    ax = axes[1, 0]
    bottom = np.zeros(len(yearly))
    cmap = plt.cm.get_cmap('Set2', len(MINORITY_LABELS))
    for i, l in enumerate(MINORITY_LABELS):
        rates = [crime_df[crime_df['year']==yr][f'min_{l}'].mean()*100 for yr in yearly['year']]
        ax.bar(yearly['year'].astype(int), rates, bottom=bottom, label=l, color=cmap(i), edgecolor='white')
        bottom += np.array(rates)
    ax.set_xlabel('Year'); ax.set_ylabel('Cumulative % (stacked)')
    ax.set_title('(c) Minority Label Composition by Year', fontweight='bold')
    ax.legend(fontsize=8, loc='upper right')

    # 2d — gap: minority rate minus nonmin rate
    ax = axes[1, 1]
    gap = yearly['minority_rate'] - yearly['nonmin_rate']
    bar_colors2 = [PALETTE['Minority'] if g > 0 else PALETTE['Non-Minority'] for g in gap]
    ax.bar(yearly['year'].astype(int), gap, color=bar_colors2, edgecolor='white')
    ax.axhline(0, color='black', lw=1)
    ax.set_xlabel('Year'); ax.set_ylabel('Minority Rate − Non-Minority Rate (pp)')
    ax.set_title('(d) Labeling Gap: Minority Overrepresentation', fontweight='bold')
    for yr, g in zip(yearly['year'].astype(int), gap):
        ax.text(yr, g + (0.3 if g >= 0 else -0.6), f'{g:+.1f}pp', ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig('outputs/fig2_temporal_shifts.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 2 saved.")

# ─── FIGURE 3 — Statistical Modeling ─────────────────────────────────────────
# Logistic regression: DV = has_minority, IVs = is_crime, crime_severity, year_centered
model_df = df[['has_minority','has_non_minority','is_crime','crime_severity','year']].dropna().copy()
model_df['year_c'] = model_df['year'] - 2020

# Model A: Minority ~ crime context
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2

def logistic_with_ci(X, y, labels):
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    clf = LogisticRegression(max_iter=1000, solver='lbfgs')
    clf.fit(Xs, y)
    coefs = clf.coef_[0]
    # Bootstrap CI
    rng = np.random.default_rng(42)
    boot_coefs = []
    for _ in range(500):
        idx = rng.integers(0, len(Xs), len(Xs))
        try:
            c = LogisticRegression(max_iter=500).fit(Xs[idx], y.iloc[idx]).coef_[0]
            boot_coefs.append(c)
        except: pass
    boot_coefs = np.array(boot_coefs)
    ci_lo = np.percentile(boot_coefs, 2.5, axis=0)
    ci_hi = np.percentile(boot_coefs, 97.5, axis=0)
    or_    = np.exp(coefs)
    or_lo  = np.exp(ci_lo)
    or_hi  = np.exp(ci_hi)
    return pd.DataFrame({'Variable': labels, 'LogOdds': coefs,
                         'OR': or_, 'OR_lo': or_lo, 'OR_hi': or_hi})

# Model for minority marking
X_min = model_df[['is_crime','crime_severity','year_c']]
res_min = logistic_with_ci(X_min.values, model_df['has_minority'],
                           ['Crime Context','Crime Severity','Year Trend'])
res_min['Group'] = 'Minority'

# Model for non-minority marking
res_nonmin = logistic_with_ci(X_min.values, model_df['has_non_minority'],
                              ['Crime Context','Crime Severity','Year Trend'])
res_nonmin['Group'] = 'Non-Minority'

res_all = pd.concat([res_min, res_nonmin])

# Chi-square test: minority vs nonmin in crime context
cont_table = pd.crosstab(crime_df['identity_group'],
                         crime_df['crime_severity'].map({0:'Low',1:'Med',2:'High'}))
chi2_stat, p_val, dof, _ = stats.chi2_contingency(cont_table)

# Proportion test: minority marking in crime vs non-crime
crime_min_rate = crime_df['has_minority'].mean()
noncrime_min_rate = df[df['is_crime']==0]['has_minority'].mean()
n1, n2 = len(crime_df), len(df[df['is_crime']==0])
p_pool = (crime_df['has_minority'].sum() + df[df['is_crime']==0]['has_minority'].sum()) / (n1+n2)
z_stat = (crime_min_rate - noncrime_min_rate) / np.sqrt(p_pool*(1-p_pool)*(1/n1+1/n2))
p_z = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"\nChi2 test (identity × severity): χ²={chi2_stat:.2f}, p={p_val:.4f}, dof={dof}")
print(f"Z-test (minority rate crime vs non-crime): z={z_stat:.2f}, p={p_z:.4e}")
print(f"  Crime articles: {crime_min_rate*100:.2f}% minority-marked")
print(f"  Non-crime articles: {noncrime_min_rate*100:.2f}% minority-marked")

with plt.rc_context(FIG_STYLE):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Figure 3 – Statistical Modeling:\nHypothesis Test — Minority Identities More Explicitly Marked in Crime Context',
                 fontsize=14, fontweight='bold')

    # 3a — Forest plot (Odds Ratios)
    ax = axes[0, 0]
    colors_or = {
        ('Crime Context','Minority'): PALETTE['Minority'],
        ('Crime Context','Non-Minority'): PALETTE['Non-Minority'],
        ('Crime Severity','Minority'): '#E8967A',
        ('Crime Severity','Non-Minority'): '#7AAAD4',
        ('Year Trend','Minority'): '#EEBBA0',
        ('Year Trend','Non-Minority'): '#A0C4E8',
    }
    y_pos = []; y_labels = []; y_colors = []
    tick_pos = 0
    for var in ['Crime Context','Crime Severity','Year Trend']:
        for grp in ['Minority','Non-Minority']:
            row = res_all[(res_all['Variable']==var) & (res_all['Group']==grp)].iloc[0]
            ax.errorbar(row['OR'], tick_pos,
                        xerr=[[row['OR']-row['OR_lo']], [row['OR_hi']-row['OR']]], 
                        fmt='o', color=colors_or.get((var,grp), 'gray'),
                        markersize=8, capsize=4, lw=1.5)
            ax.text(row['OR_hi']+0.02, tick_pos, f"{row['OR']:.2f}", va='center', fontsize=8)
            y_pos.append(tick_pos)
            y_labels.append(f'{var}\n({grp})')
            tick_pos += 1
        tick_pos += 0.5
    ax.axvline(1, color='black', ls='--', lw=1)
    ax.set_yticks(y_pos); ax.set_yticklabels(y_labels, fontsize=8)
    ax.set_xlabel('Odds Ratio (standardized predictors, 95% CI bootstrap)')
    ax.set_title('(a) Forest Plot: Odds Ratios\nMinority vs Non-Minority Models', fontweight='bold')

    # 3b — Proportion comparison with CI
    ax = axes[0, 1]
    groups_names = ['Crime\n(Minority)', 'Non-Crime\n(Minority)', 'Crime\n(Non-Min.)', 'Non-Crime\n(Non-Min.)']
    props = [
        crime_df['has_minority'].mean()*100,
        df[df['is_crime']==0]['has_minority'].mean()*100,
        crime_df['has_non_minority'].mean()*100,
        df[df['is_crime']==0]['has_non_minority'].mean()*100,
    ]
    ns = [len(crime_df), len(df[df['is_crime']==0])]*2
    errs = [1.96*np.sqrt((p/100)*(1-p/100)/n)*100 for p,n in zip(props,ns)]
    bar_c = [PALETTE['Minority'],'#F0B0A0',PALETTE['Non-Minority'],'#A0C0E0']
    bars3 = ax.bar(groups_names, props, color=bar_c, edgecolor='white',
                   yerr=errs, capsize=5, error_kw={'lw':1.5})
    ax.set_ylabel('% Articles with Identity Label')
    ax.set_title('(b) Proportion Test:\nMinority Marking in Crime vs Non-Crime', fontweight='bold')
    ax.text(0.5, 0.93, f'Z = {z_stat:.2f}, p {"< 0.001" if p_z < 0.001 else f"= {p_z:.4f}"}',
            transform=ax.transAxes, ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    for bar, v in zip(bars3, props):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{v:.1f}%',
                ha='center', fontsize=8, fontweight='bold')

    # 3c — Heatmap: identity group × severity
    ax = axes[1, 0]
    heat_df = crime_df.copy()
    heat_df['sev_label'] = heat_df['crime_severity'].map({0:'Low',1:'Medium',2:'High'})
    heat_df['id_simple'] = heat_df['identity_group']
    pivot = heat_df.groupby(['sev_label','id_simple'])['Title'].count().unstack(fill_value=0)
    pivot = pivot.reindex(index=['Low','Medium','High'],
                          columns=['Minority','Non-Minority','Neither'], fill_value=0)
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    sns.heatmap(pivot_pct, annot=True, fmt='.1f', cmap='RdBu_r',
                ax=ax, linewidths=0.5, cbar_kws={'label':'% of Articles'})
    ax.set_title(f'(c) Identity Group × Crime Severity\nHeatmap (% row)\nχ²={chi2_stat:.1f}, p{"<0.001" if p_val<0.001 else f"={p_val:.3f}"}',
                 fontweight='bold')
    ax.set_xlabel('Identity Group'); ax.set_ylabel('Crime Severity')

    # 3d — Year-by-year OR bar for crime context coefficient
    ax = axes[1, 1]
    yr_ors_min = []; yr_ors_nonmin = []
    years_list = sorted(df['year'].dropna().unique().astype(int))
    for yr in years_list:
        sub = df[df['year'] == yr][['has_minority','has_non_minority','is_crime','crime_severity']].dropna()
        if sub['is_crime'].sum() < 10: 
            yr_ors_min.append(np.nan); yr_ors_nonmin.append(np.nan); continue
        try:
            clf_m = LogisticRegression(max_iter=500).fit(sub[['is_crime','crime_severity']], sub['has_minority'])
            yr_ors_min.append(np.exp(clf_m.coef_[0][0]))
        except: yr_ors_min.append(np.nan)
        try:
            clf_n = LogisticRegression(max_iter=500).fit(sub[['is_crime','crime_severity']], sub['has_non_minority'])
            yr_ors_nonmin.append(np.exp(clf_n.coef_[0][0]))
        except: yr_ors_nonmin.append(np.nan)
    
    x = np.arange(len(years_list)); w = 0.35
    ax.bar(x - w/2, yr_ors_min,    w, label='Minority',     color=PALETTE['Minority'],     edgecolor='white')
    ax.bar(x + w/2, yr_ors_nonmin, w, label='Non-Minority', color=PALETTE['Non-Minority'], edgecolor='white')
    ax.axhline(1, color='black', ls='--', lw=1)
    ax.set_xticks(x); ax.set_xticklabels(years_list)
    ax.set_ylabel('Odds Ratio (crime context predictor)')
    ax.set_title('(d) OR of Crime Context → Identity Marking\nby Year (logistic regression)', fontweight='bold')
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('outputs/fig3_statistical_model.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 3 saved.")

# ─── PRINT SUMMARY TABLE ─────────────────────────────────────────────────────
print("\n=== ODDS RATIO TABLE ===")
print(res_all[['Group','Variable','OR','OR_lo','OR_hi']].to_string(index=False))
print("\n=== YEARLY RATES ===")
print(yearly[['year','minority_rate','nonmin_rate']].to_string(index=False))
print("\nAll figures saved")
