import json
from typing import List
from prettytable import PrettyTable

from models import OutputInfo, NFT, Attribute, AttributeInfo, Property

tier_1_attributes: List[AttributeInfo] = []
tier_2_attributes: List[AttributeInfo] = []
tier_3_attributes: List[AttributeInfo] = []

tier1: List[OutputInfo] = []
tier2: List[OutputInfo] = []
tier3: List[OutputInfo] = []


def get_weight(property: str, item_tier: int, trait_type: str) -> int:
    if item_tier == 3:
        for item in tier_3_attributes:
            if item.trait_type == trait_type:
                item.all_quantity += 1
                for p in item.properties:
                    if p.name == property:
                        p.quantity += 1
                        return p.weight
    if item_tier == 2:
        for item in tier_2_attributes:
            if item.trait_type == trait_type:
                item.all_quantity += 1
                for p in item.properties:
                    if p.name == property:
                        p.quantity += 1
                        return p.weight
    if item_tier == 1:
        for item in tier_1_attributes:
            if item.trait_type == trait_type:
                item.all_quantity += 1
                for p in item.properties:
                    if p.name == property:
                        p.quantity += 1
                        return p.weight
    return 0


def count_all_quantity():
    for item in tier_3_attributes:
        sum = 0
        for p in item.properties:
            sum += p.quantity
        item.all_quantity = sum
    for item in tier_2_attributes:
        sum = 0
        for p in item.properties:
            sum += p.quantity
        item.all_quantity = sum
    for item in tier_1_attributes:
        sum = 0
        for p in item.properties:
            sum += p.quantity
        item.all_quantity = sum


def get_data(index: int) -> OutputInfo:

    with open(f'1000_1/{index}.json', "r") as f:
        text = f.read()
    dict_data = dict(json.loads(text))

    attributes: List[Attribute] = []
    for attribute in dict_data['attributes']:
        attributes.append(Attribute(trait_type=attribute.get("trait_type"),
                                    value=attribute.get("value")))

    return OutputInfo(item=NFT(name=dict_data['name'],
                               image=dict_data['image'],
                               attributes=attributes,
                               tier=dict_data['attributes'].pop().get("value")), rarity_score=0)


def init_attributes():
    with open('tier1_attributes', "r") as f:
        text = f.read()

    dict_list = []
    text = json.loads(text)

    for t in text:
        dict_list.append(dict(t))

    for item in dict_list:
        property_list: List[Property] = []
        for property in item['properties']:
            property_list.append(Property(name=property.get("name"), quantity=0, weight=property.get("weight")))

        tier_1_attributes.append(AttributeInfo(trait_type=item['trait_type'], all_quantity=0, properties=property_list))

    with open('tier2_attributes', "r") as f:
        text = f.read()

    dict_list = []
    text = json.loads(text)

    for t in text:
        dict_list.append(dict(t))

    for item in dict_list:
        property_list: List[Property] = []
        for property in item['properties']:
            property_list.append(Property(name=property.get("name"), quantity=0, weight=property.get("weight")))

        tier_2_attributes.append(
            AttributeInfo(trait_type=item['trait_type'], all_quantity=0, properties=property_list))

    with open('tier3_attributes', "r") as f:
        text = f.read()

    dict_list = []
    text = json.loads(text)

    for t in text:
        dict_list.append(dict(t))

    for item in dict_list:
        property_list: List[Property] = []
        for property in item['properties']:
            property_list.append(Property(name=property.get("name"), quantity=0, weight=property.get("weight")))

        tier_3_attributes.append(
            AttributeInfo(trait_type=item['trait_type'], all_quantity=0, properties=property_list))


def add_data_to_lists():
    for i in range(1, 1001):
        data = get_data(i)
        sum_value = 0
        for attribute in data.item.attributes:
            sum_value += get_weight(attribute.value, data.item.tier, attribute.trait_type)
        data.rarity_score = sum_value
        if data.item.tier == 1:
            tier1.append(data)
        if data.item.tier == 2:
            tier2.append(data)
        if data.item.tier == 3:
            tier3.append(data)
    tier1.sort(key=lambda x: x.rarity_score)
    tier2.sort(key=lambda x: x.rarity_score)
    tier3.sort(key=lambda x: x.rarity_score)


def output_attributes_info(data: list, tier: int):
    with open(f'tier_{tier}_data.txt', 'w') as fp:
        for item in data:
            output = PrettyTable()
            output.title = item.trait_type
            output.field_names = ['name', 'weight', 'percentage']
            for p in item.properties:
                double = 0
                if p.quantity != 0: double = (p.quantity / item.all_quantity) * 100
                output.add_row([p.name, p.weight, "{:.{}f}".format(double, 2)])
            fp.write(output.get_string())
            fp.write('\n\n')


def main():
    init_attributes()
    add_data_to_lists()
    count_all_quantity()
    output_attributes_info(tier_1_attributes, 1)
    output_attributes_info(tier_2_attributes, 2)
    output_attributes_info(tier_3_attributes, 3)

    return 0


main()
