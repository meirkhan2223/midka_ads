#!/usr/bin/env python3
"""ADS Midterm Judge. Іске қосу: python3 judge.py  -> http://localhost:8000
Керек: Python 3.8+, C++ үшін g++ (орнатылған болуы керек)."""
import re, random, math, sys, os, json, subprocess, tempfile, time, shutil, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

TL = 3  # time limit, секунд
ints = lambda s: list(map(int, s.split()))
L = lambda a: ' '.join(map(str, a))
def size(r, k, lo, hi, mx): return lo if k == 1 else (r.randint(lo, hi) if k == 0 else mx)

PB = {}; ORDER = []
def P(id, grp, title, lvl, topic, text, ex, gen, sol):
    PB[id] = dict(id=id, grp=grp, title=title, lvl=lvl, topic=topic, text=text, ex=ex, gen=gen, sol=sol); ORDER.append(id)

# ---------- BST helper ----------
def bst(vals):
    V = [vals[0]]; Lc = [-1]; Rc = [-1]; D = [1]
    for v in vals[1:]:
        c = 0; d = 1
        while True:
            d += 1
            if v < V[c]:
                if Lc[c] < 0: Lc[c] = len(V); break
                c = Lc[c]
            else:
                if Rc[c] < 0: Rc[c] = len(V); break
                c = Rc[c]
        V.append(v); Lc.append(-1); Rc.append(-1); D.append(d)
    return V, Lc, Rc, D
def gbst(r, k, extra=False):
    n = size(r, k, 1, 12, 500)
    v = r.sample(range(1, 10**9), n)
    if k == 2 and r.random() < .5: v.sort(reverse=r.random() < .5)
    s = f"{n}\n{L(v)}\n"
    return s + (f"{r.randint(1, n)}\n" if extra else "")

# ---------- 1A delete ----------
def g1a(r, k):
    n = size(r, k, 1, 10, 100000); R = 5 if k == 2 else 3
    a = [r.randint(-R, R) for _ in range(n)]; x = r.choice(a)
    if all(v == x for v in a): a[0] = x + 1
    return f"{n}\n{L(a)}\n{x}\n"
def s1a(s):
    t = ints(s); n = t[0]; return L([v for v in t[1:n+1] if v != t[n+1]])
P('1A', 'V1', 'Delete nodes', 'easy', 'Linked list',
  "Singly linked list. Given n integers and x, delete all nodes with value x and print the remaining list.\nInput: n (1<=n<=1e5); n integers; x (at least one element != x).\nOutput: remaining numbers separated by spaces.",
  ["6\n1 2 3 2 4 2\n2\n", "3\n5 6 7\n9\n"], g1a, s1a)

# ---------- 1B isqrt ----------
def g1b(r, k):
    if k == 1: ms = [10**18, 10**18 - 1, 1]
    else:
        ms = []
        for _ in range(size(r, k, 3, 8, 20000)):
            c = r.random()
            v = (lambda q: q*q + r.choice([-1, 0, 1]))(r.randint(1, 10**9)) if c < .3 else r.randint(1, 10**18) if c < .6 else r.randint(1, 100)
            ms.append(min(max(v, 1), 10**18))
    return f"{len(ms)}\n{L(ms)}\n"
s1b = lambda s: '\n'.join(str(math.isqrt(m)) for m in ints(s)[1:])
P('1B', 'V1', 'Integer square root', 'medium', 'Binary search on answer',
  "For each m find floor(sqrt(m)): the largest r with r*r <= m. Use binary search on the answer (float sqrt is not precise for 1e18).\nInput: t (1<=t<=2e4); t integers m_i (1<=m_i<=1e18).\nOutput: floor(sqrt(m_i)) for each, one per line.",
  ["3\n16 17 1\n", "1\n1000000000000000000\n"], g1b, s1b)

# ---------- 1C build heap ----------
def g1c(r, k):
    n = size(r, k, 2, 12, 100000); R = 10**9 if k == 2 else 6
    return f"{n}\n{L([r.randint(-R, R) for _ in range(n)])}\n"
