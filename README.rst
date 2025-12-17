.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/medialog.officecreate/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/medialog.officecreate/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/medialog.officecreate/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/medialog.officecreate?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/medialog.officecreate/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/medialog.officecreate

.. image:: https://img.shields.io/pypi/v/medialog.officecreate.svg
    :target: https://pypi.python.org/pypi/medialog.officecreate/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/medialog.officecreate.svg
    :target: https://pypi.python.org/pypi/medialog.officecreate
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/medialog.officecreate.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/medialog.officecreate.svg
    :target: https://pypi.python.org/pypi/medialog.officecreate/
    :alt: License


=====================
medialog.officecreate
=====================

Generate Office files in Plone. From templates

Features
--------

- Can be bullet points


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Datagridfield
--------------

        <?xml version='1.0' encoding='utf8'?>
        <model xmlns:i18n="http://xml.zope.org/namespaces/i18n" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns:indexer="http://namespaces.plone.org/supermodel/indexer" xmlns:users="http://namespaces.plone.org/supermodel/users" xmlns:lingua="http://namespaces.plone.org/supermodel/lingua" xmlns="http://namespaces.plone.org/supermodel/schema">
        <schema>
            <field name="table" type="zope.schema.List">
        <description/>
        <title>Table</title>
        <value_type type="collective.z3cform.datagridfield.row.DictRow">
            <schema>medialog.officecreate.interfaces.INameValueRow</schema>
        </value_type>
        <form:widget type="collective.z3cform.datagridfield.datagridfield.DataGridFieldFactory"/>
        </field>
        </schema>
        </model>

        

Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install medialog.officecreate by adding it to your buildout::

    [buildout]

    ...

    eggs =
        medialog.officecreate


and then running ``bin/buildout``


Authors
-------

Provided by awesome people ;)


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/medialog.officecreate/issues
- Source Code: https://github.com/collective/medialog.officecreate
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
