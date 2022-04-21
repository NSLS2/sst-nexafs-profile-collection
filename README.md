# UCAL ipython profile

This profile depends on independent packages developed under the 
NSLS-II-SST organization.

To install a new custom package for development, first navigate to the 
package, then:

```bash
source $BS_ENV
pip install -e . --user --no-dependencies
```

If your package has requirements that are not met by the base environment, it is recommended that they be 
installed in a shared overlay. 
```${BS_PYTHONPATH}```

A specific dependency can similarly be installed from github with, for example:
```bash
pip install git+https://github.com/tacaswell/mpl-qtthread --prefix ${BS_PYTHONPATH%/lib*} --upgrade -I --no-dependencies
```