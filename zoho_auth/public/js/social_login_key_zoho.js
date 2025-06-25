/*
 * Client script for Social Login Key: streamline 'Zoho' preset
 * and lock every field the backend controls.
 */
const ZOHO_LOCKED = [
    "base_url", "authorize_url", "access_token_url",
    "api_endpoint", "redirect_url", "api_endpoint_args",
    "auth_url_data", "icon",
  ];
  
  function lockZoho(frm) {
    const isZoho = frm.doc.provider_name === "Zoho";
    // limit dropdown to 'Zoho'
    frm.set_df_property("provider_name", "options", "\nZoho");
  
    // auto-fill defaults on first select
    if (isZoho && frm.is_new()) {
      frappe.call({
        method: "zoho_auth.api.get_default_provider_values",
        callback(r) {
          Object.entries(r.message).forEach(([k, v]) => frm.set_value(k, v));
        },
      });
    }
  
    // toggle read-only
    ZOHO_LOCKED.forEach(f => frm.set_df_property(f, "read_only", isZoho));
  }
  
  frappe.ui.form.on("Social Login Key", {
    onload: lockZoho,
    provider_name: lockZoho,
  });
  