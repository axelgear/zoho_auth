from __future__ import annotations
import json
from typing import Dict

import frappe
import requests
from frappe import _
from frappe.utils.oauth import get_oauth_keys, get_redirect_uri, login_oauth_user


def _endpoints(provider: str) -> tuple[str, str]:
    """Return (token_url, userinfo_url) based on *current* Social Login Key."""
    doc = frappe.get_doc("Social Login Key", provider)
    base = doc.base_url.rstrip("/")
    return (
        f"{base}/oauth/v2/token",
        f"{base}/oauth/v2/userinfo",
    )


def _log_and_bail(title: str, msg: str, http_status: int = 400):
    frappe.log_error(title=title, message=msg)
    frappe.respond_as_web_page("Zoho Login Failed", msg, http_status_code=http_status)


@frappe.whitelist(allow_guest=True)
def login_via_zoho(code: str, state: str):
    provider = "zoho"

    # ------------------------------------------------------------------ 1  credentials
    try:
        keys = get_oauth_keys(provider)
        client_id, client_secret = keys["client_id"], keys["client_secret"]
    except Exception:
        _log_and_bail("Zoho OAuth2", "Client credentials not configured", 500)
        return

    redirect_uri = get_redirect_uri(provider)

    # ------------------------------------------------------------------ 2  redeem code
    token_url, userinfo_url = _endpoints(provider)
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        tok_res = requests.post(token_url, data=payload, timeout=15)
        tok_res.raise_for_status()
    except Exception:
        _log_and_bail("Zoho OAuth2", f"Token request failed\n{tok_res.text if 'tok_res' in locals() else ''}")
        return

    tok = tok_res.json()
    access_token, id_token_jwt = tok.get("access_token"), tok.get("id_token")
    if not access_token:
        _log_and_bail("Zoho OAuth2", f"Access token missing\n{json.dumps(tok, indent=2)}")
        return

    # ------------------------------------------------------------------ 3  fetch profile
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    try:
        ui_res = requests.get(userinfo_url, headers=headers, timeout=15)
        ui_res.raise_for_status()
        info: Dict = ui_res.json()
    except Exception:
        _log_and_bail("Zoho OAuth2", f"Userinfo fetch failed\n{ui_res.text if 'ui_res' in locals() else ''}")
        return

    # fallback: decode id_token for email if /userinfo missed it
    if "email" not in info and id_token_jwt:
        try:
            import jwt as pyjwt
            info.update(pyjwt.decode(id_token_jwt, options={"verify_signature": False}))
        except Exception:
            frappe.log_error("Zoho OAuth2", "Failed to decode id_token")

    email = (
        info.get("email") or info.get("primary_email") or info.get("EmailId")
        or info.get("preferred_username")
    )
    if not email:
        _log_and_bail("Zoho OAuth2", f"Email missing in payload\n{json.dumps(info, indent=2)}", 417)
        return

    display = info.get("name") or info.get("display_name") or ""
    data = {
        "email": email,
        "first_name": display.split(" ")[0],
        "last_name": " ".join(display.split(" ")[1:]),
        "id": info.get("ZUID") or email,
        "sub": info.get("sub") or info.get("ZUID") or email,
        "email_verified": True,
    }

    # ------------------------------------------------------------------ 4  hand off to Frappe
    login_oauth_user(data, provider=provider, state=state)


@frappe.whitelist()
def get_default_provider_values():
    """Helper for the form script (prefill when choosing 'Zoho')."""
    base = "https://accounts.zoho.com"
    return {
        "base_url": base,
        "authorize_url": f"/oauth/v2/auth",
        "access_token_url": f"/oauth/v2/token",
        "api_endpoint": f"/oauth/v2/userinfo",
        "redirect_url": "/api/method/zoho_auth.api.login_via_zoho",
        "auth_url_data": json.dumps({
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
        }),
        "icon": "https://www.zohowebstatic.com/sites/zweb/images/favicon.ico",
    }


@frappe.whitelist(allow_guest=True)
def zoho_login(code: str, state: str):
    """Legacy alias – keeps old redirect URIs working."""
    return login_via_zoho(code, state)
