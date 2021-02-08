def getTime(t):
	m, s = divmod(t, 60)
	h, m = divmod(m, 60)

	return '{:02d}h{:02d}m{:02d}s'.format(int(h), int(m), int(s))