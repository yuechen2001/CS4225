
counts = {}
for line in input_stream:
  country = get_country(line) # Get country of current message
  if country in ['Singapore', 'United States']:
    for token in line.split():
      if token not in counts:
        counts[token] = {'Singapore':0, 'United States':0}
      counts[token][country] += 1

for token in counts:
  cur_counts = counts[token]
  ratio = cur_counts['Singapore'] / (cur_counts['Singapore'] + cur_counts['United States'])
  print(f"{token}\t{ratio}")
