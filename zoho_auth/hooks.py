app_name = "zoho_auth"
app_title = "Zoho Auth"
app_publisher = "AxelGear"
app_description = "Zoho OAuth2 login for Frappe"
app_email = "rejithr1995@gmail.com"
app_license = "MIT"

# Modern method (Frappe ≥15) – register social login provider
social_login = {
    "Zoho": "zoho_auth.oauth_provider.get_zoho_auth_provider",
}

after_install = "zoho_auth.install.after_install"

doctype_js = {
    "Social Login Key": "public/js/social_login_key_zoho.js",
}
