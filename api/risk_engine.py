def calculate_risk(probability, anomaly_flag):

    if probability > 0.7 or anomaly_flag == -1:
        return "HIGH"

    elif probability > 0.4:
        return "MEDIUM"

    else:
        return "LOW"