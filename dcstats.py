import dcid, argparse, json, requests

cache = {}

def get(url):
	if url in cache:
		return cache[url]
	else:
		r = requests.get(url)
		cache[url] = r
		return r

def findPiece(target, start, end, default=None):
	p = target.find(start)
	if p == -1:
		return default
	p += len(start)
	ep = target.find(end, p)
	if ep == -1:
		return default
	return target[p:ep]

def dataForPanel(pid, parents=()):
	tr = {}
	r = get("http://drawception.com/panel/drawing/"+pid+"/-")
	if r.text.find("not be found") != -1:
		return None
	tr["id"] = pid
	if not "artist" in parents:
		tr["artist"] = dataForUser(findPiece(r.text, '<a href="/player/', '/'), parents+("panel",))
	tr["text"] = findPiece(r.text, '<h1>', '</h1>')
	t = int(findPiece(r.text, 'Drawn in ', ' minutes', '0'))*60 + int(findPiece(r.text, ' minutes ', ' seconds', '0'))
	if t > 0:
		tr["time"] = t
	gid = findPiece(r.text, '<a href="/viewgame/', '/')
	if not "game" in parents and gid != None:
		tr["game"] = dataForGame(gid, parents+("panel",))
	if gid != None:
		gr = get("http://drawception.com/viewgame/"+gid+"/-")
		usi = dcid.unscrambleID(pid)
		likesection = findPiece(gr.text, 'like-'+str(usi), '</div>')
		if likesection == None:
			return None
		tr["bonus"] = findPiece(likesection, 'bonusModifier" style="display: none;">', '<')
		tr["likes"] = findPiece(likesection, 'numlikes">', '<')
	return tr

def dataForUser(uid, parents=()):
	tr = {}
	r = get("http://drawception.com/player/"+uid+"/-")
	tr["id"] = uid
	tr["name"] = findPiece(r.text, "og:title\" content=\"", "'")
	tr["level"] = findPiece(r.text, "Level:</b> ", " ")
	return tr

def dataForGame(gid, parents=()):
	tr = {}
	r = get("http://drawception.com/viewgame/"+gid+"/-")
	tr["id"] = gid
	nppt = "panel-number\">"
	npp = r.text.rfind(nppt)+len(nppt)
	tr["numPanels"] = r.text[npp:r.text.find("<", npp)]
	tr["favorites"] = findPiece(r.text, 'numfaves">', '<')
	return tr

def printData(d, ns):
	if d == None:
		return
	if ns.format == None:
		print(json.dumps(d))
	else:
		sp = ns.format.split(",")
		tp = ""
		for x in sp:
			if len(tp) != 0:
				tp += ","
			if x in d:
				tp += str(d[x])
			else:
				tp += "null"
		print(tp)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	typegroup = parser.add_mutually_exclusive_group(required=True)
	typegroup.add_argument('--panel', dest="panelId")
	typegroup.add_argument('--game', dest="gameId")
	parser.add_argument('--csv', dest="format")
	ns = parser.parse_args()
	d = None
	if ns.panelId != None:
		if ns.panelId == "scan":
			while True:
				printData(dataForPanel(dcid.randomID("QD563336", "djZC6336")), ns)
		else:
			d = dataForPanel(ns.panelId)
	elif ns.gameId != None:
		d = dataForGame(ns.gameId)
	if d != None:
		printData(d, ns)
