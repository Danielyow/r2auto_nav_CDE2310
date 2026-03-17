from setuptools import setup

package_name = 'simple_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nus',
    maintainer_email='nus@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'r2mover = simple_nav.r2mover:main',
            'r2moverotate = simple_nav.r2moverotate:main',
            'r2scanner = simple_nav.r2scanner:main',
            'r2occupancy = simple_nav.r2occupancy:main',
            'r2occupancy2 = simple_nav.r2occupancy2:main',
            'r2auto_nav = simple_nav.r2auto_nav:main',
            'frontier_detector = simple_nav.frontier_detector:main',
            'lidar_tester = simple_nav.lidar_tester:main',
            'navigator = simple_nav.navigator:main',
        ],
    },
)
