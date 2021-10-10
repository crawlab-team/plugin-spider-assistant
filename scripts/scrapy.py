import ast
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('action')
parser.add_argument('-f', '--file', dest='filepath')
args = parser.parse_args()


def parse_items(filepath: str) -> list:
    # ast object
    ast_obj = _parse_ast(filepath)

    # results
    results = []

    # iterate body elements
    for el in ast_obj.body:
        # skip if type is not ast.ClassDef
        if type(el) != ast.ClassDef:
            continue

        # parsed results
        res = _parse_items_element(el)

        # skip if result is empty
        if res is None:
            continue

        # add to results
        results.append(res)

    return results


def parse_settings(filepath: str) -> list:
    # ast object
    ast_obj = _parse_ast(filepath)

    # results
    results = []

    # iterate body elements
    for el in ast_obj.body:
        # skip if type is not ast.Assign
        if type(el) != ast.Assign:
            continue

        # parsed result
        res = _parse_settings_element(el)

        # skip if result is empty
        if res is None:
            continue

        # add to results
        results.append(res)

    return results


def _parse_items_element(el) -> [dict, None]:
    # result
    res = {}

    # skip if bases is empty
    if len(el.bases) == 0:
        return

    # base
    b = el.bases[0]

    # skip if base is not valid
    if not _is_type(el, 'scrapy', 'Item'):
        return

    # item name
    res['name'] = el.name

    # item fields
    res['fields'] = []

    # iterate sub statements
    for stmt in el.body:
        # skip if type is not valid
        if type(stmt) != ast.Assign or type(stmt.value) != ast.Call:
            continue

        # skip if func is not valid
        if not _is_type(stmt.value.func, 'scrapy', 'Field'):
            continue

        # skip if targets empty
        if len(stmt.targets) == 0:
            continue

        # target
        tgt: ast.Name = stmt.targets[0]

        # skip if target is not ast.Name
        if type(tgt) != ast.Name:
            continue

        # field name
        field = tgt.id

        # add to fields
        res['fields'].append(field)

    return res


def _parse_settings_element(el) -> [dict, None]:
    # result
    res = {}

    # skip if targets is empty
    if len(el.targets) == 0:
        return

    # target
    tgt: ast.Name = el.targets[0]

    # skip if type is not ast.Name
    if type(tgt) != ast.Name:
        return

    # setting name
    res['name'] = tgt.id

    # element value
    ev = el.value

    # value type
    vt = type(ev)

    # if value is ast.Constant
    if vt == ast.Constant:
        _res = _get_constant_result(ev)
        res['type'] = _res['type']
        res['value'] = _res['value']

    # if value is ast.List
    if vt == ast.List:
        res['type'] = 'list'
        res['value'] = []
        # iterate sub elements
        for sub_el in ev.elts:
            # skip if sub element is not ast.Constant
            if type(sub_el) != ast.Constant:
                return
            res['value'].append(_get_constant_result(sub_el))

    # if value is ast.Dict
    if vt == ast.Dict:
        res['type'] = 'dict'
        res['value'] = []
        # iterate keys and values
        for i in range(len(ev.values)):
            key = ev.keys[i]
            value = ev.values[i]
            # skip if key or value is not ast.Constant
            if type(key) != ast.Constant or type(value) != ast.Constant:
                return
            res['value'].append({
                'key': _get_constant_result(key),
                'value': _get_constant_result(value),
            })

    return res


def _get_constant_result(el: ast.Constant) -> dict:
    return {
        'type': type(el.value).__name__,
        'value': el.value,
    }


def _parse_ast(filepath: str) -> ast.Module:
    with open(filepath) as f:
        src = f.read()

    res = ast.parse(src)
    print(ast.dump(res, indent=4))

    return res


def _is_type(el, m: str, t: str) -> bool:
    if type(el) == ast.Name:
        if el.id != t:
            return False
    elif type(el) == ast.Attribute:
        if type(el.value) != ast.Name or el.value.id != m:
            return False
        if el.attr != t:
            return False
    return True


def main():
    results = None
    if args.action == 'ast':
        results = _parse_ast(args.filepath)

    if args.action == 'items':
        results = parse_items(args.filepath)

    if args.action == 'settings':
        results = parse_settings(args.filepath)

    print(results)


if __name__ == '__main__':
    main()
