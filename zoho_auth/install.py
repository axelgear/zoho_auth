import json
import frappe


def after_install():
    """Seed a disabled Social Login Key named 'zoho' if it doesn't exist."""
    if frappe.db.exists("Social Login Key", "zoho"):
        return

    doc = frappe.new_doc("Social Login Key")
    doc.name = "zoho"
    doc.provider_name = "Zoho"
    doc.social_login_provider = "Custom"
    doc.enable_social_login = 0          # admin will flip later

    # *** pick ONE data-centre and keep it everywhere ***
    base = "https://accounts.zoho.com"   # or .in / .eu / .com.cn …

    doc.base_url = base
    doc.authorize_url = f"{base}/oauth/v2/auth"
    doc.access_token_url = f"{base}/oauth/v2/token"
    doc.api_endpoint = f"{base}/oauth/v2/userinfo"
    doc.redirect_url = "/api/method/zoho_auth.api.login_via_zoho"  # site-relative works too
    doc.icon = "https://www.zohowebstatic.com/sites/zweb/images/favicon.ico"

    doc.auth_url_data = json.dumps({
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    })

    doc.insert(ignore_permissions=True, ignore_mandatory=True)
    frappe.db.commit()
