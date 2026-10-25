# Lossless recovery transport for intact public consumer outputs

These nine binary parts encode four registers already published in full. They are duplicate representations, not additional observations, candidates, awards or dollars. No private source archives, article bodies, credentials or private notes are included.

`transport-manifest.json` gives the original relative path, byte count and SHA256; the combined deterministic gzip byte count/hash; and every ordered part’s size/hash. Each part is at most4MiB. All parts and all four recovered original files have been verified byte-for-byte by hash.

From the package directory, run:

```sh
python3 code/recovery_transport.py restore --destination /absolute/recovery-output
```

The command checks each part, concatenated gzip and recovered original before installation. An existing output with different bytes is not overwritten. With no destination, it verifies without installing another copy.

This transport recovers the intact consumer registers. It does not claim equivalence to the unavailable independent13267-key Stage1 package. The two workflows used different screens and denominators.
