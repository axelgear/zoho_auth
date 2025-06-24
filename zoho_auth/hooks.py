# OAuth providers are dynamically loaded from config/oauth_provider.py
# zoho_auth/hooks.py

app_name = "zoho_auth"
app_title = "Zoho Auth"
app_publisher = "AxelGear"
app_description = "Zoho OAuth2 login for Frappe"
app_email = "rejithr1995@gmail.com"
app_license = "MIT"

oauth_providers = [
    {
        "provider_name": "Zoho",
        "provider_logos": {
            "default": "/assets/frappe/images/oauth-logo.png"
        },
        "client_id": "ZOHO_CLIENT_ID",
        "client_secret": "ZOHO_CLIENT_SECRET",
        "authorize_url": "https://accounts.zoho.in/oauth/v2/auth",
        "access_token_url": "https://accounts.zoho.in/oauth/v2/token",
        "api_endpoint": "https://accounts.zoho.in/oauth/user/info",
        "base_url": "https://www.zohoapis.in",
        "redirect_uri": "/api/method/frappe.integrations.oauth2_logins.login_via_oauth2",
        "response_type": "code",
        "scope": "ZohoCRM.modules.ALL",
        "token_params": {
            "grant_type": "authorization_code"
        },
        "icon": "fa fa-key"
    }
]
