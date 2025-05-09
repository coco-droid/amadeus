try:
    # Try absolute import first (when running as installed package)
    from amadeus.cli import app
except ModuleNotFoundError:
    # Fall back to relative import (when running from within the package)
    from cli import app

if __name__ == "__main__":
    app()
