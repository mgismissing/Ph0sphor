import phosphor as ph

overlay = ph.Overlay("com.android.systemui", "PhosphorSystemUI", "com.morph3us.ph0sphor.ui", True, 999)

overlay.link_resource(ph.ResourceTarget("string", "sec_quick_settings_flashlight_label"), ph.Resource("string", "qs_flashlight", "Flashbang"))

print(overlay.overlays)