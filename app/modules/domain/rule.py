from collections import defaultdict
from decimal import Decimal
from app.errors import DataError
from .values import number, parts


def evaluate(row):
    start, end = row['始端'], row['末端']
    edges = {}
    for item in parts(row['双向跳接']):
        link, sep, value = item.partition(':')
        a, arrow, b = link.partition('>')
        if not (sep and arrow and a and b) or a == b or (a,b) in edges:
            raise DataError('BUSINESS', f'接续声明冲突 {item}')
        edges[a,b] = number(value,0,100)
    graph = defaultdict(list)
    for (a,b), loss in edges.items():
        if edges.get((b,a)) != loss:
            raise DataError('BUSINESS', f'返向跳接缺失或衰减不符 {a}>{b}')
        graph[a].append(b)
    if start == end:
        raise DataError('BUSINESS', '链路始末端须不同')
    queue = [(start,None)]
    seen, proof = {}, []
    while queue:
        port, previous = queue.pop()
        if port in seen:
            raise DataError('BUSINESS', f'回路端口 {port}')
        seen[port] = previous
        queue.extend((adjacent,port) for adjacent in graph[port] if adjacent != previous)
    if end not in seen:
        raise DataError('BUSINESS', f'链路止于断点，未达 {end}')
    loss, cursor = Decimal(0), end
    while seen[cursor] is not None:
        previous = seen[cursor]
        hop = edges[previous,cursor]
        proof.append((f'{previous} → {cursor}',hop,'dB'))
        loss += hop
        cursor = previous
    if loss > number(row['光损预算'],0,100):
        raise DataError('BUSINESS', f'累计光损 {loss} dB 超预算')
    return loss, list(reversed(proof))
