import click
import logging
import pandas as pd
from astropy.coordinates import SkyCoord
from astroutils.logger import setupLogger
from pathlib import Path

logger = logging.getLogger(__name__)

PACKAGE_ROOT = Path(__file__).parent.parent

@click.command()
@click.option('-f', '--csv', type=click.Path(), help="CSV file containing beam locations")
@click.option('-B', '--band', type=click.Choice(['low', 'mid', 'high']), help='Choice of RACS band to query beam footprint')
@click.argument('ra')
@click.argument('dec')
def main(band, ra, dec, csv):

    setupLogger(verbose=True)

    unit = 'hourangle' if ':' in ra or 'h' in ra else 'deg'
    source = SkyCoord(ra=ra, dec=dec, unit=(unit, 'deg'))


    if csv:
        logger.info(f"Using beam locations at:\n{csv}")
    else:
        logger.info(f"Defaulting to RACS {band} beam and field footprint.")

        if source.dec.degree < -70:
            logger.warning(f"Southern fields may have different rotation to RACS footprint")

        csv = PACKAGE_ROOT / f'racs_{band}_beams.csv'

    beams = pd.read_csv(PACKAGE_ROOT / csv)
    bcoords = SkyCoord(ra=beams.RA_DEG, dec=beams.DEC_DEG, unit='deg')

    beams['d2d'] = source.separation(bcoords).deg

    logger.info(f"\n{beams.sort_values('d2d')}")

if __name__ == '__main__':
    main()
