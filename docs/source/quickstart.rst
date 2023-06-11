Quick Start
===========

.. _Quick Start:

Quick Start (terminal)
----------------------

#. Refer to the :doc:`hardware_setup` to setup the jumpers on your development kit.

#. Call: ``pip install "py_ble_manager[dev] @ git+https://github.com/dialog-semiconductor/py_ble_manager.git`` to install the ``py_ble_manager`` package and its dependencies.

    .. note:: 
      Specifying [dev] will install optional dependency: `prompt_toolkit <https://pypi.org/project/prompt-toolkit/>`_.
      ``prompt_toolkit`` is used in some of the examples to provide a command line interface.

    .. note:: 
      This library requires Python v3.10.5 or later.

#. `Download <https://github.com/Renesas-US-Connectivity/py_ble_manager/tree/main/src/py_ble_manager/util>`_ the py_ble_manager enabled firmware binary to the DA14531 Pro Development kit by calling the ``py_ble_manager_programmer`` utility from the terminal.
    
#. The package is now installed and you are ready to run one of the `examples <https://github.com/Renesas-US-Connectivity/py_ble_manager/tree/main/examples>`_!
