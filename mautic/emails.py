# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .api import API


class Emails(API):
    _endpoint = 'emails'

    def send(self, obj_id):
        """
        Send email to the assigned lists

        :param obj_id: int
        :return: dict|str
        """
        response = self._client.session.post(
            '{url}/{id}/send'.format(
                url=self.endpoint_url, id=obj_id
            )
        )
        return self.process_response(response)

    def send_to_contact(self, obj_id, contact_id):
        """
        Send email to a specific contact

        :param obj_id: int
        :param contact_id: int
        :return: dict|str
        """
        response = self._client.session.post(
            '{url}/{email_id}/contact/{contact_id}/send'.format(
                url=self.endpoint_url, email_id=obj_id, contact_id=contact_id
            )
        )
        return self.process_response(response)
    def create_email(self, name, subject, customHtml, **kwargs):
        """
        Create a new email
        # Check here for more info: https://developer.mautic.org/?json#create-email
        :param name: string
        :param subject: string
        :param customHtml: string
        :param kwargs: other optional parameters for the email
        :return: dict|str
        """
        payload = {
            "name": name,
            "subject": subject,
            "customHtml": customHtml
        }
        payload.update(kwargs)

        response = self._client.session.post(
            '{url}/new'.format(url=self.endpoint_url), json=payload
        )
        return self.process_response(response)

    def get_email(self, email_id):
        """
        Get an individual email by ID

        :param email_id: int
        :return: dict|str
        """
        response = self._client.session.get(
            '{url}/{id}'.format(
                url=self.endpoint_url, id=email_id
            )
        )
        return self.process_response(response)
