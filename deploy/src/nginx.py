from io import StringIO

from pyinfra import host
from pyinfra.operations import apt, files

from facts import IsInstalled

def __install():
    """
    Ensures that nginx is installed.
    
    __install ensures that nginx is installed by using the IsInstalled
    fact to query for the package with dpkg.

    Returns:
        None
    """

    if not host.get_fact(IsInstalled, package_name="nginx"):
        apt.packages(packages=["nginx"], present=True)

def site_from_string(name: str, src: StringIO, enable: bool = False):
    """
    Creates a new nginx site from a string.

    Uploads the contents of src to /etc/nginx/sites-available/{name}.
    If you would like to create a site from a file, use site_from_file.

    Args:
        name: The name of the file in /etc/nginx/sites-available/.
        src: The contents of the site configuration file.
        enable: Whether to enable the site after creating it.
    """

    # Ensure that nginx is installed
    __install()

    files.put(
        name=f"Nginx site {name} available",
        src=src,
        dest=f"/etc/nginx/sites-available/{name}",
    )

    if enable:
        enable_site(name)

def site_from_file(name: str, src: str, enable: bool = False):
    """
    Creates a new nginx site from a file.

    Uploads the file to /etc/nginx/sites-available/{name}.
    If you would like to create a site from a string, use site_from_string.

    Args:
        name: The name of the file in /etc/nginx/sites-available/.
        src: The path to the file to upload.
        enable: Whether to enable the site after creating it.
    """

    __install()

    files.put(
        name=f"Nginx site {name} available",
        src=src,
        dest=f"/etc/nginx/sites-available/{name}",
    )

    if enable:
        enable_site(name)

def enable_site(name: str):
    """
    Enables an nginx site.

    Creates a symlink from /etc/nginx/sites-enabled/{name} to
    /etc/nginx/sites-available/{name}.

    Args:
        name: The name of the site to enable.
    """

    __install()

    files.symlink(
        name=f"Nginx site {name} enabled",
        path=f"/etc/nginx/sites-enabled/{name}",
        target=f"/etc/nginx/sites-available/{name}",
    )
