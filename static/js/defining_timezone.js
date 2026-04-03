let tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (!tz) {
        tz = "UTC"
    }
    document.cookie = "mytz=" + tz + ";path=/";
