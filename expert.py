import json


class ExpertSystem:

    def __init__(self):
        self._ITERATIONS = 2
        self._RULE = lambda x, y: min(x, key=lambda x: abs(y - x))
        with open('./source/convertion.json', 'r') as convertor_file:
            self._CONVERTOR = json.load(convertor_file)

    def apply_rule_base(self, creterion: float, affiliation: list):
        coff_list, choice_list = affiliation, list()
        for _ in range(self._ITERATIONS):
            choice = self._RULE(coff_list, creterion)
            choice_list.append(
                coff_list.pop(
                    coff_list.index(choice)
                )
            )
        return choice_list

    def fuzzy_logical_output(self, user_input: list) -> list:
        result_list = list()
        for creterion, affiliation_keys in zip(user_input, self._CONVERTOR.keys()):
            result_list.append(
                self.apply_rule_base(
                    creterion,
                    list(self._CONVERTOR[affiliation_keys].values())
                )
            )
        return result_list

    def aggregate(self, phasified_list: list) -> list:
        aggregated_list = list()
        for items in phasified_list:
            aggregated_list.append(sum(items) / len(items))
        return aggregated_list

    def dephasifier(self, aggregate_output: list) -> list:
        dephasifier_list, weights_list = list(), list()
        for creterion, affiliation_key in zip(aggregate_output, self._CONVERTOR.keys()):
            affiliation_temp_dict = self._CONVERTOR[affiliation_key]

            choice_list = list(affiliation_temp_dict.values())

            temp_dephasifier_list, temp_weights_list = list(), list()

            for _ in range(self._ITERATIONS):
                choice = min(
                    choice_list,
                    key=lambda x: abs(creterion - x)
                )
                temp_weights_list.append(1 - abs(creterion - choice))
                temp_dephasifier_list.append(str(choice_list.index(choice)))
                del choice_list[choice_list.index(choice)]

            dephasifier_list.append(temp_dephasifier_list)
            weights_list.append(temp_weights_list)

        weights_list = list(map(list, zip(*weights_list)))
        dephasifier_list = list(map(list, zip(*dephasifier_list)))
        result_list = list()

        for inx in range(self._ITERATIONS):
            output_str = ''.join(dephasifier_list[inx])
            weight = 1

            for temp_weight in weights_list[inx]:
                weight *= temp_weight
            result_list.append(dict(weight=weight, number=output_str))
        return result_list
