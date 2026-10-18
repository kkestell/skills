# Claude Code Tips and Tricks

## No Free Advertising

Disable Claude's attribution in commits and pull requests:

```json
{
  "includeCoAuthoredBy": false
}
```

See the [attribution settings](https://code.claude.com/docs/en/settings-reference#includecoauthoredby).

## Spinner Verbs

`"mode": "replace"` replaces the default spinner verbs with your own. Use `"append"` to keep the defaults too. Here's my full list:

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": [
      "DISTILLING A CHINESE MODEL",
      "PERPETUAL MOTION IS POWERED BY CUBIC WISDOM",
      "RELOCATING THE EYES OF THE FLOUNDER FISH",
      "GENE RAY IS NOT A CRACKPOT",
      "BE THREE FEET BEHIND YOUR HEAD"
    ]
  }
}
```

## Disable Artifacts

Turn off Claude Code's Artifact tool:

```json
{
  "enableArtifact": false
}
```

See [Disable artifacts](https://code.claude.com/docs/en/artifacts#disable-artifacts).
