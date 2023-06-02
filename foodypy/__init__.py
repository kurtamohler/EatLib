from .nutrients import (
    Nutrients,
)

from .database import (
    search,
    get,
    install_database,
    copy_database,
)

# Install database if it hasn't been installed yet
try:
    install_database()
except RuntimeError:
    pass

del nutrients
del database
del error_checking
