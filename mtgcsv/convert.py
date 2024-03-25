"""
Convert between various MTG CSV formats.

Usage:
  convert.py <input> <output> <format>

Options:
  -h, --help     Show this screen.
  -v, --version  Show version.

Arguments:
  <input>        Input CSV.
  <output>       Output CSV filepath.
  <format>       Output format.
"""
import pandas as pd
from docopt import Dict, docopt
from mapper import QUANTITY, NAME, SETNAME, FOIL, IS_FOIL

def main(args: Dict) -> None:
    """
    Covert between various MTG CSV formats.
    """
    df = pd.read_csv(args['<input>']).dropna(axis='columns')

    if args['<format>'].lower() == "cardkingdom":
        out = to_cardkingdom(df)
        out.to_csv(args['<output>'], index=False, header=False)

def to_cardkingdom(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert to Card Kingdom CSV.
    """
    for col in df.columns:
        if col in NAME:
            name = col
        elif col in SETNAME:
            setname = col
        elif col in FOIL:
            foil = col
        elif col in QUANTITY:
            quantity = col
    df.loc[df[foil].isin(IS_FOIL), foil] = "true"
    df.loc[~df[foil].isin(IS_FOIL), foil] = "false"

    return df[[name, setname, foil, quantity]]


if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.0.1")
    main(arguments)