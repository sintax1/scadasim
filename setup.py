from setuptools import setup

setup(name='scadasim',
      version='0.1',
      description='SCADA Simulator encompassing things from PLCs to devices such as valves, pumps, tanks, etc. and environmental properties such as water pH levels',
      url='https://github.com/sintax1/scadasim',
      author='sintax1',
      author_email='sintax@obscurepacket.org',
      license='MIT',
      packages=['scadasim', 'scadasim.devices', 'scadasim.fluids', 'scadasim.devices', 'scadasim.sensors', 'scadasim.utils', 'tests'],
      zip_safe=False)

