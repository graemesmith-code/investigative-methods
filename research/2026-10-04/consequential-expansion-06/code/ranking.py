"""Order next-check readiness. Heterogeneous source scores never enter the key."""
def readiness_key(row):
    return row['readiness_tier'], row['effort_tier'], row['test_id']
