import typing

from pyinfra import host
from pyinfra.operations import apt, server

from facts import IsInstalled

def __install():
    if not host.get_fact(IsInstalled, package_name="certbot"):
        apt.packages(packages=["certbot"], present=True)

def get_certs(email_address: str, webroot_path: str, domain_names: typing.List[str]):
    __install()

    certbot_command = "certbot certonly"

    # Set the email address so that we aren't prompted for it
    certbot_command += f" --email {email_address}"

    # Automatically agree to the terms of service
    certbot_command += " --agree-tos"

    # Use the webroot plugin to verify the domain ownership
    certbot_command += f" --webroot --webroot-path {webroot_path}"

    # Add all of the domain names
    for domain_name in domain_names:
        certbot_command += f" -d {domain_name}"

    server.shell(
        name="Get Let's Encrypt certs",
        commands=[certbot_command],
    )
