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

"""
def get_matrix(x):
    wrg = x['wrong'].split()
    cor = x['correct'].split()
    corrc = x['correction'].split()

    if len(wrg) != len(cor) or len(wrg) != len(corrc):
        print(wrg)
        print("====")
        print(cor)
        print("====")
        print(corrc)

    assert len(wrg) == len(cor) and len(wrg) == len(corrc)

    res = [0, 0, 0, 0]  # res = [TP, FP, TN, FN]
    for w, c_true, cx in zip(wrg, cor, corrc):
        if w == c_true:
            # the word was correct so shouldn't have been changed

            if c_true == cx:
                # true negative
                res[2] += 1
            elif c_true != cx:
                # false positive (or was changed to incorrect word)
                res[1] += 1

        else:
            # the word was incorrect so should have been changed

            if c_true == cx:
                # true positive
                res[0] += 1
            else:
                # false negative (or was changed to incorrect word)
                res[3] += 1
    return res
"""
