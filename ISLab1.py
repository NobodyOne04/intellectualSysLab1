ITERATIONS = 2

CONVERTOR = {
	'Purpose': {
		'family': .1,
		'urban': .2,
		'sport': .5,
		'commercial': .7,
	},
	'Nsumber of passengers': {
		'2 passengers': .2,
		'4 passengers': .7,
		'> 4 passengers': .9,
	},
	'Body work': {
		'hatchback': .4,
		'SUV': .1,
		'crossover': .2,
		'sedan': .5,
		'pickup': .12,
		'minivan': .17,
		'limousine': .99,
		'roadster': .72,
		'cabriolet': .7,
		'compartment': .77,
	},
	'Gear box': {
		'automatic': 0,
		'manual': 1,
	},
	'Budget': {
		'Budget': .3,
		'Medium budget': .6,
		'Premium': .9,
	},
	'Condition': {
		'Requires service': .3,
		'Good condition': .6,
		'Factory': .9,
	}
}

RULE = lambda x, y: min(x, key=lambda x: abs(y - x))

def phasifier() -> list:
	result_list = list()
	for rule_key, rule in CONVERTOR.items():
		existing_values = ', '.join(list(rule.keys()))
		user_input_temp = input(f"{rule_key}? {existing_values}\n")

		assert user_input_temp in existing_values, f"{user_input} is not in {existing_values}"

		result_list.append(CONVERTOR[rule_key][user_input_temp])
	return result_list

def apply_rule_base(creterion: float, affiliation: list):
	coff_list, choice_list = affiliation, list()
	for _ in range(ITERATIONS):
		choice = RULE(coff_list, creterion)
		choice_list.append(
			coff_list.pop(
				coff_list.index(choice)
			)
		)
	return choice_list

def fuzzy_logical_output(user_input: list) -> list:
	result_list = list()
	for creterion, affiliation_keys in zip(user_input, CONVERTOR.keys()):
		result_list.append(
			apply_rule_base(
				creterion,
				list(CONVERTOR[affiliation_keys].values())
			)
		)
	return result_list

def aggregate(phasified_list: list) -> list:
	aggregated_list = list()
	for items in phasified_list:
		aggregated_list.append(sum(items)/len(items))
	return aggregated_list

def dephasifier(aggregate_output: list) -> None:
	dephasifier_list, weights_list = list(), list()
	for creterion, affiliation_key in zip(aggregate_output, CONVERTOR.keys()):
		affiliation_temp_dict = CONVERTOR[affiliation_key]

		choice_list = list(affiliation_temp_dict.values())

		temp_dephasifier_list, temp_weights_list = list(), list()

		for _ in range(ITERATIONS):
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

	for inx in range(ITERATIONS):
		output_str = ''.join(dephasifier_list[inx])
		weight = 1

		for temp_weight in weights_list[inx]:
			weight *= temp_weight

		print(f"Car list №{output_str} with weight {weight}")

if __name__ == '__main__':
	user_input_list = phasifier()
	rule_base_output_list = fuzzy_logical_output(user_input_list)
	aggregate_output_list = aggregate(rule_base_output_list)
	dephasifier(aggregate_output_list)