def s1c(s):
    n, *a = ints(s); a = [0] + a[:n]
    for i in range(n // 2, 0, -1):
        j = i
        while 2*j <= n:
            c = 2*j
            if c + 1 <= n and a[c+1] > a[c]: c += 1
            if a[c] > a[j]: a[c], a[j] = a[j], a[c]; j = c
            else: break
    return L(a[1:])
P('1C', 'V1', 'Build max-heap (sift down)', 'hard', 'Heap / heap sort',
  "Build a max-heap bottom-up. Children of i are 2i and 2i+1 (1-indexed). Sift down i: while i has a child, take the child c with the larger value (left if equal); if a_c > a_i swap and i=c, else stop. Apply to i = n/2 (floor) down to 1.\nInput: n (1<n<1e5); n integers.\nOutput: the array after building the heap.",
  ["5\n1 5 9 4 6\n", "3\n2 7 7\n"], g1c, s1c)

# ---------- 2A reverse ----------
def g2a(r, k):
    n = size(r, k, 1, 10, 100000); return f"{n}\n{L([r.randint(-10**9, 10**9) for _ in range(n)])}\n"
s2a = lambda s: L(ints(s)[1:][::-1])
P('2A', 'V2', 'Reverse a list', 'easy', 'Linked list',
  "Build a singly linked list from n integers, reverse it by changing the links, print it.\nInput: n (1<=n<=1e5); n integers.\nOutput: the reversed list separated by spaces.",
  ["5\n1 2 3 4 5\n", "1\n42\n"], g2a, s2a)

# ---------- 2B binary search ----------
def g2b(r, k):
    n = size(r, k, 1, 10, 100000); q = size(r, k, 1, 10, 100000); hi = 10**9 if k == 2 else 15
    a = sorted(r.randint(1, hi) for _ in range(n))
    xs = [r.randint(1, hi) if r.random() < .5 else r.choice(a) for _ in range(q)]
    return f"{n}\n{L(a)}\n{q}\n{L(xs)}\n"
def s2b(s):
    t = ints(s); n = t[0]; st = set(t[1:n+1]); return '\n'.join('YES' if x in st else 'NO' for x in t[n+2:])
P('2B', 'V2', 'Is it in the array?', 'easy', 'Binary search',
  "Sorted array of n integers and q queries. For each x print YES if x occurs, else NO. Linear scan is too slow: use binary search.\nInput: n (1<=n<=1e5); sorted a_i (1<=a_i<=1e9); q (1<=q<=1e5); q integers x_j.\nOutput: YES/NO for each query, one per line.",
  ["5\n1 3 3 7 10\n4\n3 4 10 1\n", "1\n5\n2\n5 6\n"], g2b, s2b)

# ---------- 2C sort students desc ----------
def g2c(r, k):
    n = size(r, k, 1, 8, 100000); al = 'abcdefghijklmnopqrstuvwxyz' if k == 2 else 'abc'
    rows = [(''.join(r.choice(al) for _ in range(r.randint(1, 10 if k == 2 else 3))), r.randint(0, 100 if k == 2 else 4)) for _ in range(n)]
    return f"{n}\n" + ''.join(f"{a} {b}\n" for a, b in rows)
def s2c(s):
    t = s.split(); n = int(t[0]); rows = [(t[1+2*i], int(t[2+2*i])) for i in range(n)]
    return '\n'.join(f"{a} {b}" for a, b in sorted(rows, key=lambda x: (-x[1], x[0])))
P('2C', 'V2', 'Sort students (comparator)', 'medium', 'Quick sort / heap sort',
  "Sort n students (name, score) by score descending; equal scores by name ascending. Implement quick sort or heap sort with a comparator.\nInput: n (1<=n<=1e5); n lines 'name score' (name: 1..10 lowercase letters, score 0..100).\nOutput: sorted students, one per line, same format.",
  ["4\nbob 90\nalice 95\ncarl 90\ndave 70\n", "2\nzed 50\namy 50\n"], g2c, s2c)

# ---------- 3A insert ----------
def g3a(r, k):
    n = size(r, k, 1, 10, 100000); a = [r.randint(-10**9, 10**9) for _ in range(n)]
    p = r.choice([0, n]) if k == 1 else r.randint(0, n)
    return f"{n}\n{L(a)}\n{p} {r.randint(-10**9, 10**9)}\n"
def s3a(s):
    t = ints(s); n = t[0]; a = t[1:n+1]; p, x = t[n+1], t[n+2]; return L(a[:p] + [x] + a[p:])
P('3A', 'V3', 'Insert a node', 'easy', 'Linked list',
  "Insert a new node with value x so that it gets position p (from 0; 0 = new head, n = new tail). Print the list.\nInput: n (1<=n<=1e5); n integers (list head to tail); p and x (0<=p<=n).\nOutput: the n+1 numbers separated by spaces.",
  ["4\n1 2 4 5\n2 3\n", "1\n7\n0 9\n"], g3a, s3a)

# ---------- 3B BST height ----------
P('3B', 'V3', 'BST height', 'medium', 'Binary search tree',
  "Insert n numbers one by one into an empty BST (smaller -> left, otherwise right). Print the height: number of nodes on the longest root-to-leaf path (single node = 1).\nInput: n (1<=n<=500); n distinct integers (1..1e9).\nOutput: the height.",
  ["5\n5 3 8 1 4\n", "4\n1 2 3 4\n"], gbst, lambda s: str(max(bst(ints(s)[1:])[3])))

# ---------- 3C stable merge sort ----------
def g3c(r, k):
    n = size(r, k, 1, 10, 100000); al = 'abcdefghijklmnopqrstuvwxyz'
    return f"{n}\n" + ''.join(f"{''.join(r.choice(al) for _ in range(r.randint(1, 4)))} {r.randint(1, 5)}\n" for _ in range(n))
def s3c(s):
    t = s.split(); n = int(t[0]); rows = [(t[1+2*i], int(t[2+2*i])) for i in range(n)]
    return '\n'.join(a for a, b in sorted(rows, key=lambda x: x[1]))
P('3C', 'V3', 'Stable merge sort', 'medium', 'Merge sort',
  "Sort students (name, grade) by grade ascending using a STABLE sort (equal grades keep input order). Merge sort takes from the left half on ties.\nInput: n (1<=n<=1e5); n lines 'name grade' (name: 1..10 lowercase letters, grade 1..5).\nOutput: names in sorted order, one per line.",
  ["5\nann 3\nbob 1\ncat 3\ndan 2\neve 1\n", "3\nx 5\ny 5\nz 5\n"], g3c, s3c)

# ---------- 4A gcd lcm ----------
def g4a(r, k):
    if k == 1: return r.choice(["1 1\n", "1000000000 999999999\n", "1000000000 1000000000\n"])
    hi = 10**9 if k == 2 else 100
    return f"{r.randint(1, hi)} {r.randint(1, hi)}\n"
def s4a(s):
    a, b = ints(s); g = math.gcd(a, b); return f"{g} {a // g * b}"
P('4A', 'V4', 'GCD and LCM', 'easy', 'Euclidean algorithm',
  "Find gcd(a, b) and lcm(a, b) using the Euclidean algorithm. lcm can reach 1e18: use 64-bit (long long).\nInput: a b (1<=a,b<=1e9).\nOutput: gcd and lcm separated by a space.",
  ["12 18\n", "7 5\n"], g4a, s4a)

# ---------- 4B preorder ----------
def s4b(s):
    V, Lc, Rc, _ = bst(ints(s)[1:]); st = [0]; o = []
    while st:
        u = st.pop(); o.append(V[u])
        if Rc[u] >= 0: st.append(Rc[u])
        if Lc[u] >= 0: st.append(Lc[u])
    return L(o)
P('4B', 'V4', 'BST preorder', 'medium', 'Binary search tree',
  "Insert n numbers one by one into an empty BST (smaller -> left, otherwise right). Print the preorder traversal: root, left subtree, right subtree.\nInput: n (1<=n<=500); n distinct integers (1..1e9).\nOutput: n numbers in preorder separated by spaces.",
  ["6\n5 3 8 1 4 9\n", "3\n3 2 1\n"], gbst, s4b)

# ---------- 4C merge ----------
def g4c(r, k):
    n = size(r, k, 1, 8, 100000); m = size(r, k, 1, 8, 100000); R = 10**9 if k == 2 else 9
    a = sorted(r.randint(-R, R) for _ in range(n)); b = sorted(r.randint(-R, R) for _ in range(m))
    return f"{n}\n{L(a)}\n{m}\n{L(b)}\n"
def s4c(s):
    t = ints(s); n = t[0]; m = t[n+1]; return L(sorted(t[1:n+1] + t[n+2:n+2+m]))
P('4C', 'V4', 'Merge two sorted arrays', 'easy', 'Merge sort (merge)',
  "Merge two non-decreasing arrays into one sorted array of length n+m using the merge procedure with two pointers (do not sort again).\nInput: n; n integers; m; m integers (n,m<=1e5, values -1e9..1e9).\nOutput: merged array separated by spaces.",
  ["3\n1 4 7\n4\n2 4 5 9\n", "1\n5\n1\n5\n"], g4c, s4c)

# ---------- 5A sieve ----------
def g5a(r, k):
    return f"{r.choice([1, 2]) if k == 1 else r.choice([10**6, 999983, 500000]) if k == 2 else r.randint(1, 100)}\n"
def s5a(s):
    n = int(s); 
    if n < 2: return '0'
    sv = bytearray([1]) * (n + 1); sv[0] = sv[1] = 0
    for i in range(2, int(n**.5) + 1):
        if sv[i]: sv[i*i::i] = bytearray(len(range(i*i, n + 1, i)))
    return str(sum(sv))
P('5A', 'V5', 'Count primes', 'easy', 'Sieve of Eratosthenes',
  "Count the primes p <= n using the sieve of Eratosthenes.\nInput: n (1<=n<=1e6).\nOutput: the number of primes not exceeding n.",
  ["10\n", "20\n"], g5a, s5a)

# ---------- 5B BST leaves ----------
def s5b(s):
    V, Lc, Rc, _ = bst(ints(s)[1:]); return str(sum(1 for i in range(len(V)) if Lc[i] < 0 and Rc[i] < 0))
P('5B', 'V5', 'BST leaves', 'medium', 'Binary search tree',
  "Insert n numbers one by one into an empty BST (smaller -> left, otherwise right). Count the leaves (nodes without children).\nInput: n (1<=n<=500); n distinct integers (1..1e9).\nOutput: the number of leaves.",
  ["5\n5 3 8 1 4\n", "4\n1 2 3 4\n"], gbst, s5b)

# ---------- 5C check min-heap ----------
def g5c(r, k):
    n = size(r, k, 1, 10, 100000); hi = 10**9 if k == 2 else 20
    a = sorted(r.randint(1, hi) for _ in range(n))
    if n > 1 and r.random() < .5:
        i, j = r.randrange(n), r.randrange(n); a[i], a[j] = a[j], a[i]
    return f"{n}\n{L(a)}\n"
def s5c(s):
    n, *a = ints(s); a = [0] + a[:n]
    return 'YES' if all(a[i] <= a[c] for i in range(1, n + 1) for c in (2*i, 2*i + 1) if c <= n) else 'NO'
P('5C', 'V5', 'Is it a min-heap?', 'easy', 'Binary heap',
  "Array a_1..a_n stores a binary heap: children of i are 2i and 2i+1 (if <= n). It is a min-heap if every element is <= each of its children. Check it.\nInput: n (1<=n<=1e5); n integers (1..1e9).\nOutput: YES or NO.",
  ["6\n1 3 2 7 4 5\n", "4\n2 1 3 4\n"], g5c, s5c)

# ---------- V6 and Oth Var ----------
def gops(r, k, a, d):
    n = size(r, k, 2, 12, 100000); ops = []; c = 0
    for i in range(n):
        if c > 0 and i > 0 and r.random() < .45: ops.append(d); c -= 1
        else: ops.append(f"{a} {r.randint(1, 10**9 if k == 2 else 20)}"); c += 1
    if all(o != d for o in ops): ops[-1] = d
    return f"{n}\n" + '\n'.join(ops) + '\n'
def s6a(s):
    q = []; h = 0; o = []
    for l in s.split('\n')[1:]:
        if l.startswith('push'): q.append(l.split()[1])
        elif l.startswith('pop'): o.append(q[h]); h += 1
    return '\n'.join(o)
P('6A', 'V6', 'Queue', 'easy', 'Queue',
  "Empty queue, n operations: 'push x' adds x to the end; 'pop' removes the front element and prints it.\nInput: n (1<=n<=1e5); n lines: 'push x' (1<=x<=1e9) or 'pop'. Queue is never empty at pop; at least one pop.\nOutput: each popped number on a separate line.",
  ["5\npush 3\npush 7\npop\npush 1\npop\n", "3\npush 10\npop\npush 20\n"], lambda r, k: gops(r, k, 'push', 'pop'), s6a)

import bisect
def s6b(s):
    t = ints(s); n = t[0]; a = t[1:n+1]
    return '\n'.join(str(bisect.bisect_left(a, x) + 1 if bisect.bisect_left(a, x) < n else -1) for x in t[n+2:])
P('6B', 'V6', 'Lower bound', 'medium', 'Binary search',
  "Sorted array of n integers and q queries. For each x find the smallest index i (from 1) with a_i >= x, or -1 if all elements are < x. Use binary search.\nInput: n (1<=n<=1e5); sorted a_i (1..1e9); q (1<=q<=1e5); q integers x_j (1..1e9).\nOutput: the answer for each query, one per line.",
  ["5\n1 3 3 7 10\n4\n3 4 11 1\n", "3\n2 2 2\n2\n2 1\n"], g2b, s6b)

import heapq
def s6c(s):
    n, *a = ints(s); h = [-v for v in a[:n]]; heapq.heapify(h)
    while len(h) > 1:
        y = -heapq.heappop(h); x = -heapq.heappop(h)
        if y != x: heapq.heappush(h, -(y - x))
    return str(-h[0] if h else 0)
def g6c(r, k):
    n = size(r, k, 1, 10, 100000); R = 10**9 if k == 2 else 20
    return f"{n}\n{L([r.randint(1, R) for _ in range(n)])}\n"
P('6C', 'V6', 'Last stone', 'medium', 'Heap / priority queue',
  "n stones with weights a_i. While there are >= 2 stones, take the two heaviest x <= y and smash them: if x = y both are destroyed, otherwise x is destroyed and the other becomes y - x. Print the weight of the last stone (0 if none). Use a max-heap.\nInput: n (1<=n<=1e5); n integers (1..1e9).\nOutput: the last stone's weight or 0.",
  ["6\n2 7 4 1 8 1\n", "2\n5 5\n"], g6c, s6c)

def s_o1(s):
    t = ints(s); n = t[0]; a = t[1:n+1]
    return '\n'.join(str(bisect.bisect_right(a, x) - bisect.bisect_left(a, x)) for x in t[n+2:])
P('O1', 'Oth Var', 'Count occurrences', 'medium', 'Binary search (lower/upper bound)',
  "Sorted array of n integers and q queries. For each x print how many times x occurs. Use lower bound and upper bound.\nInput: n (1<=n<=1e5); sorted a_i (1..1e9); q (1<=q<=1e5); q integers x_j (1..1e9).\nOutput: the count for each query, one per line.",
  ["7\n1 2 2 2 5 5 9\n4\n2 5 3 9\n", "1\n4\n1\n4\n"], g2b, s_o1)

def s_o2(s):
    n, *a = ints(s); a = [0] + a[:n]; p = a[n]; i = 0
    for j in range(1, n):
        if a[j] < p: i += 1; a[i], a[j] = a[j], a[i]
    a[i+1], a[n] = a[n], a[i+1]
    return L(a[1:])
def g_o2(r, k):
    n = size(r, k, 1, 10, 100000); R = 10**9 if k == 2 else 6
    return f"{n}\n{L([r.randint(-R, R) for _ in range(n)])}\n"
P('O2', 'Oth Var', 'Lomuto partition', 'medium', 'Quick sort (partition)',
  "Perform exactly one Lomuto partition and print the array: pivot p = a_n, i = 0; for j = 1..n-1: if a_j < p then i++ and swap a_i, a_j; finally swap a_{i+1} and a_n.\nInput: n (1<=n<=1e5); n integers (-1e9..1e9).\nOutput: the array after the partition, separated by spaces.",
  ["6\n3 9 1 8 2 4\n", "3\n2 7 7\n"], g_o2, s_o2)

def g_o3(r, k):
    n = size(r, k, 1, 10, 100000); R = 10**9 if k == 2 else 8
    return f"{n}\n{L([r.randint(-R, R) for _ in range(n)])}\n{r.randint(1, n)}\n"
P('O3', 'Oth Var', 'k-th smallest', 'medium', 'Quick sort / quickselect',
  "Find the k-th smallest element (position k, from 1, after sorting non-decreasingly). Use quick sort, heap sort or quickselect.\nInput: n (1<=n<=1e5); n integers (-1e9..1e9); k (1<=k<=n).\nOutput: the k-th smallest element.",
  ["5\n7 2 9 2 5\n3\n", "1\n-4\n1\n"], g_o3, lambda s: str(sorted(ints(s)[1:-1])[ints(s)[-1] - 1]))

def s_o4(s):
    h = []; o = []
    for l in s.split('\n')[1:]:
        if l.startswith('add'): heapq.heappush(h, -int(l.split()[1]))
        elif l.startswith('extract'): o.append(str(-heapq.heappop(h)))
    return '\n'.join(o)
P('O4', 'Oth Var', 'Priority queue', 'medium', 'Binary heap (insert / extract max)',
  "Max priority queue, initially empty, n operations: 'add x' inserts x; 'extract' removes the largest number and prints it. Use a binary heap.\nInput: n (1<=n<=1e5); n lines 'add x' (1<=x<=1e9) or 'extract'. Queue is never empty at extract; at least one extract.\nOutput: each extracted number on a separate line.",
  ["6\nadd 5\nadd 1\nadd 9\nextract\nadd 7\nextract\n", "3\nadd 4\nadd 4\nextract\n"], lambda r, k: gops(r, k, 'add', 'extract'), s_o4)

# ---------- Extra (own problems, same topics) ----------
def ge1(r, k):
    n = size(r, k, 1, 8, 100000); p = [1] + r.sample(range(2, n + 1), n - 1) if n > 1 else [1]
    nx = [0] * (n + 1)
    for i in range(n - 1): nx[p[i]] = p[i + 1]
    nx[p[-1]] = r.choice([0, p[r.randrange(n)]])
    return f"{n}\n{L(nx[1:])}\n"
def se1(s):
    n, *a = ints(s); seen = set(); u = 1
    while u:
        if u in seen: return 'YES'
        seen.add(u); u = a[u-1]
    return 'NO'
P('E1', 'Extra', 'Cycle in a linked list', 'medium', 'Linked list',
  "A linked list is given by array nxt: node i points to nxt_i (0 = end of list). Starting from node 1, determine whether the list has a cycle (you reach a node twice). Use O(1) extra memory if you can (Floyd).\nInput: n (1<=n<=1e5); n integers nxt_i (0<=nxt_i<=n).\nOutput: YES if there is a cycle, else NO.",
  ["4\n2 3 4 2\n", "3\n2 3 0\n"], ge1, se1)

P('E2', 'Extra', 'k-th smallest in BST', 'medium', 'Binary search tree',
  "Insert n numbers into an empty BST (smaller -> left, otherwise right). Print the k-th smallest value (inorder traversal).\nInput: n (1<=n<=500); n distinct integers; k (1<=k<=n).\nOutput: the k-th smallest value.",
  ["5\n5 3 8 1 4\n2\n", "1\n7\n1\n"], lambda r, k: gbst(r, k, True),
  lambda s: str(sorted(ints(s)[1:-1])[ints(s)[-1] - 1]))

def ge3(r, k):
    n = size(r, k, 1, 10, 100000); R = 10**4 if k == 2 else 20
    return f"{n} {r.randint(1, n)}\n{L([r.randint(1, R) for _ in range(n)])}\n"
def se3(s):
    t = ints(s); n, k = t[:2]; a = t[2:2+n]; lo, hi = max(a), sum(a)
    while lo < hi:
        m = (lo + hi) // 2; c = 1; cur = 0
        for v in a:
            if cur + v > m: c += 1; cur = v
            else: cur += v
        if c <= k: hi = m
        else: lo = m + 1
    return str(lo)
P('E3', 'Extra', 'Split array', 'hard', 'Binary search on answer',
  "Split an array of n positive integers into exactly k non-empty contiguous parts so that the largest part sum is as small as possible. Print that minimum. (Binary search on the answer + greedy check.)\nInput: n k (1<=k<=n<=1e5); n integers (1..1e4).\nOutput: the minimal possible largest sum.",
  ["5 2\n7 2 5 10 8\n", "3 3\n1 2 3\n"], ge3, se3)

KZ = {}
KZ['1A'] = "Бір бағытты байланысқан тізім (singly linked list). n бүтін сан және x саны берілген. Мәні x-ке тең барлық түйіндерді (node) өшіріп, қалған тізімді шығар.\nКіріс: n (1<=n<=1e5); n бүтін сан (тізім басынан аяғына дейін); x. Кемінде бір элемент x-ке тең емес.\nШығыс: қалған сандар ретімен, бос орынмен бөлініп."
KZ['1B'] = "Әр m саны үшін floor(sqrt(m)) тап: r*r <= m болатын ең үлкен бүтін r. Жауап бойынша binary search қолдан (1e18 үшін float sqrt дәл емес).\nКіріс: t (1<=t<=2*10^4); t сан m_i (1<=m_i<=1e18).\nШығыс: әр m_i үшін floor(sqrt(m_i)), әрқайсысы жаңа жолда."
KZ['1C'] = "Max-heap-ті төменнен жоғары қарай құр. 1-ден индекстелген массивте i-дің балалары 2i және 2i+1. Sift down(i): i-дің баласы бар болғанша, үлкен мәнді баланы c деп ал (тең болса сол жағын); егер a_c > a_i болса, алмастырып i=c қой, әйтпесе тоқта. Оны i = floor(n/2)-ден 1-ге дейін кему ретімен қолдан.\nКіріс: n (1<n<1e5); n бүтін сан.\nШығыс: heap құрылғаннан кейінгі массив."
KZ['2A'] = "n бүтін саннан бір бағытты linked list құр, сілтемелерді (link) өзгерту арқылы тізімді кері айналдыр да шығар.\nКіріс: n (1<=n<=1e5); n бүтін сан.\nШығыс: кері айналған тізім, бос орынмен бөлініп."
KZ['2B'] = "Сұрыпталған n бүтін сан массиві және q сұраныс берілген. Әр x үшін массивте бар болса YES, әйтпесе NO шығар. Әр сұранысқа сызықтық іздеу баяу: binary search қолдан.\nКіріс: n (1<=n<=1e5); сұрыпталған a_i (1..1e9); q (1<=q<=1e5); q сан x_j.\nШығыс: әр сұранысқа YES/NO, жаңа жолда."
KZ['2C'] = "n студент (аты, балл) берілген. Балл бойынша кему ретімен сұрыпта; балл тең болса, аты бойынша алфавит ретімен. Comparator-мен quick sort немесе heap sort жаз.\nКіріс: n (1<=n<=1e5); n жол 'name score' (name: 1..10 кіші латын әрпі, score 0..100).\nШығыс: сұрыпталған студенттер, әрқайсысы жаңа жолда, сол форматта."
KZ['3A'] = "Linked list-ке мәні x жаңа түйінді p позициясына қой (нөлден басталады: 0 = жаңа бас (head), n = жаңа соңы). Тізімді шығар.\nКіріс: n (1<=n<=1e5); n бүтін сан (тізім басынан аяғына дейін); p және x (0<=p<=n).\nШығыс: n+1 сан, бос орынмен бөлініп."
KZ['3B'] = "n санды бос BST-ге ретімен енгіз (кіші болса солға, әйтпесе оңға). Ағаштың биіктігін шығар: түбірден ең ұзын жапыраққа дейінгі жолдағы түйін саны (бір түйін = 1).\nКіріс: n (1<=n<=500); n әртүрлі бүтін сан (1..1e9).\nШығыс: биіктік."
KZ['3C'] = "Студенттерді (аты, баға) баға бойынша өсу ретімен сұрыпта, ТҰРАҚТЫ (stable) сұрыптаумен: бағасы тең студенттер кіріс ретін сақтайды. Merge sort тең болғанда сол жақ жартыдан алады.\nКіріс: n (1<=n<=1e5); n жол 'name grade' (name: 1..10 кіші латын әрпі, grade 1..5).\nШығыс: сұрыпталған аттар, әрқайсысы жаңа жолда."
KZ['4A'] = "gcd(a, b) мен lcm(a, b)-ны Евклид алгоритмімен тап. lcm 1e18-ге жетуі мүмкін: 64-биттік тип (long long) қолдан.\nКіріс: a b (1<=a,b<=1e9).\nШығыс: gcd және lcm, бос орынмен бөлініп."
KZ['4B'] = "n санды бос BST-ге ретімен енгіз (кіші болса солға, әйтпесе оңға). Ағашты preorder ретімен шығар: түбір, сол ішкі ағаш, оң ішкі ағаш.\nКіріс: n (1<=n<=500); n әртүрлі бүтін сан (1..1e9).\nШығыс: preorder бойынша n сан, бос орынмен бөлініп."
KZ['4C'] = "Өсу ретімен (non-decreasing) сұрыпталған екі массивті ұзындығы n+m бір сұрыпталған массивке біріктір. Merge sort-тың merge процедурасын (екі көрсеткіш) қолдан, қайта сұрыптама.\nКіріс: n; n сан; m; m сан (n,m<=1e5, мәндер -1e9..1e9).\nШығыс: біріктірілген массив, бос орынмен бөлініп."
KZ['5A'] = "Эратосфен елегімен (sieve) p <= n болатын жай сандар санын тап.\nКіріс: n (1<=n<=1e6).\nШығыс: n-нен аспайтын жай сандар саны."
KZ['5B'] = "n санды бос BST-ге ретімен енгіз (кіші болса солға, әйтпесе оңға). Жапырақтар санын (балалары жоқ түйіндер) тап.\nКіріс: n (1<=n<=500); n әртүрлі бүтін сан (1..1e9).\nШығыс: жапырақ саны."
KZ['5C'] = "a_1..a_n массивінде binary heap сақталған: i-дің балалары 2i және 2i+1 (n-нен аспаса). Әр элемент өз балаларының әрқайсысынан үлкен болмаса, бұл min-heap. Массив min-heap екенін тексер.\nКіріс: n (1<=n<=1e5); n бүтін сан (1..1e9).\nШығыс: YES немесе NO."
KZ['6A'] = "Басында бос queue (кезек) және n операция: 'push x' x-ті соңына қосады; 'pop' алдыңғы элементті өшіріп, оны шығарады.\nКіріс: n (1<=n<=1e5); n жол: 'push x' (1<=x<=1e9) немесе 'pop'. pop кезінде кезек бос емес; кемінде бір pop бар.\nШығыс: әр pop шығарған сан, жаңа жолда."
KZ['6B'] = "Сұрыпталған n бүтін сан массиві және q сұраныс. Әр x үшін a_i >= x болатын ең кіші i индексін (1-ден санағанда) тап; барлық элемент x-тен кіші болса -1. Binary search қолдан.\nКіріс: n (1<=n<=1e5); сұрыпталған a_i (1..1e9); q (1<=q<=1e5); q сан x_j (1..1e9).\nШығыс: әр сұранысқа жауап, жаңа жолда."
KZ['6C'] = "n тас бар, i-ші тастың салмағы a_i. Кемінде екі тас болғанда, ең ауыр екеуін ал (салмақтары x <= y) және соқтығыстыр: x = y болса екеуі де жойылады, әйтпесе x жойылады да, екіншісінің салмағы y - x болады. Соңғы қалған тастың салмағын шығар (тас қалмаса 0). Max-heap қолдан.\nКіріс: n (1<=n<=1e5); n бүтін сан (1..1e9).\nШығыс: соңғы тастың салмағы немесе 0."
KZ['O1'] = "Сұрыпталған n бүтін сан массиві және q сұраныс. Әр x үшін оның массивте неше рет кездесетінін шығар. Lower bound және upper bound қолдан.\nКіріс: n (1<=n<=1e5); сұрыпталған a_i (1..1e9); q (1<=q<=1e5); q сан x_j (1..1e9).\nШығыс: әр сұранысқа кездесу саны, жаңа жолда."
KZ['O2'] = "Дәл бір рет Lomuto partition жаса да массивті шығар: pivot p = a_n, i = 0; j = 1..n-1 үшін: егер a_j < p болса, i++ және a_i мен a_j-ны алмастыр; соңында a_{i+1} мен a_n-ды алмастыр.\nКіріс: n (1<=n<=1e5); n бүтін сан (-1e9..1e9).\nШығыс: partition-нан кейінгі массив, бос орынмен бөлініп."
KZ['O3'] = "k-ші ең кіші элементті тап (өсу ретімен сұрыптағаннан кейін k-ші орында тұрған, 1-ден санағанда). Quick sort, heap sort немесе quickselect қолдан.\nКіріс: n (1<=n<=1e5); n бүтін сан (-1e9..1e9); k (1<=k<=n).\nШығыс: k-ші ең кіші элемент."
KZ['O4'] = "Max priority queue, басында бос, n операция: 'add x' x-ті қосады; 'extract' ең үлкен санды өшіріп, оны шығарады. Binary heap қолдан.\nКіріс: n (1<=n<=1e5); n жол 'add x' (1<=x<=1e9) немесе 'extract'. extract кезінде кезек бос емес; кемінде бір extract бар.\nШығыс: әр extract шығарған сан, жаңа жолда."
KZ['E1'] = "Linked list nxt массивімен берілген: i түйіні nxt_i-ге сілтейді (0 = тізім соңы). 1-түйіннен бастап тізімде цикл бар-жоғын анықта (бір түйінге екі рет жетсең, цикл бар). Мүмкін болса O(1) қосымша жад қолдан (Floyd).\nКіріс: n (1<=n<=1e5); n бүтін сан nxt_i (0<=nxt_i<=n).\nШығыс: цикл болса YES, әйтпесе NO."
KZ['E2'] = "n санды бос BST-ге енгіз (кіші болса солға, әйтпесе оңға). k-ші ең кіші мәнді шығар (inorder).\nКіріс: n (1<=n<=500); n әртүрлі бүтін сан; k (1<=k<=n).\nШығыс: k-ші ең кіші мән."
KZ['E3'] = "n оң бүтін саннан тұратын массивті дәл k бос емес тізбектес бөлікке бөл, ең үлкен бөлік қосындысы мүмкін болғанша кіші болсын. Сол минимумды шығар. (Жауап бойынша binary search + greedy тексеру.)\nКіріс: n k (1<=k<=n<=1e5); n бүтін сан (1..1e4).\nШығыс: ең үлкен қосындының минимал мәні."

# ---------- build tests: 2 samples + 8 generated = 10 ----------
for p in PB.values():
    r = random.Random(p['id'])
    ins = p['ex'] + [p['gen'](r, k) for k in (0, 0, 0, 1, 1, 2, 2, 2)]
    p['tests'] = [(i, p['sol'](i)) for i in ins]

# ---------- runner ----------
import signal
HIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
def trunc(x, n): return x[:n] + '…' if len(x) > n else x
def clean(t, d): return t.replace(d + os.sep, '').replace(d, '')
def same(out, exp):
    a, b = out.split(), exp.split()
    if b and all(x in ('YES', 'NO') for x in b): a = [x.upper() for x in a]  # yes/Yes/YES бәрі қабылданады
    return a == b
def diff(out, exp):
    ol = [l.split() for l in out.strip().splitlines() if l.strip()]; el = [l.split() for l in exp.strip().splitlines() if l.strip()]
    if not ol: return 'Жауап бос: ештеңе шығармадың (print / cout жазылды ма?)'
    for i in range(max(len(ol), len(el))):
        x = el[i] if i < len(el) else None; y = ol[i] if i < len(ol) else None
        if x is None: return f'Артық шығыс: {i+1}-жолда күтілмеген «{" ".join(y)[:60]}»'
        if y is None: return f'Шығыс тым қысқа: {i+1}-жол жоқ (күтілгені «{" ".join(x)[:60]}»)'
        for j in range(max(len(x), len(y))):
            u = x[j] if j < len(x) else '(жоқ)'; w = y[j] if j < len(y) else '(жоқ)'
            if u != w: return f'Алғашқы айырмашылық: {i+1}-жол, {j+1}-мән. Күтілгені «{u}», сенде «{w}»'
    return ''
def rc_hint(rc):
    if rc < 0:
        try: name = signal.Signals(-rc).name
        except Exception: name = str(-rc)
    else: name = {3221225477: 'SIGSEGV', 3221225725: 'SIGSEGV', 3221225620: 'SIGFPE'}.get(rc, '')
    return {'SIGSEGV': 'Segmentation fault: массивтен шығып кеттің, жарамсыз pointer (nullptr) немесе тым терең recursion.',
            'SIGFPE': 'Нөлге бөлу (division by zero) немесе integer overflow.',
            'SIGABRT': 'Abort: exception (vector.at, bad_alloc) немесе assert.'}.get(name, f'Программа exit code {rc} қайтарды (main соңында return 0 болуы керек).')

def run_tests(pid, lang, code):
    p = PB[pid]; d = tempfile.mkdtemp()
    try:
        if lang == 'cpp':
            src = os.path.join(d, 'a.cpp'); exe = os.path.join(d, 'a.exe' if os.name == 'nt' else 'a')
            open(src, 'w', encoding='utf-8').write(code)
            try:
                c = subprocess.run(['g++', '-O2', '-std=c++17', src, '-o', exe], capture_output=True, text=True, timeout=90)
            except FileNotFoundError:
                return {'ce': 'g++ табылмады. C++ компиляторын орнат (MinGW / build-essential / Xcode tools).', 'cel': []}
            if c.returncode:
                msg = clean(c.stderr, d)
                return {'ce': msg[:3000], 'cel': sorted({int(x) for x in re.findall(r'a\.cpp:(\d+):\d+: (?:fatal )?error', msg)})}
            cmd = [exe]
        else:
            try: compile(code, 'a.py', 'exec')
            except SyntaxError as e:
                return {'ce': f'SyntaxError: {e.msg}\n  жол {e.lineno}: {(e.text or "").strip()}', 'cel': [e.lineno or 1]}
            src = os.path.join(d, 'a.py'); open(src, 'w', encoding='utf-8').write(code); cmd = [sys.executable, src]
        res = []; shown = False
        for i, (inp, out) in enumerate(p['tests']):
            t = time.time(); got = ''; err = ''; hint = ''; line = None; dm = ''
            try:
                r = subprocess.run(cmd, input=inp, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=TL)
                dt = time.time() - t; got = r.stdout; ef = clean(r.stderr, d); err = ef[-600:]
                if r.returncode:
                    v = 'RE'
                    if lang == 'py':
                        m = re.findall(r'a\.py", line (\d+)', ef); line = int(m[-1]) if m else None
                        lines = [x for x in ef.strip().splitlines() if x.strip()]; hint = lines[-1] if lines else 'Runtime error'
                    else: hint = rc_hint(r.returncode)
                elif same(got, out): v = 'AC'
                else: v = 'WA'; dm = diff(got, out)
            except subprocess.TimeoutExpired:
                v = 'TLE'; dt = TL
                hint = f'Time limit {TL}s асты (тест {i+1}). Алгоритм тым баяу (мысалы O(n²)), шексіз цикл немесе кіріс күтіп тұр.'
            e = {'n': i + 1, 'v': v, 't': round(dt, 2)}
            if v != 'AC' and not shown:
                shown = True
                e.update(got=trunc(got, 300), err=err, hint=hint, diff=dm, inp=trunc(inp, 400), inpcut=len(inp) > 400, exp=trunc(out, 300))
                if line: e['line'] = line
            res.append(e)
        return {'res': res}
    finally:
        shutil.rmtree(d, True)

# ---------- web ----------
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, body, ct='application/json'):
        b = body.encode('utf-8'); self.send_response(200); self.send_header('Content-Type', ct + '; charset=utf-8')
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path == '/api/p':
            self.send(json.dumps([dict(id=i, grp=PB[i]['grp'], title=PB[i]['title'], lvl=PB[i]['lvl'], topic=PB[i]['topic'], text=PB[i]['text'], kz=KZ.get(i, ''),
                                       ex=[{'i': a, 'o': b} for a, b in PB[i]['tests'][:2]]) for i in ORDER]))
        elif self.path == '/api/h':
            self.send(open(HIST, encoding='utf-8').read() if os.path.exists(HIST) else '{}')
        else: self.send(HTML, 'text/html')
    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        if self.path == '/api/h':
            open(HIST, 'w', encoding='utf-8').write(body.decode('utf-8')); self.send('{}'); return
        q = json.loads(body)
        self.send(json.dumps(run_tests(q['pid'], q['lang'], q['code'])))

