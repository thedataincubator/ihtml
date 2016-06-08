# ihtml

ihtml is a module for [IPython/Jupyter](https://ipython.org/) that allows for the display of HTML within an &lt;iframe&gt;.  This ensures that the displayed HTML exists in its own DOM, and thus cannot disrupt the notebook itself.

## Installation

Simply download the file [ihtml.py](https://raw.githubusercontent.com/thedataincubator/ihtml/master/ihtml.py) from this repo and place it somewhere from which IPython will be able to import it.  Note that IPython adds `~/.ipython/` to the import paths.

## Usage

See the [README.ipynb](https://github.com/thedataincubator/ihtml/blob/master/README.ipynb) notebook for usage examples.  Note that the iframe output is not rendered correctly on Github; view it on your own notebook server to see it in action.
