def scrape_norm():
    soup = get_soup_from_html('../in/daily_norm.html')
    body = soup.body

    norm = []
    for p in body.find_all('p'):
        group = p.get_text()
        tb = p.find_next_sibling('table')
        for i, tr in enumerate(tb.find_all('tr')):
            if i == 0: continue
            heap = tr.get_text().strip().split()
            u = heap.pop()
            q = heap.pop()
            name = " ".join(heap)
            norm.append((group, name, q, u))
    if norm:
        save_json('norm.json', norm)
