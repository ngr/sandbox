from collections import defaultdict
from typing import List, Dict


by_destination = {}


def destinations_dict(schedule) -> Dict:
    result = defaultdict(list)
    for flight in schedule:
        result[flight[1]].append((flight[0], flight[2]))
    return dict(result)


def get_best_price(a, b):
    global by_destination

    best_price = None
    if b in by_destination:
        for source, price in by_destination[b]:
            if source == a:
                if not best_price:
                    best_price = price
                    break
                if price < best_price:
                    best_price = price
    # else:
    #     print(f"not found direct flights {a} to {b}")
    # print(f"best price direct for {a} to {b} is {best_price}")
    return best_price


def get_smart_price(source, destination, exclude_list=[], best=1000) -> List:
    global by_destination, root_destination

    best_price = get_best_price(source, destination)
    # if best_price < best:
    #     print(f"smart price found direct: {source} to {destination} with best {best_price}")
    #     return best_price
    # try:
    print(f"####Getting price {source} to {destination} with current best {best_price}")

    if destination not in by_destination:
        return None

    for src, value in by_destination[destination]:
        print(f"You can get to {destination} for {value} from {src}")
        cost = value

        # src, value = r
        if source == src:
            print(f"skipping {src} to {destination}")
            continue

        if (src, destination) in exclude_list:
            continue
        # if root_destination == destination:
        #     print(f"skippin root destination {destination}")
        #     continue

        # print(src, destination, value)
        # print(f"calculate {src}, {destination}")

        smart_price = get_smart_price(source, src, exclude_list=[*exclude_list, (src, destination)])

        # if not smart_price or smart_price == 1000:
        #     return None

        print(f"you can get to {destination} from {src} for {smart_price}")
        if smart_price and smart_price + cost <= best_price:
            best_price = smart_price + cost
            break
        else:
            return best_price
    # except ValueError as err:
    #     print(f"Caught exception for {source} to {destination}: {err}")

    # print(f"Best price for {source} -> {destination} is {best_price}")

    return best_price


def useless_flight(schedule: List) -> List:
    global by_destination, root_destination
    by_destination = destinations_dict(schedule)
    print(by_destination)
    # t = get_best_price('A', 'C')
    # print(t)

    result = []
    for i, (source, destination, cost) in enumerate(schedule):
        root_destination = destination
        best_price = cost
        print("core: ", source, destination, cost)

        if get_best_price(source, destination) < cost:
            print(f"already in best price {source}, {destination}, {cost}")
            result.append(i)
            continue

        smart_price = get_smart_price(source, destination)
        print(source, destination, "cost: ", cost, "smart_price:", smart_price)
        if smart_price < cost:
            print(f"smart_price {smart_price} < cost {cost}")
            result.append(i)

    print(f"Result: {result}")
    # your code here
    return result


if __name__ == '__main__':
    print("Example:")
    #   print(useless_flight([['A', 'B', 50],
    # ['B', 'C', 40],
    # ['A', 'C', 100]]))

    #   # These "asserts" are used for self-checking and not for an auto-testing
    #   print(useless_flight([['A', 'B', 50], ['B', 'C', 30], ['A', 'C', 90], ['A', 'C', 100]]))
    # print(useless_flight([['A', 'B', 50], ['B', 'C', 30], ['A', 'C', 90]]))

    # assert useless_flight([['A', 'B', 50], ['B', 'C', 30], ['A', 'C', 90], ['A', 'C', 100]]) == [2, 3]
    # assert useless_flight([['A', 'B', 50], ['B', 'C', 40], ['A', 'C', 90]]) == []

    #   assert useless_flight([['A', 'B', 50],
    # ['B', 'C', 40],
    # ['A', 'C', 40]]) == []
    assert useless_flight([
        ['A', 'C', 10],  # 0
        ['C', 'B', 10],  # 1
        ['C', 'E', 10],
        ['C', 'D', 10],  # 3
        ['B', 'E', 25],  # 4
        ['A', 'D', 20],
        ['D', 'F', 50],
        ['E', 'F', 90]  # 7
    ]) == [4, 7]
#   print("Coding complete? Click 'Check' to earn cool rewards!")
