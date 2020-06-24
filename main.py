import re

programs = [
    """
(a b c)
    """,
    """
(a (b c) (d (e f) (g h i j)))
    """,
    """
(define (fib-iter n)
  (do ((num 2 (+ num 1))
       (fib-prev 1 fib)
       (fib 1 (+ fib fib-prev)))
      ((>= num n) fib)))
""",
    """
(define (fib-rec n)
  (if (< n 2)
      n
      (+ (fib-rec (- n 1))
         (fib-rec (- n 2)))))
""",
    """
(define (fib n)
  (let loop ((a 0) (b 1) (n n))
    (if (= n 0) a
        (loop b (+ a b) (- n 1)))))         
""",
    """
(define (sieve n)
  (define (aux u v)
    (let ((p (car v)))
      (if (> (* p p) n)
        (let rev-append ((u u) (v v))
          (if (null? u) v (rev-append (cdr u) (cons (car u) v))))
        (aux (cons p u)
          (let wheel ((u '()) (v (cdr v)) (a (* p p)))
            (cond ((null? v) (reverse u))
                  ((= (car v) a) (wheel u (cdr v) (+ a p)))
                  ((> (car v) a) (wheel u v (+ a p)))
                  (else (wheel (cons (car v) u) (cdr v) a))))))))
  (aux '(2)
    (let range ((v '()) (k (if (odd? n) n (- n 1))))
      (if (< k 3) v (range (cons k v) (- k 2))))))
""",
]

TOKENS = [
    (re.compile(r"\s+"), "whitespace"),
    (re.compile(r"\("), "paren-open"),
    (re.compile(r"\)"), "paren-close"),
    (re.compile(r"\d+"), "number"),
    (re.compile(r"[\w\-\?']+"), "atom"),
    (re.compile(r"\S+"), "operator"),
]


def tokenize(src):
    length = len(src)
    index = 0
    while index < length:
        source = src[index:]
        for pattern, token_type in TOKENS:
            match = pattern.match(source)
            if match:
                string = match[0]
                # start = match.start()
                end = match.end()
                index += end
                if token_type != "whitespace":
                    yield (token_type, string)
                break


def parse(tokens):
    token_type, string = tokens.pop(0)
    if token_type == "paren-open":
        array = []
        while tokens:
            if tokens[0][0] == "paren-close":
                tokens.pop(0)
                return array
            else:
                array.append(parse(tokens))
        # return parse_array(tokens)
    elif token_type == "number":
        return string
    elif token_type == "atom":
        return string
    elif token_type == "operator":
        return string
    else:
        raise ValueError("Unknown token_type {}".format(token_type))


def is_list(x):
    return isinstance(x, list)


def indent(string, level):
    prefix = " " * level
    return prefix + string


def one_line(ast):
    if is_list(ast):
        items = " ".join(one_line(x) for x in ast)
        return "({})".format(items)
    else:
        return str(ast)


def multi_line(ast, level):
    if is_list(ast):
        lines = []
        lines.append(indent("(", level))
        for index, x in enumerate(ast):
            lines += pretty_lines(x, level + 1)
        lines.append(indent(")", level))
        return lines
    else:
        return [indent(str(ast), level)]
    # if is_list(ast):
    #     lines = []
    #     lines.append(indent("(", level))
    #     for x in ast:
    #         lines += pretty_lines(x, level + 1)
    #     lines.append(indent(")", level))
    #     return lines
    # else:
    #     return [indent(str(ast), level)]


WIDTH = 80


def pretty_lines(ast, level=0):
    one = indent(one_line(ast), level)
    if len(one) <= WIDTH:
        return [one]
    else:
        multi = multi_line(ast, level)
        return multi


def format_line(line):
    edges = "░░"
    edges = "|"
    return edges + " " + line.ljust(WIDTH) + " " + edges


for src in programs[0:]:
    # continue
    print(src)
    # tokens = re.finditer(r"\w+|\(", src)
    # tokens = [match[0] for match in tokens]
    # print(tokens)
    tokens = tokenize(src)
    # for token_type, string in tokenize(src):
    #     if token_type == "whitespace":
    #         continue
    #     print('"{}"'.format(string), "  -  ", token_type)
    # print()
    ast = parse(list(tokens))
    # print(parsed)
    lines = pretty_lines(ast)
    for line in lines:
        print(format_line(line))
    print()
