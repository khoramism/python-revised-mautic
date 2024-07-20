================================
 Mautic Python
================================

A Python wrapper for the Mautic API utilizing `requests-oauthlib <https://github.com/requests/requests-oauthlib>`_.

Installation
------------

To install this package, use the following command:

.. code-block:: bash

    pip install git+https://github.com/khoramism/python-revised-mautic.git

Quickstart
----------

1. Enter your Mautic API credentials in ``apitester/oauth2_app.py``.

2. Run the Flask app to obtain an OAuth2 token:

   .. code-block:: bash

       python apitester/oauth2_app.py

   This will generate a ``creds.json`` file in a temporary directory, allowing you to start using the Mautic API.

Usage
-----

To interact with the Mautic API:

.. code-block:: python

    from python_mautic import MauticOauth2Client, Contacts
    from python_mautic.utils import read_token_tempfile

    # Load the OAuth2 token
    token = read_token_tempfile()

    # Initialize the Mautic client
    mautic = MauticOauth2Client(base_url='<base URL>', client_id='<Mautic Public Key>', token=token)
    
    # Create a Contacts instance
    contacts = Contacts(client=mautic)
    
    # Fetch and print the list of contacts
    print(contacts.get_list())

Example: Working with Contacts and Segments
-------------------------------------------

.. code-block:: python

    from mautic import MauticOauth2Client, Contacts, Segments
    from mautic.utils import read_token_tempfile
    import json

    client_id = 'CLIENT_ID'
    client_secret = 'CLIENT_SECRET'
    base_url = 'https://mautic.example.com'

    # Load the OAuth2 token
    token = read_token_tempfile()

    # Initialize the Mautic client
    mautic = MauticOauth2Client(base_url=base_url, client_id=client_id, token=token)
    contacts = Contacts(client=mautic)
    segments = Segments(client=mautic)

    def get_segment_id(segment_name: str) -> int:
        """
        Retrieves the ID for a given segment by name.

        :param segment_name: The name of the segment.
        :return: The ID of the segment.
        """
        all_segments = segments.get_list()
        for segment in all_segments.values():
            if segment['alias'] == segment_name:
                return segment['id']

    def contact_id_in_segment(segment: str):
        """
        Retrieves all contact IDs within a specified segment.

        :param segment: The segment name.
        :return: A tuple containing a list of contact IDs and the total count.
        """
        all_contacts = []
        start, batch_size = 0, 30
        while True:
            response = contacts.get_list(search=f'segment:{segment}', start=start, limit=batch_size)
            batch_contacts = response.get("contacts", {})
            if not batch_contacts:
                break
            all_contacts.extend(batch_contacts.keys())
            start += batch_size
        return all_contacts, len(all_contacts)

    def remove_contact_from_segment(client_ids: list, segment_id: int):
        """
        Removes specified contacts from a segment.

        :param client_ids: List of contact IDs to remove.
        :param segment_id: The segment ID.
        """
        for client_id in client_ids:
            segments.remove_contact(segment_id, client_id)

        # Optional: Verify removal and attempt again if necessary.
        all_client_ids, total = contact_id_in_segment(segment_id)
        
        if total != 0:
            remove_contact_from_segment(all_client_ids, total, segment_id=segment_id)
    
