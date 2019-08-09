# Changelog

## 1.1.0

* Added support for a few more portions of the `text` section:

    * instruction_code
    * transaction_type_code
    * exchange_rate
    * sending_institution
    * sender_charges
    * receiver_charges

  Big thanks to [Broto](https://github.com/bbroto06) again for reporting the
  problem.


## 1.0.1

* Bugfix [#3](https://github.com/danielquinn/mt103/issues/3): account for
application headers for outgoing messages, MUR values containing spaces, and
trailer sections containing `{}`.  Thanks to [Broto Bhattacharjee](https://github.com/bbroto06)
for the report!


## 1.0.0

* Changed the nature of the `.user_header` attribute from a string to a
  `UserHeader` object.  This new object has the same string representation
  (`str(mt103.user_header)`), but now also possesses new sub-attributes.
* Added support for user header fields including `bank_priority_code` (`bpc`),
  `message_user_reference` (`mur`), `service_type_identifier` (`sti`), and
  `unique_end_to_end_transaction_reference` (`uetr`).


## 0.0.1

Initial release.
