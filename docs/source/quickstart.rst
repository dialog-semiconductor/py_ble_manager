Quick Start
===========

#. Refer to the :doc:`hardware_setup` to setup the jumpers on your development kit.

#. Call: ``pip install "py_ble_manager[dev] @ git+https://github.com/dialog-semiconductor/py_ble_manager.git`` to install the ``py_ble_manager`` package and its dependencies.

    .. note:: 
      Specifying [dev] will install optional dependency: `prompt_toolkit <https://pypi.org/project/prompt-toolkit/>`_.
      ``prompt_toolkit`` is used in some of the examples to provide a command line interface.

    .. note:: 
      This library requires Python v3.10.5 or later.

#. :doc:`Download <programming_util>` the py_ble_manager enabled firmware binary to the development kit by calling the ``py_ble_manager_programmer`` utility from the terminal.
    
#. The package is now installed and you are ready to run one of the `examples <https://github.com/dialog-semiconductor/py_ble_manager/tree/main/examples>`_!

.. toctree::
   :maxdepth: 2
   :hidden:
   
   hardware_setup
   programming_util
