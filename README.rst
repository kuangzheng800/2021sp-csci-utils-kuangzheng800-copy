========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |appveyor| |requires|
        |
        | |codeclimate|
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.com/csci-e-29/2021sp-csci-utils-kuangzheng800.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/csci-e-29/2021sp-csci-utils-kuangzheng800

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/csci-e-29/2021sp-csci-utils-kuangzheng800?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/csci-e-29/2021sp-csci-utils-kuangzheng800

.. |requires| image:: https://requires.io/github/csci-e-29/2021sp-csci-utils-kuangzheng800/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/csci-e-29/2021sp-csci-utils-kuangzheng800/requirements/?branch=master

.. |codeclimate| image:: https://codeclimate.com/github/csci-e-29/2021sp-csci-utils-kuangzheng800/badges/gpa.svg
   :target: https://codeclimate.com/github/csci-e-29/2021sp-csci-utils-kuangzheng800
   :alt: CodeClimate Quality Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/csci-e-29/2021sp-csci-utils-kuangzheng800/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/csci-e-29/2021sp-csci-utils-kuangzheng800/compare/v0.0.0...master



.. end-badges

CSCI utils assignment project

* Free software: MIT license

Installation
============

::

    pip install csci-utils

You can also install the in-development version with::

    pip install https://github.com/csci-e-29/2021sp-csci-utils-kuangzheng800/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import csci_utils
    csci_utils.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
