from graphviz import Digraph
import json

# todo:hack
langFile = open('lang/zh-CN.json')
lang = json.load(langFile)


def get_lang(name):
    for langGroupKey, langGroup in lang.items():
        if name in langGroup:
            return langGroup[name]


recipesFile = open('data/recipe.json')
recipes = json.load(recipesFile)

nodes = {}
edges = {}


# 添加配方
def add_recipe(recipe):
    # 将当前配方添加到节点
    add_node(recipe['name'], recipe['label'] + ' ' + str(recipe['amount']))

    # 遍历配方所需材料
    for ingredient in recipe['ingredients']:

        ingredient_name = ''
        amount = None
        if isinstance(ingredient, list):
            ingredient_name = ingredient[0]
            amount = ingredient[1]

        elif isinstance(ingredient, dict):
            ingredient_name = ingredient['name']
            amount = ingredient['amount']

        # 材料存在于配方中
        if ingredient_name in recipes:
            # 添加配方
            add_recipe(recipes[ingredient_name])
        else:
            # 添加节点
            add_node(ingredient_name, get_lang(ingredient_name))

        # 添加边
        add_edge(ingredient_name, recipe['name'], label=str(amount))
    return


# 添加所有配方
def add_recipe_all():
    for key, recipe in recipes.items():
        add_recipe(recipe)


# 添加节点
def add_node(name, label):
    if name not in nodes:
        nodes[name] = {
            'name': name,
            'label': label
        }


# 添加边
def add_edge(tail_name, head_name, label=None):
    name = tail_name + '-' + head_name
    if name not in edges:
        edges[name] = {
            'tail_name': tail_name,
            'head_name': head_name,
            'label': label
        }


# add_recipe_all()
# add_recipe(recipes['burner-inserter'])
add_recipe(recipes['inserter'])
# add_recipe(recipes['stack-inserter'])
# add_recipe(recipes['iron-gear-wheel'])
# add_recipe(recipes['utility-science-pack'])

g = Digraph('result')
for key, node in nodes.items():
    g.node(node['name'], node['label'])

for key, edge in edges.items():
    g.edge(edge['tail_name'], edge['head_name'], label=edge['label'])

g.view()
