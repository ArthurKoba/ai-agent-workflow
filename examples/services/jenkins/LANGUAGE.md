# Jenkins UI language and theme

The validated Jenkins setup used the **Locale** and **Dark Theme** plugins.

Jenkins otherwise follows browser/user locale and theme preferences, which can produce mixed-language administration screens and inconsistent screenshots/runbooks.

## Install the plugins

Go to:

```text
Manage Jenkins → Plugins → Available plugins
```

Install:

```text
Locale
Dark Theme
```

If the Locale controls do not appear immediately, restart Jenkins after plugin installation is complete and no jobs are running.

## Validated language configuration

Go to:

```text
Manage Jenkins → Appearance
```

Under **Default Language**, set:

```text
Default Language: English - en
Ignore browser preference and force this language to all users: enabled
Allow all users to use their own language preference: enabled
```

This is the exact configuration observed in the validated deployment.

The first option keeps Jenkins administration consistently English by default. The second still allows an individual user preference to override the global default where Jenkins/plugin support permits it.

## Validated theme configuration

The observed global theme settings were:

```text
Global theme: Light
Do not allow users to select a different theme: disabled
```

The **Dark Theme** plugin was installed and enabled. Individual users were allowed to select another theme; the validated administrator session itself rendered dark while the global default remained Light.

Therefore do not interpret the global `Light` value as a requirement that every user sees a light UI.

## Prism syntax highlighting

The observed syntax-highlighting theme was:

```text
Default (light and dark mode)
```

## Why keep this explicit

For shared administration:
- keep menu names in one documented language;
- avoid mixed-language screenshots and runbooks;
- allow personal theme preference without changing the global baseline;
- document both global defaults and per-user override behavior.
