<!-- living-code-readme:1 -->
# 🐳 Living Code for Lazydocker

**Calm slate. Living color.** Living Code for Lazydocker: native YAML overrides for active/inactive borders, selected rows and option text in four flavors.

[Installation](#installation) · [Flavors](#flavors) · [Configuration](#configuration) · [All ports](https://github.com/living-code-theme)

## Previews

Real application screenshots have not been captured yet.

## Installation

```sh
git clone https://github.com/living-code-theme/lazydocker.git
cd lazydocker
```

Open your Lazydocker config using the project panel’s **o** action. Merge `gui.theme` from the selected file in `themes/`, replacing existing theme keys while preserving all Docker commands and other settings.

Default locations: Linux `~/.config/lazydocker/config.yml`; macOS `~/Library/Application Support/jesseduffield/lazydocker/config.yml`; Windows `%APPDATA%\lazydocker\config.yml`. Restart Lazydocker after saving.

## Flavors

Expand a flavor for its full-size preview and activation instructions.

<details data-lc-flavor="night">
<summary><strong>Night</strong> · Dark · full palette</summary>

A real application capture is not available yet.

Merge `gui.theme` from `themes/living-code-night.yml` into your config and restart Lazydocker.

</details>

<details data-lc-flavor="frost">
<summary><strong>Frost</strong> · Dark · softer chroma</summary>

A real application capture is not available yet.

Merge `gui.theme` from `themes/living-code-frost.yml` into your config and restart Lazydocker.

</details>

<details data-lc-flavor="paper">
<summary><strong>Paper</strong> · Light · near-white slate</summary>

A real application capture is not available yet.

Merge `gui.theme` from `themes/living-code-paper.yml` into your config and restart Lazydocker.

</details>

<details data-lc-flavor="signal">
<summary><strong>Signal</strong> · Dark · teal accent</summary>

A real application capture is not available yet.

Merge `gui.theme` from `themes/living-code-signal.yml` into your config and restart Lazydocker.

</details>

## Configuration

Only the four exposed theme attributes are changed: `activeBorderColor`, `inactiveBorderColor`, `selectedLineBgColor`, and `optionsTextColor`. Each is the native array of color/style attributes. Active borders are bold. Do not replace your full config with the fragment unless you intentionally want all other settings to return to defaults.

## Compatibility

For Lazydocker’s `gui.theme` attribute API with hex-color support. This is intentionally a partial UI theme: terminal foreground/background, container health labels and other hard-coded colors are not individually configurable by this API. Use a matching Living Code terminal palette. Tests validate native YAML and the exact field contract; no Docker daemon is needed for maintenance.

## Contributing

Found a problem? [Open an issue](https://github.com/living-code-theme/lazydocker/issues/new/choose) with the app version, the flavor and a screenshot. Want Living Code somewhere else? [Request a port](https://github.com/living-code-theme/core/issues/new?template=port-request.yml).

Pull requests are welcome. Keep this README, `port.json` and `images/` in sync, and use real screenshots of the app, never mockups.

🦎 **One chameleon, many habitats.** Part of [Living Code](https://github.com/living-code-theme).

## License

[MIT](LICENSE) © Elliot Luque
