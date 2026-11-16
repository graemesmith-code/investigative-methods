# Rabbit update cards: useful headlines

16 November 2026

The latest-update cards now lead with what a researcher can do with the records. Each card contains the original addition date and time, followed by one short sentence. The whole card opens the full update. Status labels and repeated “See the update” text have been removed.

| Full update title | Homepage headline |
| --- | --- |
| NIH ExPORTER annual project and linked-data files | Follow US public money into medical research. |
| Grants.gov daily full opportunity extract | See what the US government is offering to fund. |
| AER ST1 historical well-licence lists and amendments | Trace changes to Alberta’s oil and gas well licences. |

Future homepage headlines should explain a useful research possibility in everyday language. Avoid product abbreviations, file formats and administrative labels. Keep the claim within the source’s actual coverage: funding opportunities are not awards, and well licences are not proof of drilling.

The original source names, technical descriptions, evidence links, identifiers and approval records remain in the full updates. Addition timestamps remain 16 November 2026 at 13:28 Central European Time; changing a headline does not reset them. The approved catch case study is unchanged.

A researcher should be able to see why a collection might matter before learning what its publisher calls it. The details still matter; they belong one click away.

## Technical note

Display headlines are keyed by proposal identifier in `app/living-ui.tsx`. The source records and release events are unchanged. Cards retain their exact `/changes#change-<proposal-id>` targets, semantic time elements, and visible keyboard focus. Styling in `app/gateway.css` underlines only the headline on hover or focus. Keep this public-facing copy separate from personal investigation notes.
