# -*- coding: utf-8 -*-
"""
MD DaVis: A python package to analyze molecular dynamics trajecotires
          of proteins

Usage:
  md_davis <command> [<args>...]
  md_davis -h | --help
  md_davis -v | --version

Options:
  -h, --help        Show this screen.
  -v, --version     Show version.

Available Commands:
  sequence          get the sequence from a PDB file
  plot              plotting commands
  plot_dipoles      plot commands
  create            create HDF5 files
  electrostatics    Commands for calculating surface electrostatic
                    pontential using Delphi and MSMS
  collect           collect data from various calculations into one
                    HDF binary file
  landscape         Make energy landscapes
"""

import sys
import subprocess
from docopt import docopt

from . import __version__

def main():
    """Console script entrypoint for md_davis."""
    args = docopt(__doc__,
                  version=__version__,
                  options_first=True)

    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'collect':
        from . import collect
        collect.main(argv=argv)

    elif args['<command>'] == 'contacts':
        from .utils import contacts
        contacts.main(argv=argv)

    elif args['<command>'] == 'hbonds':
        from .utils import hbonds
        hbonds.main(argv=argv)

    elif args['<command>'] == 'sequence':
        from .structure import sequence
        sequence.main(argv=argv)

    elif args['<command>'] == 'surface':
        from .structure import surface
        surface.main(argv=argv)

    elif args['<command>'] == 'electrostatics':
        from .electrostatics import surface_electrostatics
        surface_electrostatics.main(argv=argv)

    elif args['<command>'] == 'residue':
        if len(args['<args>']) > 1:
            if args['<args>'][0] == 'dataframe':
                import md_davis.collect_data.create_residue_dataframe as res_df
                arguments = docopt(res_df.__doc__, argv=argv)
                res_df.main(arguments)
                return
            if args['<args>'][0] == 'aligned':
                import md_davis.collect_data.create_aligned_residue_dataframe as res_aligned_df
                res_aligned_df.main(argv=argv)
                return
        print('Invalid command. The available commands are:')
        print('  md_davis residue dataframe')
        print('  md_davis residue aligned')


    elif args['<command>'] == 'plot':
        if len(args['<args>']) < 1:
            print('Choose a plotting command')
            return
        if args['<args>'][0] == 'xvg':
            from .plotting import plot_xvg
            plot_xvg.main(argv=argv)
        elif args['<args>'][0] == 'dipoles':
            from .plotting import plot_dipoles
            plot_dipoles.main(argv=argv)
        elif args['<args>'][0] == 'rmsd_rg':
            from .plotting import plot_rmsd_rg
            plot_rmsd_rg.main(argv=argv)
        elif args['<args>'][0] == 'residue':
            import md_davis.plotting.plot_residue_dataframe
            arguments = docopt(
                doc = md_davis.plotting.plot_residue_dataframe.__doc__,
                argv = argv
            )
            md_davis.plotting.plot_residue_dataframe.main(arguments)
        else:
            pass
    elif args['<command>'] == 'landscape':
        if len(args['<args>']) > 1:
            if args['<args>'][0] == 'rmsd_rg':
                from .landscape import rmsd_rg_landscape
                rmsd_rg_landscape.main(argv=argv)
                return
            if args['<args>'][0] == 'animation':
                from .landscape import landscape_animation
                landscape_animation.main(argv=argv)
                return
        print('Invalid command. The available commands are:')
        print('  md_davis landscape rmsd_rg')
        print('  md_davis landscape animation')
    else:
        exit("%r is not a md_davis command. See 'md_davis --help'." % args['<command>'])
    return


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
