Quick Start
===========

.. _Quick Start:

Quick Start (terminal)
----------------------

#. Clone or download this repository

#. Connect the jumpers on the DA14531 Pro Development kit as depicted below:

   .. image:: ../../assets/da14531_pro_kit_jumpers.png

#. Download the GTL enabled :download:`firmware binary <../../firmware/da14531mod_pro_kit.bin>` to the DA14531 Pro Development kit.

#. Open a command prompt or terminal and navigate to the repository on your PC.

#. Setup a virtual environment by calling ``<path_to/py_ble_manager>$ python -m venv ./venv``. Note this library has been tested with Python v3.10.5. 
   To create a virtual environment that uses Python 3.10.5, you must already have Python 3.10.5 downloaded on your computer. To use the above command to create a Python 3.10.5 environment, 
   Python 3.10.5 must be configured in your PATH. You can download it from the `python website <https://www.python.org/downloads/release/python-3105/>`_.

#. Activate the virtual environment. The specific command depends on your operating system. From a windows command prompt call: ``<path_to_venv>\Scripts\activate.bat``

#. Call: ``pip install .`` to install the py_ble_manager package and its dependencies.

#. The package is now installed and you are ready to run one of the [examples](examples)


Quick Start (VS Code)
----------------------

#. Follow steps 1-3 in the `Quick Start`_ section.

#. Open the ``py_ble_manager`` repository directory in VS Code.

#. Setup a virtual environment by calling: ``$ python -m venv ./venv`` from the VS Code terminal. Note this library has been tested with Python v3.10.5. 
   To create a virtual environment that uses Python 3.10.5, you must already have Python 3.10.5 downloaded on your computer. To use the above command to create a Python 3.10.5 environment, 
   Python 3.10.5 must be configured in your PATH. You can download it from the `python website <https://www.python.org/downloads/release/python-3105/>`_.

#. Activate the virtual environment. Hold CTRL+shift+P to open the command palette. Select ``Python: Select Interpreter``. Select the interpreter in the virtual environment you just created (labeled venv).
   Open a new terminal in VS Code and the virtual environment will be activated.

#. Call: ``pip install .`` to install the py_ble_manager package and its dependencies.

#. The package is now installed and you are ready to run one of the `examples <https://github.com/Renesas-US-Connectivity/py_ble_manager/tree/main/examples>`_