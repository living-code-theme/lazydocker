import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import { resolveAll } from '../scripts/palette.mjs';
import { keys, hexColors, assertContrast } from './helpers.mjs';
const fixture = JSON.parse(await readFile(new URL('./fixtures/upstream.json', import.meta.url)));
const read = path => readFile(new URL('../' + path, import.meta.url), 'utf8');
import YAML from 'yaml';

for (const f of resolveAll()) test(f.name + ': Lazydocker native attribute arrays', async () => {
  const t = YAML.parse(await read('themes/' + f.slug + '.yml'));
  keys(t, ['gui']); keys(t.gui, ['theme']); keys(t.gui.theme, fixture.colors);
  const attributes = t.gui.theme;
  for (const values of Object.values(attributes)) {
    assert.ok(Array.isArray(values)); assert.match(values[0], /^#[a-f0-9]{6}$/);
    assert.ok(values.slice(1).every(value => ['bold', 'reverse', 'underline'].includes(value)));
  }
  assert.deepEqual(attributes.activeBorderColor, [f.r('borderActive'), 'bold']);
  assert.deepEqual(attributes.inactiveBorderColor, [f.r('fgMuted')]);
  assert.deepEqual(attributes.selectedLineBgColor, [f.r('selection')]);
  assert.deepEqual(attributes.optionsTextColor, [f.r('link')]);
});
