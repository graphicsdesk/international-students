from collections import defaultdict
import pandas as pd

# Reads a GSS export, then structures it into a dictionary (represents a tree)
def read_gss(filename, fieldscope='Detailed'):
    if fieldscope not in ['Detailed', 'Broad']:
        raise ValueError('fieldscope attribute must be Detailed or Broad.')

    df = pd.read_csv(filename, header=4, index_col=False, thousands=',')
    df.columns = [
        'Year', 'Institution Name', fieldscope + ' Fields', 'Citizenship', 'Count'
    ]
    df = df.drop('Institution Name', 1) # We assume all data describes Columbia
    df = df[1:-3] # Drop first row (total) annd last 3 rows (footnotes)

    # Re-structure dataframe into a tree
    d = defaultdict(lambda: defaultdict(dict))
    for _, row in df.iterrows():
        year = int(row['Year'])
        field = row[fieldscope + ' Fields']
        citizenship = row['Citizenship']
        d[year][field][citizenship] = row['Count']

    # Return the tree with all unique fields
    return d, df[fieldscope + ' Fields'].unique()

