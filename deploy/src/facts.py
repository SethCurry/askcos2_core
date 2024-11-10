from pyinfra.api import FactBase

class IsInstalled(FactBase):
    '''
    Checks whether a given package is installed with apt
    '''

    def command(self, package_name: str):
        return f"dpkg -s {package_name}; echo $?"
    
    def process(self, output: str):
        return output.splitlines()[-1] == "0"
