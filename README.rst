=========
slt.theme
=========

This package contains theme related files for SLT shopping site.

.. image:: https://secure.travis-ci.org/taito/slt.theme.png
    :target: http://travis-ci.org/taito/slt.theme

Changelog
---------

0.27 (2015-07-24)
=================

- Add dependency to Products.CMFPlacefulWorkflow for test. [taito]
- Implement verkkolasku. [taito]

0.26 (2014-11-29)
===================

- Add css for Site Administrator. [taito]

0.25.2 (2014-09-16)
===================

- Fix method: set_birth_date on class: UserDataPanelAdapter. [taito]

0.25.1 (2014-02-21)
===================

- Use preview for viewlet: shop article listing. [taito]

0.25 (2014-01-08)
=================

- Use Finnish format for birth date. [taito]

0.24 (2013-11-27)
=================

- Add javascript to toggle birth date field. [taito]

0.23.2 (2013-11-22)
===================

- Fix AttributeError for viewlets: collective.cart.shopping.viewlet.order-listing-birth-date and collective.cart.shopping.viewlet.order-listing-registration-number [taito]

0.23.1 (2013-11-12)
===================

- Update style. [taito]
- Cache article listing viewlet. [taito]

0.23 (2013-11-06)
=================

- Fix module name template.py -> view.py [taito]
- Add field: birth date for billing and shipping page. [taito]

0.22 (2013-10-22)
=================

- Test with Plone-4.3.2. [taito]
- Style footer. [taito]
- Enable field for registration number for anonymous. [taito]

0.21.6 (2013-09-04)
===================

- Test with Plone-4.3.1. [taito]
- Fix view: pwreset_finish available for every interfaces. [taito]

0.21.5 (2013-05-27)
===================

- Add upgrade step. [taito]

0.21.4 (2013-05-27)
===================

- Add permission to show stock at add to cart form. [taito]

0.21.3 (2013-05-22)
===================

- Fixed method: class_collapsible for address listing viewlet. [taito]
- Added view: @@members for exporting member information. [taito]

0.21.2 (2013-05-18)
===================

- Updated styles. [taito]

0.21.1 (2013-05-18)
===================

- Refactored viewlets. [taito]

0.21 (2013-05-17)
===================

- Adds order listing related views. [taito]

0.20.3 (2013-05-07)
===================

- Updated views. [taito]

0.20.2 (2013-05-07)
===================

- Updated styles. [taito]

0.20.1 (2013-05-03)
===================

- Added upgrade step. [taito]

0.20 (2013-05-02)
=================

- Lead to @@personal-information after log in to fill those information. [taito]
- Fixed link to order. [taito]

0.19 (2013-05-01)
=================

- Removed dependency from five.grok. [taito]

0.18.2 (2013-04-11)
===================

- Updated translations. [taito]

0.18.1 (2013-04-11)
===================

- Added upgrade step to enable only viewlet: sll.basetheme.footer.info to viewletmanager: plone.portalfooter. [taito]

0.18 (2013-04-11)
=================

- Moved test packages to extras_require. [taito]
- Overrides templates to add registration number. [taito]

0.17 (2013-03-26)
=================

- Applied localization for vat. [taito]

0.16 (2013-03-20)
=================

- Applied localization for money. [taito]

0.15 (2013-03-18)
=================

- Updated translations. [taito]

0.14 (2013-03-18)
=================

- Added field allow_direct_marketing to personal preferences. [taito]
- Redirect to personal preferences after first time login. [taito]
- Tested with Plone-4.2.5. [taito]

0.13 (2013-03-12)
=================

- Covered tests. [taito]

0.12 (2013-03-05)
=================

- Updated for session cart. [taito]

0.11 (2013-02-12)
=================

- Updated order related templates. [taito]

0.10 (2013-02-05)
=================

- Clear created but not processed cart when visiting shop top. [taito]

0.9 (2013-01-31)
================

- Updated order listing view. [taito]

0.8 (2013-01-30)
================

- Updated billing and shipping page. [taito]

0.7 (2013-01-25)
================

- Updated color of article number within cart at portlet. [taito]
- Added billing-info page for different infos against shipping info. [taito]
- Updated color of link on footer. [taito]
- Show byline only to Manager and Site Admin roles. [taito]

0.6.1 (2013-01-16)
==================

- Updated feed order. [taito]

0.6 (2012-12-20)
================

- Added dependency to slt.portlet. [taito]
- Added registration form to override default one. [taito]
- Removed dependency to plone.app.theming. [taito]

0.5.1 (2012-12-12)
==================

- Updated styles for navigation and dependencies. [taito]
- Moved footer message to sll.basetheme package. [taito]

0.5 (2012-11-26)
================

- Added upgrade step to update registry: slt.theme.articles_feed_on_top_page. [taito]

0.4 (2012-11-23)
================

- Added testing integration to Travis CI. [taito]

0.3.2 (2012-11-21)
==================

- Updated templates. [taito]

0.3.1 (2012-11-15)
==================

- Added font family to css. [taito]

0.3 (2012-11-13)
================

- Added template for order listing and address listing. [taito]
- Added viewlet for address. [taito]
- Added dependency to slt.carousel. [taito]

0.2 (2012-11-04)
================

- Added TTW editable footer. [taito]
- Added fallback image. [taito]
- Tested with Plone-4.2.2. [taito]


0.1.1 (2012-10-15)
==================

- Added upgrade step to hide viewlets. [taito]


0.1 (2012-10-15)
================

- Initial release. [taito]
