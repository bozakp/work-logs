import datetime
import collections

def line_sets(lines):
    start = 0
    while start < len(lines):
        stop = start+1
        while stop < len(lines) and lines[stop][0] != "=":
            stop += 1
        yield lines[start:stop]
        start = stop

with open("tab_history.log", "r") as f:
    lines = f.readlines()

# Get count of tabs opened vs minute of day
hmmap = collections.defaultdict(int)
for ls in line_sets(lines):
    n_new_tabs = sum(1 if l[0] == "+" else 0 for l in ls[1:])
    dt = datetime.datetime.fromtimestamp(float(ls[0][1:]))
    hms = "%02d:%02d" % (dt.hour, dt.minute)
    hmmap[hms] += n_new_tabs

for hour in xrange(24):
    for minute in xrange(60):
        hms = "%02d:%02d" % (hour, minute)
        #print("%s,%d" % (hms, hmmap[hms]))

# Get count of tabs opened vs day of week
dwmap = collections.defaultdict(int)
for ls in line_sets(lines):
    n_new_tabs = sum(1 if l[0] == "+" else 0 for l in ls[1:])
    dt = datetime.datetime.fromtimestamp(float(ls[0][1:]))
    dwmap[dt.weekday()] += n_new_tabs

# Find length of day by determining the difference between the first entry and
# last entry on each calendar day
start_dt = datetime.datetime(1970, 1, 1)
prev_ls = ["=0"]
times = dict()
for ls in line_sets(lines):
    dt = datetime.datetime.fromtimestamp(float(ls[0][1:]))
    prev_dt = datetime.datetime.fromtimestamp(float(prev_ls[0][1:]))
    delta = dt - prev_dt
    # if idle for an hour, assume not working
    if delta.seconds > 3600 or delta.days > 0:
        s = str(prev_dt.date())
        diff = prev_dt - start_dt
        if s in times:
            times[s] += diff
        else:
            times[s] = diff
        start_dt = dt
    prev_ls = ls
# aggregate by month
for month in xrange(1, 13):
    matching = []
    for time in times:
        t = datetime.datetime.strptime(time, "%Y-%m-%d")
        if t.month == month:
            matching.append(times[time].seconds)
    if len(matching) > 0:
        print("Month %02d" % month)
        print("\tAverage: %.2f" % (float(sum(matching) / len(matching)) / 3600))
        print("\tSum:     %.2f" % (float(sum(matching)) / 3600))
# aggregate by day
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for dow in xrange(7):
    matching = []
    for time in times:
        t = datetime.datetime.strptime(time, "%Y-%m-%d")
        if t.date().weekday() == dow:
            matching.append(times[time].seconds)
    if len(matching) > 0:
        print(day_names[dow])
        print("\tAverage: %.2f" % (float(sum(matching) / len(matching)) / 3600))
        print("\tSum:     %.2f" % (float(sum(matching)) / 3600))

for dow in xrange(7):
    print("%s,%d" % (day_names[dow], dwmap[dow]))
