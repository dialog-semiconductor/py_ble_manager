Quick Start
===========

#. Refer to the :doc:`hardware_setup` to setup the jumpers on your development kit.

#. Call: ``pip install "py-ble-manager[dev]`` to install the ``py_ble_manager`` package and its dependencies.

    .. note:: 
      Specifying [dev] will install optional dependency: `prompt_toolkit <https://pypi.org/project/prompt-toolkit/>`_.
      ``prompt_toolkit`` is used in some of the examples to provide a command line interface.

    .. note:: 
      This library requires Python v3.10.5 or later.

    .. note:: 
      It is recommended to install the library using a virtual environment. 
      To setup a virtual environment using [venv](https://docs.python.org/3/library/venv.html) call: `$ python -m venv ./<name_of_your_env>`. 
      Note to create a virtual environment that uses Python 3.10.5, you must already have Python 3.10.5 downloaded on your computer. 
      To use the above command to create a Python 3.10.5 environment, Python 3.10.5 must be configured in your PATH. 
      You can download it from the [python website](https://www.python.org/downloads/release/python-3105/).

#. :doc:`Download <programming_util>` the py_ble_manager enabled firmware binary to the development kit by calling the ``py_ble_manager_programmer`` utility from the terminal.
    
#. The package is now installed and you are ready to run one of the `examples <https://github.com/dialog-semiconductor/py_ble_manager/tree/main/examples>`_!

.. toctree::
   :maxdepth: 2
   :hidden:
   
   hardware_setup
   programming_util
