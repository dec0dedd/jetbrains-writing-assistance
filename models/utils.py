from Levenshtein import distance


def dist(x):
    return distance(x['wrong'], x['correct'])


def get_matrix(x):
    ground_truth = set(x['correct'].split())
    model_out = set(x['correction'].split())
    original = set(x['correct'].split())

    tp = len(ground_truth.intersection(model_out))
    fp = len(model_out - ground_truth)
    tn = len(ground_truth.intersection(original) - model_out)
    fn = len(ground_truth - model_out)

    return [tp, fp, tn, fn]