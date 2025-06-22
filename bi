rm -fv compiled_res_$1/* &&
aapt2 compile -v -o compiled_res_$1/ res-$1/**/*.xml &&
aapt2 link -v -o Phosphor-$1.apk \
    --manifest AndroidManifest-$1.xml \
    -I ~/Android/Sdk/platforms/android-35/android.jar \
    -I framework-res.apk \
    -R compiled_res_$1/*.flat \
    --version-code 1 \
    --version-name 1.0 \
    --target-sdk-version 34 \
    --auto-add-overlay &&
apksigner sign --ks ~/Android/Customization/Unresigned/release.keystore --out Phosphor-$1-signed.apk Phosphor-$1.apk &&
mv -fv Phosphor-$1-signed.apk ph0sphor/system_ext/overlay/Phosphor-$1.apk