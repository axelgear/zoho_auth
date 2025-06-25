"""
Dynamic provider descriptor for Frappe ≤14 (old social_login hook).
Pull everything from the Social Login Key so you never mix Zoho
data-centres after an admin change.
"""
from __future__ import annotations
import frappe


def get_zoho_auth_provider():
    if not frappe.db.exists("Social Login Key", "zoho"):
        return []

    doc = frappe.get_doc("Social Login Key", "zoho")

    return [
        {
            "provider_name": "Zoho",
            "provider_logos": {"default": "/assets/frappe/images/oauth-logo.png"},
            "client_id": doc.client_id,
            "client_secret": doc.client_secret,
            "authorize_url": doc.authorize_url,
            "access_token_url": doc.access_token_url,
            "api_endpoint": doc.api_endpoint,
            "base_url": doc.base_url,
            "redirect_url": doc.redirect_url,
            "response_type": "code",
            "scope": "openid email profile",
            "icon": doc.icon,
        }
    ]
