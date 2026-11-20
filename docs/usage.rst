=====
Usage
=====

To use qimp in a project::

    import numpy as np

    from qimp.ImageEncoding.Encodings import FRQI
    from qimp.ImageEncoding.QuantumImage import QuantumImage

    image = QuantumImage(np.array([[0, 255], [255, 0]]))
    FRQI(image)

    print(image.circuit)

QImP supports FRQI and NEQR encoding. Import ``NEQR`` from
``qimp.ImageEncoding.Encodings`` and call it with a new ``QuantumImage``:

.. code-block:: python

    from qimp.ImageEncoding.Encodings import NEQR
    from qimp.ImageEncoding.QuantumImage import QuantumImage, generate_example_image

    image = QuantumImage(generate_example_image(side=8))
    NEQR(image)

An image must be a NumPy ``ndarray``. ``QuantumImage`` pads rectangular or non-square
inputs to the smallest square with power-of-two dimensions and supports one optional
zoom factor. Encoding an object a second time raises an exception because an object can
only hold one encoding.

The image encodings are the supported library surface for this package. Translation,
Sobel filtering, the demonstration script, and circuit retrieval remain experimental.
