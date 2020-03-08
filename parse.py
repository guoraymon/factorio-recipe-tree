import json

langFile = open('lang/zh-CN.json')
lang = json.load(langFile)

rawDataFile = open('rawData/recipe.json')
rawDates = json.load(rawDataFile)


def get_lang(name):
    for langGroupKey, langGroup in lang.items():
        if name in langGroup:
            return langGroup[name]


recipes = {}
for rawData in rawDates:
    ingredients = {}

    # 默认配方
    if 'ingredients' in rawData:
        ingredients = rawData['ingredients']

    # 普通难度配方
    if 'normal' in rawData:
        ingredients = rawData['normal'].get('ingredients', {})

    # 配方产出数量
    # 默认为1
    amount = 1
    # 如果要results, 说明是多产出的，匹配到对应产出
    if 'results' in rawData:
        for rawItem in rawData['results']:
            if isinstance(rawItem, dict):
                if rawItem['name'] == rawData['name']:
                    amount = rawItem['amount']

            elif isinstance(rawItem, list):
                amount = rawItem[1]

    recipes[rawData['name']] = {
        'name': rawData['name'],
        'label': get_lang(rawData['name']),
        'ingredients': ingredients,
        'amount': amount
    }

# print(json.dumps(recipes))

with open('data/recipe.json', 'w') as dataFile:
    json.dump(recipes, dataFile, ensure_ascii=False)
