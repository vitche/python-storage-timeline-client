from setuptools import setup

setup(
    name='storage_timeline_client',
    version='1.7',
    description='Python Storage.Timeline client',
    author='Vitche Research Team Developer',
    author_email='developer@vitche.com',
    py_modules=['storage_timeline_client'],
    install_requires=['python-dotenv',
                      'wasm_storage_timeline @ git+https://github.com/vitche/wasm_storage_timeline.git'
    ]
)
