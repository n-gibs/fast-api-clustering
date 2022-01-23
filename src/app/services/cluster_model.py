from typing import List

import pickle
import numpy as np
import pandas as pd
import sklearn
from loguru import logger
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from src.app.db import db, Session
from src.app.core.messages import NO_VALID_PAYLOAD
from src.app.models.cluster_payload import CustomerSegmentationPayload
from src.app.models.cluster_prediction import CustomerSegmentationResult

class CustomerSegmentationModel(object):

    RESULT_UNIT_FACTOR = 100000

    def __init__(self, model_path):
        self.model_path = model_path
        self._load_local_model()

    def _load_local_model(self):
        with open(self.model_path, 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

    def _pre_process(self, data: pd.DataFrame) -> str:
        logger.debug("Pre-processing payload.")

        # TODO: Make modular, find categorical columns and encode all of them
        X = data.iloc[:, 1:5].values
        genders = data.iloc[:, 0].values
        # Encoding independent categorical variables
        labelencoder_X = LabelEncoder()
        X[:, 0] = labelencoder_X.fit_transform(genders)
        onehotencoder = OneHotEncoder()
        X = onehotencoder.fit_transform(X).toarray()
        return X

    def _predict(self, features: np.array) -> dict:
        logger.debug("Predicting.")
        clusters_result = self.model.fit_predict(features)
        return clusters_result

    def _post_process(self, data: pd.DataFrame) -> CustomerSegmentationResult:
        logger.debug("Post-processing clusters.")
        result = self._get_cluster_info(data)
        info = CustomerSegmentationResult(clusters=result)
        return info

    def predict(self, payload: CustomerSegmentationPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        session = Session()

        data = pd.DataFrame(pd.read_sql_table(table_name=payload.table_name, con=session.connection(), index_col="id"))
        pre_processed_payload = self._pre_process(data)

        session.close()

        clusters = self._predict(pre_processed_payload)

        data['Cluster'] = clusters
        post_processed_result = self._post_process(data)
        return post_processed_result

    def _get_cluster_info(block_data, df: pd.DataFrame):
        CONST_CLUSTER = 'Cluster'
        float_formatter = "{:.2f}".format

        clusters_info = dict()
        unique_values = df[CONST_CLUSTER].unique()
        for cluster_number in unique_values:
            cluster = dict()
            current_cluster = df[df[CONST_CLUSTER] == cluster_number]
            for (column_name, column_data) in current_cluster.items():
                if (column_name.find('ID') != -1 or column_name == CONST_CLUSTER):
                    continue

                if (column_data.dtype == 'object'):
                    unique_values = current_cluster[column_name].unique()
                    categorical = dict()
                    for val in unique_values:
                        categorical[val] = float_formatter(
                            np.sum(current_cluster[column_name] == val))
                        cluster[column_name] = categorical
                else:
                    col_max = float_formatter(current_cluster[column_name].max())
                    col_min = float_formatter(current_cluster[column_name].min())
                    col_mean = float_formatter(current_cluster[column_name].mean())
                    col_median = float_formatter(current_cluster[column_name].median())
                    col_std = float_formatter(current_cluster[column_name].std())

                    cluster[column_name] = {
                        'max': col_max,
                        'min': col_min,
                        'mean': col_mean,
                        'median': col_median,
                        'std': col_std
                    }

                clusters_info[str(cluster_number)] = cluster

        return clusters_info
