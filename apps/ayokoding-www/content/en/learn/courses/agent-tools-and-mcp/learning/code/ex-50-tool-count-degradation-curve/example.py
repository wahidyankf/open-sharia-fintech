# Learner-owned measurements avoid a universal threshold claim.
counts = (5, 19, 46)
# This local suite records deterministic selection scores.
scores = {5: 1.0, 19: 0.8, 46: 0.5}
# More advertised tools lower this suite's observed score.
assert scores[5] > scores[19] > scores[46]
# Print the measured local curve.
print([(count, scores[count]) for count in counts])
