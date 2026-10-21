// Lazydocker exposes four theme attributes. Other UI colors belong to the host terminal.
export function generate(flavors) {
  return flavors.map(f => ({ path: `themes/${f.slug}.yml`, content:
    '# Merge gui.theme into the existing lazydocker config; preserve other options.\n' +
    `gui:\n  theme:\n    activeBorderColor:\n      - "${f.r('borderActive')}"\n      - bold\n` +
    `    inactiveBorderColor:\n      - "${f.r('fgMuted')}"\n` +
    `    selectedLineBgColor:\n      - "${f.r('selection')}"\n` +
    `    optionsTextColor:\n      - "${f.r('link')}"\n`,
  }));
}
