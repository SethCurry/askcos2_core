from pyinfra import host
from pyinfra.operations import apt, server

from facts import IsInstalled

def __install():
    # Bail out early if docker is already installed
    if host.get_fact(IsInstalled, package_name="docker-ce"):
        return

    apt.packages(packages=["ca-certificates", "curl"])

    server.shell(
        name="Get Docker GPG key and add repository",
        commands=[
            "install -m 0755 -d /etc/apt/keyrings",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
            "chmod a+r /etc/apt/keyrings/docker.asc",
            "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable\" > /etc/apt/sources.list.d/docker.list"
        ]
    )

    apt.packages(name="Install Docker",
                 packages=["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"])

def allow_user_to_use_docker(user: str):
    __install()

    server.user(name=f"Add user {user} to Docker group",
                user=user,
                groups=["docker"])
