#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os import path
from flask import Flask
from flask import json
from flask import request
from pickle import load
from pandas import DataFrame
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

scoring_obj = None
data_path = 'data'
file_name = 'model.pkl'


@app.route('/api/credits/scoring/', methods=['POST'])
def scoring():
    try:
        return json.dumps({"scoring_result": get_score(request.json)})
    except Exception as e:
        raise BadRequest("Scoring counting failed. Details: {}".format(e))

cols = [
    u'RevolvingUtilizationOfUnsecuredLines',
    u'age',
    u'NumberOfTime30-59DaysPastDueNotWorse',
    u'DebtRatio',
    u'MonthlyIncome',
    u'NumberOfOpenCreditLinesAndLoans',
    u'NumberOfTimes90DaysLate',
    u'NumberRealEstateLoansOrLines',
    u'NumberOfTime60-89DaysPastDueNotWorse',
    u'NumberOfDependents'
]


def get_score(data_dict):
    """
    :param data_dict:
        age: int
        credit_monthly_payments: []
        credits_residue (except real estate and car loans): []
        credit_limits (except real estate and car loans): []
        MonthlyIncome: float
        NumberOfTimes90DaysLate: int
        NumberOfDependents: int
        NumberOfTime30-59DaysPastDueNotWorse: int
        NumberOfTime60-89DaysPastDueNotWorse: int
        NumberRealEstateLoansOrLines: int
        NumberOfOpenCreditLinesAndLoans: int
    :return:
        scoring value
    """
    data_dict['DebtRatio'] = \
        sum(data_dict['credit_monthly_payments']) / (data_dict['MonthlyIncome'] + 1)

    data_dict['RevolvingUtilizationOfUnsecuredLines'] = \
        (sum(data_dict['credits_residue']) + 1) / (sum(data_dict['credit_limits']) + 1)

    data_dict['MonthlyIncome'] = \
        data_dict['MonthlyIncome'] * 4.0 * 3263 / 959.0

    del data_dict['credit_monthly_payments']
    del data_dict['credits_residue']
    del data_dict['credit_limits']

    pd_data = DataFrame(data_dict, index=[1, ])
    score = scoring_obj.predict_proba(pd_data[cols])
    return score[0][0]


def main():
    with open(path.join(data_path, file_name)) as f:
        global scoring_obj
        scoring_obj = load(f)
    app.run('0.0.0.0', port=8001)


if __name__ == '__main__':
    main()
