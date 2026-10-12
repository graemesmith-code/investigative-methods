"""Compare already-attributed claims under four reviewed, version-specific contracts.

This module does not establish attribution, translate documents, or infer intent.
All money and production arithmetic uses Decimal; missing data blocks a result.
"""
from decimal import Decimal, InvalidOperation


class Blocked(ValueError):
    pass


def number(value):
    if isinstance(value, (bool, type(None))):
        raise Blocked("missing or invalid number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise Blocked("invalid number") from None
    if not result.is_finite():
        raise Blocked("non-finite number")
    return result


def overlaps(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def require(condition, reason):
    if not condition:
        raise Blocked(reason)


def assess(case, observation, manifest):
    result = {"case_id": case["id"], "project": case["project"],
              "status": "blocked", "reason": None}
    try:
        require(observation["case_id"] == case["id"], "wrong case")
        require(observation["schema_version"] == 1, "unknown observation format")
        require(observation["context"] == case["required_context"],
                "period, entity, metric, basis, or attribution differs from approved scope")
        require(all(observation["gates"].get(g) is True for g in case["required_gates"]),
                "missing or failed comparability gate")
        expected = {sid: manifest[sid]["sha256"] for sid in case["source_ids"]}
        require(observation["source_hashes"] == expected,
                "source version changed or evidence missing: review required")
        values = observation["values"]
        kind = case["comparison"]["kind"]
        if kind == "production_interval":
            mines = values["western_thousand_lb"]
            require(set(mines) == {"Toquepala", "Cuajone"}, "incomplete or extra mine population")
            quantities = [number(x) for x in mines.values()]
            host = number(values["host_fine_tonnes"])
            require(all(q >= 0 for q in quantities) and host >= 0, "negative production")
            factor = Decimal("0.45359237")  # 1,000 lb to metric tonnes, exact
            centre = sum(quantities) * factor
            width = len(quantities) * factor  # one display unit per mine, conservative
            a, b = (centre - width, centre + width), (host, host)
            result.update(unit="fine metric tonnes", western_interval=list(map(str, a)),
                          host_interval=list(map(str, b)))
            agreement = overlaps(a, b)
        elif kind == "royalty_fx_interval":
            cells = values["company_cells"]
            required = {(s, r) for s in ("34.1", "34.5", "34.8") for r in (27, 42)}
            require(len(cells) == 6 and {(c["sheet"], c["row"]) for c in cells} == required,
                    "royalty basket must contain six unique company cells")
            amounts = []
            for c in cells:
                initial, adjustment, final = map(number, (c["initial"], c["adjustment"], c["final"]))
                require(adjustment == 0 and initial == final,
                        "reconciled value changed: company adoption needs review")
                require(final >= 0, "negative/refund component: aggregate FX bound invalid")
                amounts.append(final)
            low_rate, high_rate = map(number, values["fx_xof_per_usd"])
            require(Decimal("0") < low_rate <= high_rate, "invalid exchange-rate range")
            require([str(low_rate), str(high_rate)] == case["comparison"]["approved_fx_xof_per_usd"],
                    "exchange-rate evidence changed")
            western = number(values["western_usd"])
            require(western >= 0, "negative Western total")
            total = sum(amounts)
            # One display unit for each of six XOF cells and for the USD total.
            a = (max(Decimal(0), total - len(cells)) / high_rate,
                 (total + len(cells)) / low_rate)
            b = (max(Decimal(0), western - 1), western + 1)
            result.update(unit="USD", host_xof=str(total), host_interval=list(map(str, a)),
                          western_interval=list(map(str, b)))
            agreement = overlaps(a, b)
        elif kind == "ownership_all_dates":
            dates = case["comparison"]["admissible_dates"]
            parties = case["comparison"]["parties"]
            host = values["host_percent"]
            western = values["western_percent_by_date"]
            require(set(host) == set(parties) and set(western) == set(dates),
                    "ownership parties or admissible dates missing")
            outcomes = []
            for date in dates:
                require(set(western[date]) == set(parties), "missing Western ownership party")
                matching = True
                for party in parties:
                    a, b = number(host[party]), number(western[date][party])
                    require(0 <= a <= 100 and 0 <= b <= 100, "ownership outside 0–100 percent")
                    matching = matching and a == b
                outcomes.append({"date": date, "consistent": matching})
            result["date_checks"] = outcomes
            if any(o["consistent"] for o in outcomes) and not all(o["consistent"] for o in outcomes):
                raise Blocked("date ambiguity affects outcome: at least one interpretation is consistent")
            agreement = all(o["consistent"] for o in outcomes)
        else:
            raise Blocked("unsupported comparison")
        result["status"] = "consistent" if agreement else "contradiction_candidate"
        result["reason"] = ("Claims are compatible within the approved scope and tolerances."
                            if agreement else "Claims are incompatible under the approved contract; verify extraction and amendments before reporting.")
    except (Blocked, KeyError, TypeError, ValueError, InvalidOperation) as exc:
        result.update(status="blocked", reason=str(exc))
    return result
