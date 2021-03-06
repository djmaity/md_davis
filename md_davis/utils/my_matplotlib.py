import matplotlib
from matplotlib.ticker import FuncFormatter

def set_latex_font():
    """ Set Latex use in matplotlib and load my font customization """
    font = {'family' : 'serif',
            'weight' : 'bold',
            'size'   : 12}
    matplotlib.rc('font', **font)

    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.rc('text', usetex=True)
    matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']


def sci_format(x, pos):
    """ Scientific notation formatter function """
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)


SCI_FMT = FuncFormatter(sci_format)


def plot_structure_counts(axes, counts, scale=1):
    """ Plot the stacked bar graph for the secondary structure counts """
    labels = [r'\textbf{$\alpha$-helix}',
              r'\textbf{$3_{10}$ helix}',
              r'\textbf{$\pi$-helix}',
              r'\textbf{residue in isolated $\beta$-bridge}',
              r'\textbf{$\beta$ strand}',
              r'\textbf{hydrogen bonded turn}',
              r'\textbf{bend}',
              r'\textbf{loop or irregular}',
              ]
    alpha = 0.4
    colors = [(1, 0, 0, alpha), (1, 0, 1, alpha), (0, 0, 1, alpha), (0, 1, 0, alpha), 
              (0, 1, 1, alpha), (1, 1, 0, alpha), (0, 0, 0, alpha), (0.8, 0.8, 0.8, alpha)]
    width = 1
    cumulative = counts[0] * scale
    ind = list(range(len(cumulative)))
    axes.bar(ind, cumulative, width, label=labels[0], fc=colors[0],
             ec=(0, 0, 0, 0))
    for i in range(1, 8):
        axes.bar(ind, counts[i] * scale, width, bottom=cumulative,
                 label=labels[i], fc=colors[i], ec=(0, 0, 0, 0))
        cumulative = cumulative + (counts[i] * scale)
    axes.set_xlim(-0.5, ind[-1] + 1)


def plot_with_matplotlib():
    font = {'family' : 'serif',
            'weight' : 'bold',
           }
    matplotlib.rc('font', **font)
    matplotlib.rc('text', usetex=True)
    matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']

    if len(counts) > 1:
        fig, axes = plt.subplots(len(counts), 1, sharey=True)
        axis = axes.flatten()
        fig.set_size_inches(8, 2.5*len(counts) + 1)
    else:
        fig, axes = plt.subplots(1, 1, sharey=True)
        axis = [axes]
        fig.set_size_inches(8, 4.5)

    for i, count in enumerate(counts):
        plot_structure_counts(axis[i], count)
        handles, lbs = axis[i].get_legend_handles_labels()

    axis[-1].set_xlabel(r'\textbf{Residue Numbers}')
    lgd = axis[0].legend(handles, lbs, ncol=4, frameon=False, loc='lower center', bbox_to_anchor=(0.5, 1.0))
    fig.text(0.05, 0.5, r'\textbf{\% of Frames with Specified Secondary Structure}',
             rotation='vertical', va='center')
    
    if args.output:
        fig.savefig(args.output, dpi=600, bbox_extra_artists=([lgd]), bbox_inches='tight')
    else:
        plt.show()