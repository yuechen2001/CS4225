import sys

# Raw occurrence counts (for eligibility filtering)
C_S = {}  # token -> count in Singapore
C_U = {}  # token -> count in United States

# Per-token distinct user sets
U_S_w = {}  # token -> set of distinct SG user IDs who used the token
U_U_w = {}  # token -> set of distinct US user IDs who used the token

# Total distinct users per country
U_S_set = set()  # all distinct SG users
U_U_set = set()  # all distinct US users

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('	')
    if len(parts) != 3:
        continue
    token, type_key, value = parts

    if type_key == 'count_SG':
        C_S[token] = C_S.get(token, 0) + int(value)
    elif type_key == 'count_US':
        C_U[token] = C_U.get(token, 0) + int(value)
    elif type_key == 'user_SG':
        if token == '__TOTAL__':
            U_S_set.add(value)
        else:
            if token not in U_S_w:
                U_S_w[token] = set()
            U_S_w[token].add(value)
    elif type_key == 'user_US':
        if token == '__TOTAL__':
            U_U_set.add(value)
        else:
            if token not in U_U_w:
                U_U_w[token] = set()
            U_U_w[token].add(value)

# Total distinct users per country
U_S = len(U_S_set)
U_U = len(U_U_set)

# Collect all tokens seen
all_tokens = set(C_S.keys()) | set(C_U.keys())

sg_results = []
us_results = []

for token in all_tokens:
    cs = C_S.get(token, 0)
    cu = C_U.get(token, 0)

    # Eligibility filter: same as Task 1, C_S(w) + C_U(w) >= 200
    if cs + cu < 200:
        continue

    # U_S(w) and U_U(w): number of distinct users who used this token
    us_w = len(U_S_w.get(token, set()))
    uu_w = len(U_U_w.get(token, set()))

    # User-normalized frequencies
    q_S = us_w / U_S if U_S > 0 else 0
    q_U = uu_w / U_U if U_U > 0 else 0

    # Add-one smoothing to avoid division by zero
    # Singapore user distinctiveness: D_S^user(w) = q_S(w) / (q_U(w) + 1/U_U)
    D_S = q_S / (q_U + 1 / U_U) if U_U > 0 else 0
    # US user distinctiveness: D_U^user(w) = q_U(w) / (q_S(w) + 1/U_S)
    D_U = q_U / (q_S + 1 / U_S) if U_S > 0 else 0

    sg_results.append((token, us_w, uu_w, D_S))
    us_results.append((token, us_w, uu_w, D_U))

# Sort by distinctiveness descending and select top 12
sg_results.sort(key=lambda x: -x[3])
us_results.sort(key=lambda x: -x[3])

# Output top 12 Singapore-user-distinctive tokens
for token, us_w, uu_w, score in sg_results[:12]:
    print(f"SG_user	{token}	{us_w}	{uu_w}	{score}")

# Output top 12 US-user-distinctive tokens
for token, us_w, uu_w, score in us_results[:12]:
    print(f"US_user	{token}	{us_w}	{uu_w}	{score}")