HTML = r"""<!doctype html><html lang="kk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ADS Midterm Judge</title><style>
:root{color-scheme:light}
body{margin:0;font:16px "Lucida Grande",Verdana,sans-serif;background:#e9e9e9;color:#222}
#top{background:linear-gradient(#cfcfcf,#f3f3f3 60%,#fafafa);padding:8px 24px 6px;display:flex;gap:24px;align-items:flex-start}
.ti{font-weight:bold;font-size:22px;margin:10px 0 20px;text-shadow:1px 1px 2px #bbb}
.nav{display:inline-flex;flex-wrap:wrap;border:1px solid #5a86b8;background:linear-gradient(#80b4f0,#5e9be0);box-shadow:0 2px 4px #aaa}
.nav a{padding:6px 26px;color:#143a66;font-weight:bold;cursor:pointer;border-right:1px solid #5a86b8;text-decoration:none}.nav a.on{background:linear-gradient(#5d8cc0,#6fa1d6)}
#clk{background:linear-gradient(#a8c8a0,#7fa878);border-top:1px solid #5d8a55;border-bottom:1px solid #5d8a55;padding:4px 32px;font-size:15px}
#pg{background:linear-gradient(#fff,#e4e4e4);padding:30px 0 40px;min-height:70vh}
.sec{display:inline-block;background:linear-gradient(#a9c8a2,#7ea577);border:1px solid #6c9266;border-left:0;border-radius:0 14px 0 0;padding:6px 36px 6px 40px;font-weight:bold;font-size:20px;margin-bottom:22px}
.in{padding:0 28px;overflow-x:auto}
table.t{border-collapse:collapse;border:1px solid #5a86b8;background:#fff}
table.t th{background:linear-gradient(#80b4f0,#5e9be0);color:#12365f;padding:6px 10px;text-align:left;border:1px solid #5a86b8}
table.t td{padding:6px 10px;border:1px solid #9aa}
tr.ok td{background:#c1d9c1}tr.bad td{background:#e7c5c5}tr.na td{background:#f6f6f6}
a{color:#2c5d2c;cursor:pointer}.pl a{margin-right:12px;font-weight:bold}.pl a.on{color:#000;text-decoration:none;border-bottom:2px solid #5a86b8}
pre{background:#f6f6f6;border:1px solid #bbb;padding:8px;white-space:pre-wrap;font:13px ui-monospace,Menlo,monospace}
textarea{width:min(900px,100%);height:320px;font:13.5px ui-monospace,Menlo,monospace;border:1px solid #5a86b8;padding:8px;tab-size:4}
select,input,button{font:inherit;padding:5px 10px}
button{background:linear-gradient(#80b4f0,#5e9be0);border:1px solid #5a86b8;color:#12365f;font-weight:bold;cursor:pointer}button:disabled{opacity:.5}
.b{font-size:12px;border:1px solid #888;border-radius:9px;padding:1px 8px;margin-right:6px;background:#fff}
.ex{display:grid;grid-template-columns:1fr 1fr;gap:0 14px;max-width:900px}
.cv{white-space:pre;overflow-x:auto;max-width:900px}.cv span{display:block}.cv i{display:inline-block;width:38px;color:#888;font-style:normal}.cv .er{background:#f5b5b5}
footer{padding:14px 24px;font-size:13px;color:#444}
.CodeMirror{height:430px;width:min(900px,100%);border:1px solid #5a86b8;font:14px ui-monospace,Menlo,monospace;line-height:1.45}.CodeMirror-focused{box-shadow:0 0 0 2px #7db3ee}
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closebrackets.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/matchbrackets.min.js"></script></head><body>
<div id="top"><svg width="150" height="130" viewBox="0 0 150 130"><rect width="150" height="130" fill="#aaa"/><rect x="12" y="12" width="126" height="106" fill="#eee"/><rect x="25" y="45" width="55" height="55" fill="#4caf3c" transform="rotate(-20 50 70)"/><rect x="45" y="60" width="28" height="28" fill="#eee" transform="rotate(-20 59 74)"/><rect x="80" y="25" width="40" height="40" fill="#333" transform="rotate(30 100 45)"/><rect x="95" y="80" width="30" height="22" fill="#555"/></svg>
<div><div class="ti" id="ti"></div><div class="nav" id="nav"></div></div></div>
<div id="clk"></div><div id="pg"><div class="in" id="body"></div></div>
<footer>ADS Midterm Judge (local) · тест: 10/есеп · TL 3 s · Python / g++</footer>
<script>
const $=s=>document.querySelector(s),esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
let P=[],tab='info',arg=null,busy=false;
const D={runs:[],next:1,c:{},name:"Байдулла Мейірхан",lang:"cpp",pid:null};let lastId=null,tm;
let S=Object.assign({},D,JSON.parse(localStorage.ads2||'{}'));
const save=()=>{localStorage.ads2=JSON.stringify(S);clearTimeout(tm);tm=setTimeout(()=>fetch('/api/h',{method:'POST',body:JSON.stringify(S)}),400)};
const LAB={AC:'OK',WA:'Wrong answer',RE:'Run-time error',TLE:'Time-limit exceeded'},LN={py:'python',cpp:'g++'};
const TPL={py:'import sys\ninput = sys.stdin.readline\n\n# код мұнда\n',cpp:'#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    // код мұнда\n    return 0;\n}\n'};
const NAV=[['info','Info'],['summary','Summary'],['submissions','Submissions'],['standings','Standings'],['settings','Settings']];
const fmt=d=>new Date(d).toLocaleString('sv-SE');
const go=(t,a)=>{tab=t;arg=a??null;lastId=null;render()};
const run=id=>S.runs.find(r=>r.id==id), pr=id=>P.find(p=>p.id==id);
const passed=r=>r.tests.filter(t=>t.v=='AC').length;
function render(){ed=null;const T={info:'Info',summary:'Problem summary',submissions:'Submissions',standings:'Standings',settings:'Settings',report:'Report',source:'Source'}[tab];
 $('#ti').textContent=`${S.name} [ADS-Midterm]: ${T}`;
 $('#nav').innerHTML=NAV.map(([k,n])=>`<a class="${k==tab?'on':''}" onclick="go('${k}')">${n}</a>`).join('');
 $('#body').innerHTML=({info,summary,submissions,standings,settings,report,source})[tab]();
 if(tab=='info')initInfo()}
function info(){const id=arg||S.pid||P[0].id,p=pr(id);S.pid=id;const hist=S.runs.filter(r=>r.pid==id),lr=lastId&&run(lastId);
 return `<div class="sec">Problem statements</div><div class="pl">${P.map(q=>`<a class="${q.id==id?'on':''}" onclick="go('info','${q.id}')">${q.id}</a>`).join('')}</div>
 <h2>${p.id}. ${esc(p.title)}</h2><span class="b">${p.lvl}</span><span class="b">${esc(p.topic)}</span><span class="b">Time limit: 3 s</span><span class="b">Memory limit: 256 MB</span>
 <p style="margin:8px 0"><a onclick="S.lng=(S.lng||'kz')=='kz'?'en':'kz';save();render()">🌐 ${(S.lng||'kz')=='kz'?'English (емтихандағы түпнұсқа)':'Қазақша көрсету'}</a></p><pre style="max-width:900px">${esc((S.lng||'kz')=='kz'&&p.kz?p.kz:p.text)}</pre><div class="ex">${p.ex.map((e,i)=>`<div><b>Input ${i+1}</b><pre>${esc(e.i)}</pre></div><div><b>Output ${i+1}</b><pre>${esc(e.o)}</pre></div>`).join('')}</div>
 <div class="sec" style="margin-top:20px">Submit a solution</div><p>Language: <select id="lg" onchange="sw(this.value)"><option value="cpp">g++</option><option value="py">python</option></select>
 <button id="sb" onclick="submit()">Send!</button> <span id="st"></span></p><textarea id="code" spellcheck="false" oninput="sv()"></textarea>
 <p style="color:#555;font-size:14px">Кез келген алгоритм қабылданады: жауап пен уақыт қана тексеріледі. Қайта-қайта жібере бер, тарих сақталады.</p>
 ${lr&&lr.pid==id?`<div class="sec" id="res">Result of run ${lr.id}</div>${reportBody(lr)}`:''}
 <div class="sec" style="margin-top:20px">History of ${id}</div>`+(hist.length?`<table class="t"><tr><th>Run ID</th><th>Time</th><th>Language</th><th>Result</th><th>Tests</th><th>Report</th><th>Code</th></tr>`+
 hist.map(r=>`<tr class="${r.result=='OK'?'ok':'bad'}"><td>${r.id}</td><td>${fmt(r.time)}</td><td>${LN[r.lang]}</td><td>${r.result}</td><td>${passed(r)}/10</td><td><a onclick="go('report',${r.id})">View</a></td><td><a onclick="loadCode(${r.id})">Load into editor</a></td></tr>`).join('')+`</table>`:'<p>Әлі жіберілген жоқ.</p>')}
let ed=null,loading=false;const MODE={py:'python',cpp:'text/x-c++src'};
const gc=()=>ed?ed.getValue():$('#code').value,sc=v=>{loading=true;ed?ed.setValue(v):$('#code').value=v;loading=false};
const ld=()=>sc(S.c[S.pid+S.lang]??TPL[S.lang]),sv=()=>{S.c[S.pid+S.lang]=gc();save()};
const ins=(t,x)=>{const s=t.selectionStart;t.value=t.value.slice(0,s)+x+t.value.slice(t.selectionEnd);t.selectionStart=t.selectionEnd=s+x.length;sv()};
function fbKeys(e){const t=e.target,s=t.selectionStart;
 if(e.key=='Tab'){e.preventDefault();ins(t,'    ')}
 else if(e.key=='Enter'){e.preventDefault();const ln=t.value.slice(t.value.lastIndexOf('\n',s-1)+1,s);ins(t,'\n'+ln.match(/^\s*/)[0]+(/[{:(\[]\s*$/.test(ln)?'    ':''))}}
function initInfo(){$('#lg').value=S.lang;const ta=$('#code');
 if(window.CodeMirror){ed=CodeMirror.fromTextArea(ta,{mode:MODE[S.lang],theme:'dracula',lineNumbers:true,indentUnit:4,tabSize:4,indentWithTabs:false,smartIndent:true,autoCloseBrackets:true,matchBrackets:true,
  extraKeys:{Tab:c=>c.somethingSelected()?c.indentSelected('add'):c.replaceSelection('    ','end'),'Shift-Tab':c=>c.indentSelected('subtract')}});ed.on('change',()=>{if(!loading)sv()})}
 else ta.addEventListener('keydown',fbKeys);
 ld()}
function sw(l){sv();S.lang=l;save();if(ed)ed.setOption('mode',MODE[l]);ld()}
async function submit(){if(busy)return;busy=true;$('#sb').disabled=true;$('#st').textContent='Testing…';const code=gc(),pid=S.pid,lang=S.lang;
 const r=await(await fetch('/api/run',{method:'POST',body:JSON.stringify({pid,lang,code})})).json();busy=false;
 const rn={id:S.next++,time:Date.now(),size:new Blob([code]).size,pid,lang,code,ce:r.ce||null,cel:r.cel||[],tests:r.res||[]};
 const f=rn.tests.find(t=>t.v!='AC');rn.result=rn.ce?'Compilation error':f?LAB[f.v]:'OK';rn.failed=rn.ce||!f?'N/A':f.n;
 S.runs.unshift(rn);save();lastId=rn.id;tab='info';arg=pid;render();$('#res').scrollIntoView()}
const loadCode=id=>{const r=run(id);S.pid=r.pid;S.lang=r.lang;S.c[r.pid+r.lang]=r.code;save();go('info',r.pid)};
const codeView=(c,ls)=>`<pre class="cv">`+c.split('\n').map((l,i)=>`<span class="${ls.includes(i+1)?'er':''}"><i>${i+1}</i>${esc(l)||' '}</span>`).join('')+`</pre>`;
function reportBody(r){let h=`<p>Problem <b>${r.pid}</b>, ${LN[r.lang]}, ${fmt(r.time)}: <b style="color:${r.result=='OK'?'#2b7a2b':'#b02020'}">${r.result}</b>${r.ce?'':` — өткен тест: ${passed(r)}/10, баға: ${passed(r)*10}%`}</p>`;
 if(r.ce)return h+`<h3>Compilation error</h3><pre>${esc(r.ce)}</pre>`+(r.cel.length?`<p>Қате жолдар: <b>${r.cel.join(', ')}</b></p>`:'')+codeView(r.code,r.cel);
 h+=`<table class="t"><tr><th>Test</th><th>Result</th><th>Time</th></tr>`+r.tests.map(t=>`<tr class="${t.v=='AC'?'ok':'bad'}"><td>${t.n}</td><td>${LAB[t.v]}</td><td>${t.t}s</td></tr>`).join('')+`</table>`;
 const f=r.tests.find(t=>t.v!='AC');
 if(f){h+=`<h3>Қате: test ${f.n} — ${LAB[f.v]}</h3>`;
  if(f.hint)h+=`<p><b>${esc(f.hint)}</b></p>`;if(f.diff)h+=`<p>⚠ ${esc(f.diff)}</p>`;
  if(f.line)h+=`<p>Қате жол: <b>${f.line}</b></p>`;
  h+=`<b>Input${f.inpcut?' (қысқартылған)':''}:</b><pre>${esc(f.inp)}</pre><b>Expected:</b><pre>${esc(f.exp)}</pre><b>Your output:</b><pre>${esc(f.got||'(бос)')}</pre>`;
  if(f.err)h+=`<b>stderr:</b><pre>${esc(f.err)}</pre>`;
  if(f.line)h+=codeView(r.code,[f.line])}
 return h}
function summary(){return `<div class="sec">Problem status summary</div><table class="t"><tr><th>Short name</th><th>Long name</th><th>Status</th><th>Failed test</th><th>Run ID</th></tr>`+
 P.map(p=>{const rs=S.runs.filter(r=>r.pid==p.id),ok=rs.find(r=>r.result=='OK'),r=ok||rs[0];
  return `<tr class="${!r?'na':ok?'ok':'bad'}"><td>${p.id}</td><td><a onclick="go('info','${p.id}')">${esc(p.title)}</a></td><td>${r?r.result:''}</td><td>${r&&!ok&&r.failed!='N/A'?r.failed:''}</td><td>${r?`<a onclick="go('report',${r.id})">${r.id}</a>`:''}</td></tr>`}).join('')+`</table>`}
function submissions(all){const rs=all?S.runs:S.runs.slice(0,15);
 return `<div class="sec">Sent submissions (${all?'all':'last 15'})</div><table class="t"><tr><th>Run ID</th><th>Time</th><th>Size</th><th>Problem</th><th>Language</th><th>Result</th><th>Failed test</th><th>View source</th><th>View report</th></tr>`+
 rs.map(r=>`<tr><td>${r.id}</td><td>${fmt(r.time)}</td><td>${r.size}</td><td>${r.pid}</td><td>${LN[r.lang]}</td><td>${r.result}</td><td>${r.failed}</td><td><a onclick="go('source',${r.id})">View</a></td><td><a onclick="go('report',${r.id})">View</a></td></tr>`).join('')+
 `</table>`+(all?'':`<p><a style="font-size:20px" onclick="tab='submissions';$('#body').innerHTML=submissions(true)">View all</a></p>`)}
function standings(){let tot=0;const rows=P.map(p=>{const rs=S.runs.filter(r=>r.pid==p.id),best=Math.max(0,...rs.map(passed));tot+=best;
  return `<tr class="${!rs.length?'na':best==10?'ok':'bad'}"><td>${p.id}</td><td>${esc(p.title)}</td><td>${p.lvl}</td><td>${rs.length}</td><td>${best}/10</td><td>${best*10}</td></tr>`}).join('');
 return `<div class="sec">Standings</div><p><b>Жалпы баға: ${Math.round(tot/(P.length*10)*100)}%</b> (${tot}/${P.length*10} тест)</p><table class="t"><tr><th>Problem</th><th>Name</th><th>Level</th><th>Attempts</th><th>Best tests</th><th>Score</th></tr>${rows}</table>`}
function report(){const r=run(arg);return `<div class="sec">Report for run ${r.id}</div>`+reportBody(r)+`<p><a onclick="loadCode(${r.id})">Осы кодты редакторға жүктеу</a></p>`}
const source=()=>{const r=run(arg);return `<div class="sec">Source of run ${r.id}</div><p>Problem ${r.pid}, ${LN[r.lang]}</p><pre>${esc(r.code)}</pre>`};
const settings=()=>`<div class="sec">Settings</div><p>Аты: <input id="nm" value="${esc(S.name)}"> <button onclick="S.name=$('#nm').value;save();render()">Save</button></p><p><button onclick="if(confirm('Барлық submission өшеді. Жалғастырасың ба?')){S.runs=[];S.next=1;S.c={};save();render()}">Reset all data</button></p>`;
setInterval(()=>$('#clk').textContent=new Date().toLocaleTimeString('sv-SE')+' / RUNNING',1000);$('#clk').textContent='…';
Promise.all([fetch('/api/p').then(r=>r.json()),fetch('/api/h').then(r=>r.json()).catch(()=>({}))]).then(([d,h])=>{P=d;if(h&&h.next>=S.next)S=Object.assign({},D,h);render()});
</script></body></html>"""

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Judge іске қосылды: http://localhost:{port}  (тоқтату: Ctrl+C)")
    try: webbrowser.open(f"http://localhost:{port}")
    except Exception: pass
    ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
