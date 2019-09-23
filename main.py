import re, ics, itertools, arrow
with open("wolverine.in") as in_file:
	sched = in_file.read()
def chunks(x, n):
	for i in range(0, len(x), n):
		yield x[i:i+n]
def not_empty(s):
	return not all(map(str.isspace, s))
def class_calendar():
	cal = ics.Calendar()
	rows = re.split(r"(^\d{2}:\d{2}$)", sched, flags = re.MULTILINE)
	dates = [23,24,25,26,
			23,24,25,26,
			27,
			23,25,
			25,
			27,
			25]
			
	#dates = [row.split("\t")[0] for row in rows[0].splitlines()[1:]]
	#print(dates)
	idx = 0
	for row in rows[2::2]:
		row = tuple(filter(not_empty, row.splitlines()))
		for name, full_name, type_, duration, location in chunks(row, 5):
			def parse_time(time_str):
				# FIXME date before
				nonlocal idx
				time = arrow.get(f"{dates[idx]} {time_str}", "D HH:mm", tzinfo = arrow.now().tzinfo)
				time = time.replace(**{attr: getattr(arrow.now(), attr) for attr in ("year", "month")})
				return time
				# Date doesn't work
				#date = arrow.now().shift(days=-1)
				#date = date[idx]
				#time = arrow.get(time_str, "HH:mm", tzinfo = arrow.now().tzinfo)
				#return date.replace(hour=time.hour, minute=time.minute)
			begin, end = map(parse_time, duration.replace(" ", "").split("-"))
			idx+=1
			print(name)
			print(begin.humanize())
			cal.events.add(ics.Event(name=name+"\n"+full_name, begin = begin, end = end, location = location))
		print()
	return cal

with open("wolverine.cal", "w") as out_file:
	print(class_calendar(), file = out_file)
#print(classes_by_time)
#e.name = "My cool event"
#e.begin = '2014-01-01 00:00:00'
#c.events.add(e)
#c.events
